#!/usr/bin/env python3
"""Compare the Qwen3.5-9B reasoning arm against the frontier-LLM arm, question by question.

## Where the criterion comes from

**The ground truth is not re-projected here.** Each question's `gt_ids` -- the indices of
candidates whose mask overlaps the projected ground truth by at least 5% -- was already
computed by ``eval/score_cot.py`` and stored in ``<batch>/_scored/score.json``. Reusing it
means both arms are measured with **the same ruler**, so any difference can only come from
the answers themselves.

## What is reported

1. Accuracy for both arms on the shared subset (at least one selected candidate in `gt_ids`).
2. **In-pool disambiguation rate** -- restricted to questions where `gt_ids` is non-empty.
   Neither arm can possibly be right on a question whose pool lacks the answer, so including
   those depresses both curves equally and hides the real difference.
3. The disagreement matrix and a per-question disagreement list.
4. **Confidence calibration**: accuracy within each arm's own high/medium/low groups.
   Whether a model is genuinely more accurate when it says "high" decides whether its
   confidence field can be used for failure analysis at all -- the stratified multi-frame
   analysis depends on this being true.
5. Stratification by candidate count: questions with `n_cand <= 1` require no reasoning and
   are listed separately.
6. `kind` distribution -- in particular whether the 9B arm ever uses `merged_host` -- plus
   output length, truncation, and parse failures.

⚠️ The two arms use different prompts (the 9B arm gets the compact English rule set, the
frontier arm a longer version of the same rules). **This is not a pure model comparison**
and must not be reported as one.

    python code/task2/ablation/qwen_cot_cmp.py
"""
import os, sys, json, glob, argparse
from collections import Counter, defaultdict

_CODE_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, _CODE_ROOT)
from paths import ABLATION, SOLVED  # noqa: E402
QOUT = os.path.join(ABLATION, "qwen_cot")


def load_ref():
    """q -> the frontier arm's record, including gt_ids."""
    ref = {}
    for f in sorted(glob.glob(os.path.join(SOLVED, "batch*", "_scored", "score.json"))):
        for r in json.load(open(f)):
            ref[r["q"]] = r
    return ref


def load_qwen():
    q = {}
    for f in sorted(glob.glob(os.path.join(QOUT, "qwen_cot_s*.jsonl"))):
        for line in open(f):
            try:
                r = json.loads(line)
            except Exception:
                continue
            q[r["q"]] = r          # on duplicates, the last record wins
    return q


