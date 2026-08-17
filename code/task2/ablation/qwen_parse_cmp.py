"""Qwen3.5-9B parse versus the reference parse, aligned field by field.

## How to read these numbers

**Agreement is not correctness.** The 445 reference parses can themselves be wrong. What is
measured here is "can the 9B model reproduce the same parsing convention", not "is the 9B
model's parse right".

The one field that does act as a correctness proxy is `target.concept`: it directly decides
what the segmenter searches for, everything downstream fails when it is wrong, and its value
is the least convention-dependent of the fields.

## Per-field protocol

    concept / host   passed through the synonym groups (drawer handle == drawer pull) so a
                     synonym is not recorded as an error
    entities         Jaccard over the name sets, **plus role agreement on the intersection**,
                     reported separately -- "did it extract the right things" and "did it
                     assign the right roles" are two different questions
    relations        set P/R/F1, reported both strict and **canonical**. The canonical form
                     folds inverse relations onto one direction (right_of(a,b) becomes
                     left_of(b,a) and so on), because "A is left of B" and "B is right of A"
                     are two spellings of one constraint, and strict matching would score
                     that as two separate disagreements.
    select           set equality (on/axis/value, or an ordinal index). An empty select is
                     itself a value -- inventing an ordering constraint is exactly as harmful
                     as missing one.

    python code/task2/ablation/qwen_parse_cmp.py
"""
import os, sys, json, glob, re, argparse
from collections import Counter

_CODE_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, _CODE_ROOT)
from paths import ABLATION, CANDIDATES  # noqa: E402
QOUT = os.path.join(ABLATION, "qwen_parse")

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
# Reuse the one synonym table, so the two scripts cannot drift apart.
from qwen_parse import SYN                                       # noqa: E402
from qwen_parse import norm as _norm0                            # noqa: E402


def norm(s):
    """Extends the parse script's norm to also absorb `_` and `-`.

    door_handle and door handle are two spellings of one word -- a formatting difference,
    which must not be recorded as a content disagreement.
    """
    return re.sub(r"[_\-]+", " ", _norm0(s)).strip()


def same(a, b):
    """Synonym matching must use **this file's** norm.

    The parse script's own `same` closes over its own norm, which does not absorb
    underscores, and would score door_handle against door handle as two different words.
    """
    a, b = norm(a), norm(b)
    if a == b:
        return True
    if not a or not b:
        return False
    return any(a in g and b in g for g in SYN)


# Head-word synonyms. This measures "did it recognise that the target is the touchable
# part", reported separately from "did it name it the way we do":
#   reference 'drawer handle' vs model 'handle'  -- same head word; the part-level
#                                                   judgement is right, the naming coarser
#   reference 'drawer handle' vs model 'drawer'  -- head word is drawer; it took the whole
#                                                   piece of furniture to be the target
# These do very different damage downstream, and collapsing them into one number makes the
# difference unreadable.
HEAD_SYN = [
    {"handle", "pull", "knob", "grip", "lever", "latch"},
    {"button", "switch", "dial"},
    {"socket", "outlet"},
    {"plug"},
]


def head(s):
    w = norm(s).split()
    return w[-1] if w else ""


def head_ok(a, b):
    ha, hb = head(a), head(b)
    if not ha or not hb:
        return False
    if ha == hb:
        return True
    return any(ha in g and hb in g for g in HEAD_SYN)

# Inverse relations, folded onto a single direction under the canonical protocol.
INV = {"right_of": "left_of", "below": "above", "under": "above",
       "behind": "in_front_of", "has_on_top": "on_top"}
SYMM = {"next_to", "near", "between"}


def canon_rel(rel, a, b):
    r, a, b = norm(rel), norm(a), norm(b)
    if r in INV:
        r, a, b = INV[r], b, a
    if r in SYMM:
        a, b = sorted([a, b])
    return (r, a, b)


def rel_set(p, canon):
    out = set()
    for r in (p.get("relations") or []):
        if not isinstance(r, dict):
            continue
        rel, a, b = r.get("rel"), r.get("a"), r.get("b")
        out.add(canon_rel(rel, a, b) if canon else (norm(rel), norm(a), norm(b)))
    return out


def sel_set(p):
    out = set()
    for s in (p.get("select") or []):
        if not isinstance(s, dict):
            continue
        v = s.get("value")
        if v in (None, ""):
            idx = s.get("index")
            v = f"#{idx}" if idx not in (None, "") else ""
        out.add((norm(s.get("on")), norm(s.get("axis")), norm(str(v))))
    return out


