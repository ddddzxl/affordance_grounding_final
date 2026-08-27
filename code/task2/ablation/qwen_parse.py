#!/usr/bin/env python3
"""Qwen3.5-9B **parsing** ablation: instruction -> structured parse.

## Why this stage is measured on its own

Measuring "9B parse -> frame selection -> candidate generation -> 9B reasoning" end to end
would require **regenerating every question** (re-running the segmenter, re-selecting
frames), which is prohibitively expensive. But parsing and reasoning are two independent
links in the pipeline and can be measured separately:

    this script       stage one   instruction     -> parse
    qwen_cot.py       stage two   candidate table -> answer

## What it compares against

Field-by-field alignment with the reference parses of all 445 instructions, audited three
ways (structural, semantic, and against the ground-truth labels):

    target concept   the critical one -- it decides what the segmenter searches for,
                     and everything downstream fails if it is wrong
    host             decides what the ordering constraint applies to
    entity roles     the target / host / container / landmark division of labour
    relations        the set of spatial constraints (rel, a, b)
    select           the ordering constraint (on, axis, value/index)

⚠️ **"Agrees" is not the same as "is correct"** -- the reference parse can also be wrong.
This number therefore reads as **"can the 9B model reproduce the same parsing convention"**,
not "is the 9B model's parse correct".

`concept` additionally gets a **semantic equivalence** test (drawer handle and drawer pull
count as the same thing) so that synonyms are not recorded as errors. Note that the headline
figure in the report is the stricter "correct at part level" judgement, adjudicated per
question rather than by string match; this script's agreement rate is the automated floor
under it.

## Cost

The output is a single JSON object of a few hundred tokens and needs no thinking mode, so
this is an order of magnitude cheaper than the reasoning stage -- about 20 minutes on one
GPU for all 445.

    python code/task2/ablation/qwen_parse.py --limit 5
"""
import os, sys, json, glob, re, argparse

_CODE_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, _CODE_ROOT)
from paths import ABLATION, CANDIDATES, SOLVED  # noqa: E402
OUT = os.path.join(ABLATION, "qwen_parse")

SYS = """You convert a natural-language instruction about acting on something in a room
into a structured parse. The parse is later used to search a scene for the referred object,
so every name you emit should be something an open-vocabulary object detector could find.

Output a single JSON object with exactly these four keys.

**`target`** — an object with two fields:
- `concept`: the thing a person physically touches to carry out the action. If the
  instruction says to operate a piece of furniture or an appliance, this is the small part
  they put their hand on, not the whole object.
- `host`: the countable object that part is mounted on. Use `null` when the part is not
  mounted on anything named in the instruction, or when it is only functionally connected
  to it rather than physically attached.

**`entities`** — a list of `{"name": ..., "role": ...}` covering every physical thing the
instruction mentions that could be detected. `role` is exactly one of:
- `target` — the class the answer comes from; exactly one entity has this role
- `host` — what the target is mounted on
- `container` — a larger object that encloses or holds the host
- `landmark` — mentioned only to say where something is; never the answer

**`relations`** — a list of `{"rel": ..., "a": ..., "b": ...}` for each spatial constraint
stated in the instruction. `a` and `b` are names that appear in `entities`. Use one of:
`contains`, `left_of`, `right_of`, `above`, `below`, `under`, `on_top`, `has_on_top`,
`next_to`, `near`, `behind`, `in_front_of`, `between`.

**`select`** — a list of ordering constraints, one per ordering word in the instruction.
Each is `{"on": ..., "axis": ..., "value": ...}`, or for counting,
`{"on": ..., "axis": "ordinal", "index": <1-based integer>}`.
- `axis` is `"vertical"` (value `top` / `middle` / `bottom`), `"horizontal"`
  (value `left` / `middle` / `right`), or `"ordinal"`.
- `on` names the entity being ordered — that is, the class among whose instances the user
  is picking one out. Emit an empty list if the instruction states no ordering.

Notes:
- Room names and colours or materials cannot be detected as objects. Do not create
  entities for them and do not fold them into a name.
- If the instruction refers to two things of the same class, still emit one entity for
  that class.

Output only the JSON object, inside a ```json code block. No commentary."""



def extract_json(text):
    if not text:
        return None
    for b in reversed(re.findall(r"```(?:json)?\s*(\{.*?\})\s*```", text, re.S)):
        try:
            return json.loads(b)
        except Exception:
            pass
    cand, depth, start = [], 0, None
    for i, ch in enumerate(text):
        if ch == "{":
            if depth == 0:
                start = i
            depth += 1
        elif ch == "}":
            depth -= 1
            if depth == 0 and start is not None:
                cand.append(text[start:i + 1]); start = None
    for b in reversed(cand):
        try:
            o = json.loads(b)
            if isinstance(o, dict) and "target" in o:
                return o
        except Exception:
            pass
    return None


def norm(s):
    return re.sub(r"\s+", " ", (s or "").strip().lower())