def rate(sub, key):
    return (100.0 * sum(r[key] for r in sub) / len(sub)) if sub else float("nan")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--list_diff", type=int, default=1, help="print the per-question disagreements")
    ap.add_argument("--max_list", type=int, default=25)
    args = ap.parse_args()

    ref, qw = load_ref(), load_qwen()
    keys = sorted(set(ref) & set(qw))
    if not keys:
        sys.exit("nothing comparable: check qwen_cot_s*.jsonl and _scored/score.json")

    only_q = sorted(set(qw) - set(ref))
    if only_q:
        print(f"[warn] {len(only_q)} questions have a 9B answer but no scored reference; skipped")

    rows = []
    for k in keys:
        a, b = ref[k], qw[k]
        gt = set(a["gt_ids"])
        pc, pq = set(a["pick"]), set(b.get("final") or [])
        rows.append(dict(
            q=k, text=a["text"], concept=a["concept"], n_cand=a["n_cand"],
            pool_ok=bool(a["pool_ok"]), gt_ids=sorted(gt),
            pick_c=sorted(pc), pick_q=sorted(pq),
            ok_c=bool(pc & gt), ok_q=bool(pq & gt),
            same=(pc == pq),
            conf_c=a.get("conf"), conf_q=b.get("confidence"),
            kind_c=a.get("kind"), kind_q=b.get("kind"),
            n_out=b.get("n_out", 0), trunc=bool(b.get("truncated")),
            fail=(b.get("final") is None)))

    n = len(rows)
    pool = [r for r in rows if r["pool_ok"]]
    triv = [r for r in rows if r["n_cand"] <= 1]
    hard = [r for r in rows if r["n_cand"] >= 2]

    print(f"\n{'='*74}")
    print(f"Qwen3.5-9B reasoning  vs  frontier LLM reasoning   -- {n} shared questions")
    print(f"{'='*74}")
    print(f"\n{'':<28}{'frontier':>10}{'Qwen':>10}{'delta':>8}")
    for name, sub in [("all questions", rows), ("in pool (gt_ids non-empty)", pool),
                      ("needs reasoning (cand>=2)", hard), ("trivial (cand<=1)", triv)]:
        if not sub:
            continue
        c, q = rate(sub, "ok_c"), rate(sub, "ok_q")
        print(f"  {name:<26}{c:>9.1f}%{q:>9.1f}%{q-c:>+8.1f}   n={len(sub)}")

    # ---- disagreement matrix ----
    both = sum(r["ok_c"] and r["ok_q"] for r in rows)
    conly = sum(r["ok_c"] and not r["ok_q"] for r in rows)
    qonly = sum(r["ok_q"] and not r["ok_c"] for r in rows)
    none = n - both - conly - qonly
    print(f"\n=== disagreement matrix ===")
    print(f"  both {both:>3}   frontier only {conly:>3}   Qwen only {qonly:>3}   neither {none:>3}")
    print(f"  identical id sets: {sum(r['same'] for r in rows)}/{n} "
          f"({100*sum(r['same'] for r in rows)/n:.1f}%)")

    # ---- confidence calibration ----
    print(f"\n=== confidence calibration (accuracy within each group) ===")
    for who, ck, ok in [("frontier", "conf_c", "ok_c"), ("Qwen    ", "conf_q", "ok_q")]:
        g = defaultdict(list)
        for r in rows:
            g[r[ck] or "?"].append(r)
        s = "  ".join(f"{c}:{len(v):>3}q {rate(v, ok):>5.1f}%"
                      for c, v in sorted(g.items(), key=lambda x: -len(x[1])))
        print(f"  {who}  {s}")
    print("  ^ if the high and medium groups score alike, that model's confidence field")
    print("    cannot be used for failure analysis")

    # ---- criterion types ----
    print(f"\n=== kind distribution ===")
    kc, kq = Counter(r["kind_c"] for r in rows), Counter(r["kind_q"] for r in rows)
    for k in sorted(set(kc) | set(kq), key=lambda x: -(kc[x] + kq[x])):
        print(f"  {str(k):<20}frontier {kc[k]:>3}   Qwen {kq[k]:>3}")

    # ---- output health ----
    outs = sorted(r["n_out"] for r in rows)
    print(f"\n=== Qwen output health ===")
    print(f"  length median {outs[len(outs)//2]}  max {outs[-1]}   "
          f"truncated {sum(r['trunc'] for r in rows)}  parse failures {sum(r['fail'] for r in rows)}")

    # ---- per-question disagreements ----
    if args.list_diff:
        for tag, sub in [("frontier only correct", [r for r in rows if r["ok_c"] and not r["ok_q"]]),
                         ("Qwen only correct", [r for r in rows if r["ok_q"] and not r["ok_c"]])]:
            if not sub:
                continue
            print(f"\n=== {tag} - {len(sub)} questions ===")
            for r in sub[:args.max_list]:
                print(f"  {r['q']:<26} GT{r['gt_ids']}  F{r['pick_c']}  Q{r['pick_q']}"
                      f"  ({r['conf_q']}/{r['kind_q']})")
                print(f"      {r['text'][:88]}")
            if len(sub) > args.max_list:
                print(f"  ... {len(sub)-args.max_list} more, see qwen_cot_cmp.json")

    os.makedirs(QOUT, exist_ok=True)
    out = os.path.join(QOUT, "qwen_cot_cmp.json")
    json.dump(rows, open(out, "w"), indent=1, ensure_ascii=False)
    print(f"\ndetail -> {out}")
    print("⚠️ Any report of these numbers must state that the two arms received different")
    print("   prompts, so this is not a pure model comparison.")


if __name__ == "__main__":
    main()