def sel_core(p):
    """Drop the `on` name and keep only (axis, value).

    Separates "was the ordering constraint itself extracted correctly" from "what did it
    call the class the ordering applies to".
    """
    return {(a, v) for _, a, v in sel_set(p)}


def ent_map(p):
    """name -> role. On a repeated name, the first occurrence wins."""
    m = {}
    for e in (p.get("entities") or []):
        if isinstance(e, dict) and e.get("name"):
            m.setdefault(norm(e["name"]), norm(e.get("role")))
    return m


def syn_key(s):
    """Map a synonym onto its group representative, so entity-name set comparison also
    absorbs synonyms."""
    s = norm(s)
    for i, g in enumerate(SYN):
        if s in g:
            return f"@syn{i}"
    return s


def prf(P, G):
    if not P and not G:
        return 1.0, 1.0, 1.0
    tp = len(P & G)
    p = tp / len(P) if P else 0.0
    r = tp / len(G) if G else 0.0
    f = 2 * p * r / (p + r) if (p + r) else 0.0
    return p, r, f


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dump", default="candidates")
    ap.add_argument("--max_list", type=int, default=30)
    args = ap.parse_args()
    SRC = (CANDIDATES if args.dump == "candidates"
           else os.path.join(os.path.dirname(CANDIDATES), args.dump))

    qw = {}
    for f in sorted(glob.glob(os.path.join(QOUT, "qwen_parse_s*.jsonl"))):
        for line in open(f):
            try:
                r = json.loads(line)
            except Exception:
                continue
            qw[r["q"]] = r
    if not qw:
        sys.exit(f"no qwen_parse_s*.jsonl found under: {QOUT}")

    rows, n_fail, n_trunc = [], 0, 0
    for k, b in sorted(qw.items()):
        if b.get("parse_fail") or not isinstance(b.get("parse"), dict):
            n_fail += 1
            continue
        n_trunc += bool(b.get("truncated"))
        mf = os.path.join(SRC, k, "meta.json")
        if not os.path.exists(mf):
            continue
        gp = json.load(open(mf))["parse"]
        pp = b["parse"]

        gt_t, pt = (gp.get("target") or {}), (pp.get("target") or {})
        ge, pe = ent_map(gp), ent_map(pp)
        gk = {syn_key(x) for x in ge}
        pk = {syn_key(x) for x in pe}
        shared = [x for x in ge if syn_key(x) in pk]
        # Role agreement is computed only over entities BOTH sides extracted.
        rmatch = []
        for x in shared:
            y = next((z for z in pe if syn_key(z) == syn_key(x)), None)
            if y is not None:
                rmatch.append(ge[x] == pe[y])

        rs = prf(rel_set(pp, False), rel_set(gp, False))
        rc = prf(rel_set(pp, True), rel_set(gp, True))
        gs, ps = sel_set(gp), sel_set(pp)

        rows.append(dict(
            q=k, text=b.get("text", ""),
            concept_ok=same(pt.get("concept"), gt_t.get("concept")),
            head_ok=(same(pt.get("concept"), gt_t.get("concept"))
                     or head_ok(pt.get("concept"), gt_t.get("concept"))),
            concept_exact=(norm(pt.get("concept")) == norm(gt_t.get("concept"))),
            g_concept=gt_t.get("concept"), p_concept=pt.get("concept"),
            host_ok=(same(pt.get("host"), gt_t.get("host"))
                     or (not pt.get("host") and not gt_t.get("host"))),
            g_host=gt_t.get("host"), p_host=pt.get("host"),
            ent_jacc=(len(gk & pk) / len(gk | pk)) if (gk | pk) else 1.0,
            role_ok=(sum(rmatch) / len(rmatch)) if rmatch else float("nan"),
            role_all=(all(rmatch) and len(gk ^ pk) == 0),
            rel_f_strict=rs[2], rel_f_canon=rc[2],
            rel_exact=(rel_set(pp, True) == rel_set(gp, True)),
            sel_ok=(gs == ps), g_sel=sorted(gs), p_sel=sorted(ps),
            sel_core_ok=(sel_core(gp) == sel_core(pp)),
            n_sel_g=len(gs), n_sel_p=len(ps),
            n_out=b.get("n_out", 0)))

    n = len(rows)
    if not n:
        sys.exit("nothing comparable")
    m = lambda k: 100.0 * sum(bool(r[k]) for r in rows) / n
    avg = lambda k: sum(r[k] for r in rows if r[k] == r[k]) / max(
        sum(1 for r in rows if r[k] == r[k]), 1)

    print(f"\n{'='*74}")
    print(f"Qwen3.5-9B parse  vs  reference parse   -- {n} comparable "
          f"(parse failures {n_fail}, truncated {n_trunc})")
    print(f"{'='*74}")
    print(f"\n=== per-field agreement ===")
    print(f"  target.concept  **correct at part level** {m('head_ok'):>5.1f}%   "
          f"<- recognised a touchable part, not the whole furniture")
    print(f"                   same name (via synonyms) {m('concept_ok'):>5.1f}%   "
          f"literally identical {m('concept_exact'):>5.1f}%")
    hsub = [r for r in rows if r["concept_ok"]]
    hr = (100.0 * sum(r["host_ok"] for r in hsub) / len(hsub)) if hsub else float("nan")
    print(f"  target.host      {m('host_ok'):>5.1f}%   "
          f"(restricted to the {len(hsub)} where concept already agrees: {hr:.1f}%)")
    print(f"  entities  mean name-set Jaccard {100*avg('ent_jacc'):>5.1f}%    "
          f"role (on intersection) {100*avg('role_ok'):>5.1f}%    identical {m('role_all'):>5.1f}%")
    print(f"  relations F1  strict {100*avg('rel_f_strict'):>5.1f}%   "
          f"canon {100*avg('rel_f_canon'):>5.1f}%   identical under canon {m('rel_exact'):>5.1f}%")
    print(f"  select           fully identical {m('sel_ok'):>5.1f}%   "
          f"ignoring the on name {m('sel_core_ok'):>5.1f}%   "
          f"(invented {sum(r['n_sel_p']>r['n_sel_g'] for r in rows)}, "
          f"missed {sum(r['n_sel_p']<r['n_sel_g'] for r in rows)})")
    allok = [r for r in rows if r["concept_ok"] and r["host_ok"]
             and r["role_all"] and r["rel_exact"] and r["sel_ok"]]
    print(f"\n  all five fields correct: {len(allok)}/{n} ({100*len(allok)/n:.1f}%)")

    outs = sorted(r["n_out"] for r in rows)
    print(f"  output length: median {outs[len(outs)//2]} tok  max {outs[-1]}")

    # ---- what the concept disagreements look like: the most diagnostic table here ----
    bad = [r for r in rows if not r["head_ok"]]
    naming = [r for r in rows if r["head_ok"] and not r["concept_ok"]]
    print(f"\n=== target.concept: {len(naming)} differ only in naming granularity "
          f"(right part), {len(bad)} are wrong at the part level ===")
    npat = Counter((norm(r["g_concept"]), norm(r["p_concept"])) for r in naming)
    print(f"  -- naming granularity (task understood, but the retrieval term shifts) --")
    for (g, p), c in npat.most_common(8):
        print(f"  {c:>3}x   reference {g!r:<24} -> Qwen {p!r}")
    print(f"  -- part-level errors (genuinely wrong) --")
    pat = Counter((norm(r["g_concept"]), norm(r["p_concept"])) for r in bad)
    for (g, p), c in pat.most_common(12):
        print(f"  {c:>3}x   reference {g!r:<24} -> Qwen {p!r}")
    if len(pat) > 12:
        print(f"  ... {len(pat)-12} further patterns")
    for r in bad[:args.max_list]:
        print(f"    {r['q'][:4]}  {r['text'][:70]}")
        print(f"          reference {r['g_concept']!r} / host {r['g_host']!r}   "
              f"Qwen {r['p_concept']!r} / host {r['p_host']!r}")
    if len(bad) > args.max_list:
        print(f"    ... {len(bad)-args.max_list} more, see qwen_parse_cmp.json")

    # ---- select disagreements ----
    sbad = [r for r in rows if not r["sel_ok"]]
    print(f"\n=== select disagreements - {len(sbad)} (first 12) ===")
    for r in sbad[:12]:
        print(f"  {r['q'][:4]}  {r['text'][:64]}")
        print(f"        reference {r['g_sel']}   Qwen {r['p_sel']}")

    out = os.path.join(QOUT, "qwen_parse_cmp.json")
    json.dump(rows, open(out, "w"), indent=1, ensure_ascii=False)
    print(f"\ndetail -> {out}")
    print("⚠️ Agreement is not correctness: the reference parse can also be wrong.")
    print("   Read these as 'can it reproduce the same parsing convention'.")


if __name__ == "__main__":
    main()