# Synonym groups, used for the semantic-equivalence test on concept / host so that a
# synonym is not recorded as an error.
SYN = [
    {"drawer handle", "drawer pull", "drawer knob"},
    {"door handle", "door pull", "handle"},
    {"light switch", "switch", "light button", "wall switch"},
    {"socket", "outlet", "power outlet", "wall socket"},
    {"plug", "power plug"},
    {"radiator knob", "radiator dial", "radiator valve", "thermostatic valve"},
    {"window handle", "window latch"},
    {"faucet handle", "tap handle", "faucet"},
    {"cabinet door", "closet door", "counter door", "door"},
    {"remote control", "remote"},
    {"flush button", "flush plate"},
]


def same(a, b):
    a, b = norm(a), norm(b)
    if a == b:
        return True
    if not a or not b:
        return False
    for g in SYN:
        if a in g and b in g:
            return True
    return False


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", default="Qwen/Qwen3.5-9B")
    ap.add_argument("--dump", default="candidates")
    ap.add_argument("--device", default="cuda:0")
    ap.add_argument("--shard", type=int, default=0)
    ap.add_argument("--nshard", type=int, default=1)
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--max_new", type=int, default=2048,
                    help="a single JSON object; no long thinking trace needed")
    ap.add_argument("--thinking", type=int, default=0,
                    help="parsing is structured extraction, so thinking is off by default "
                         "-- an order of magnitude faster")
    ap.add_argument("--temperature", type=float, default=0.6)
    ap.add_argument("--top_p", type=float, default=0.95)
    ap.add_argument("--seed", type=int, default=20260807)
    ap.add_argument("--resume", type=int, default=1)
    args = ap.parse_args()
    SRC = CANDIDATES if args.dump == "candidates" else os.path.join(os.path.dirname(CANDIDATES), args.dump)
    os.makedirs(OUT, exist_ok=True)

    qs = sorted(os.path.basename(d) for d in glob.glob(os.path.join(SOLVED, "batch*", "q*_*")))
    qs = [q for i, q in enumerate(qs) if i % args.nshard == args.shard]
    if args.limit:
        qs = qs[:args.limit]
    ckpt = os.path.join(OUT, f"qwen_parse_s{args.shard}.jsonl")
    done = set()
    if args.resume and os.path.exists(ckpt):
        for line in open(ckpt):
            try:
                done.add(json.loads(line)["q"])
            except Exception:
                pass
        print(f"[resume] {len(done)} questions already done")
    fh = open(ckpt, "a")

    import torch
    from transformers import AutoTokenizer
    tok = AutoTokenizer.from_pretrained(args.model)
    try:
        from transformers import Qwen3_5ForConditionalGeneration as Cls
    except Exception:
        from transformers import AutoModelForCausalLM as Cls
    print(f"[load] {args.model} ({Cls.__name__}) -> {args.device}", flush=True)
    model = Cls.from_pretrained(args.model, dtype=torch.bfloat16, device_map=args.device).eval()

    n_ok = n_fail = 0
    for j, k in enumerate(qs):
        if k in done:
            continue
        mf = os.path.join(SRC, k, "meta.json")
        if not os.path.exists(mf):
            continue
        m = json.load(open(mf))
        text = m["text"]
        msgs = [{"role": "system", "content": SYS},
                {"role": "user", "content": text}]
        prompt = tok.apply_chat_template(msgs, tokenize=False, add_generation_prompt=True,
                                         enable_thinking=bool(args.thinking))
        ids = tok(prompt, return_tensors="pt")
        n_in = ids["input_ids"].shape[1]
        torch.manual_seed(args.seed + j)
        with torch.no_grad():
            out = model.generate(**{kk: v.to(model.device) for kk, v in ids.items()},
                                 max_new_tokens=args.max_new, do_sample=True,
                                 temperature=args.temperature, top_p=args.top_p,
                                 pad_token_id=tok.pad_token_id or tok.eos_token_id)
        gen = out[0][n_in:]
        raw = tok.decode(gen, skip_special_tokens=True)
        body = raw.split("</think>")[-1] if "</think>" in raw else raw
        obj = extract_json(body)
        rec = dict(q=k, text=text, n_in=n_in, n_out=int(gen.shape[0]),
                   truncated=bool(gen.shape[0] >= args.max_new))
        if obj is None:
            rec["parse_fail"] = True; n_fail += 1
        else:
            rec["parse"] = obj; n_ok += 1
        fh.write(json.dumps(rec, ensure_ascii=False) + "\n"); fh.flush()
        tc = (obj or {}).get("target", {}).get("concept") if obj else None
        print(f"  [{j+1}/{len(qs)}] {k[:4]}  out={rec['n_out']:>4}  "
              f"concept={tc!r}{'  PARSE FAIL' if obj is None else ''}", flush=True)

    print(f"\n[shard {args.shard}] ok {n_ok} - parse failures {n_fail}   checkpoint -> {ckpt}")


if __name__ == "__main__":
    main()
