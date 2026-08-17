#!/usr/bin/env python3
"""Run the reasoning stage with Qwen3.5-9B on **exactly the same input**, as the scripted
counterpart to the frontier-LLM arm.

This is the fully automated arm of the model-scale ablation. The frontier arm was executed
interactively (see REPORT.md section 3); this script is what makes the comparison a
comparison rather than an anecdote.

## Three things that must match for the comparison to be fair

1. **Identical input**: the same `candidates.txt`. No regenerated questions, no different
   frame selection.
2. **Identical rules**: the same rule specification as the system prompt. Those rules were
   distilled from observed failures, and withholding them would turn the experiment into
   "designer versus executor" rather than a comparison of models.
3. **Identical scoring**: the output is written as a standard answer.json and goes through
   the same scoring script.

## Known failure modes, each explicitly guarded -- all are reported in the log, never silent

- **Context truncation.** The model's limit is far above our worst case of roughly 8k
  tokens, but the actual input token count is printed and warned on regardless.
- **Output cut off by max_new_tokens.** The thinking trace can be very long. After
  generating, check whether it ended on eos; if not, mark `truncated=True`. Those samples
  are counted separately and never folded into the accuracy figure.
- **JSON parse failure.** The model may wrap the object in prose or in a fenced block. The
  extractor takes the *last* complete JSON object; on failure the record is marked
  `parse_fail` and, again, counted separately.
- **Out-of-range ids.** The most common semantic error is answering with a host or container
  index. Every id in `final` is checked against the candidate count for that question's
  **target concept**; out-of-range answers are recorded as `oob` and emptied.
- **Thinking leaking into the answer.** JSON extraction only looks after `</think>`, so a
  JSON object drafted mid-reasoning cannot be mistaken for the answer.

## Sharding

`--shard i --nshard N` partitions by question index modulo N. **Never hard-code
CUDA_VISIBLE_DEVICES in the script** -- the scheduler has already set it from the resource
request, and overwriting it lands the job on someone else's GPU. Use `--device cuda:i` to
index within the allocation.

    python code/task2/s3_reasoning/qwen_cot.py --limit 3 --dry_run   # prompt only, no model
    python code/task2/s3_reasoning/qwen_cot.py --limit 8             # smoke test
"""
import os, sys, json, glob, re, argparse, datetime

_CODE_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, _CODE_ROOT)
from paths import ABLATION, CANDIDATES, PROJECT_ROOT, SOLVED  # noqa: E402

# The compact English rule set, which is also what docs/reasoning_rules.md publishes.
# English additionally has a token advantage over the longer prose version of the same rules.
RULES_EN = os.path.join(PROJECT_ROOT, "docs", "reasoning_rules.md")
OUT = os.path.join(ABLATION, "qwen_cot")

def extract_json(text):
    """Pull the last complete JSON object out of the model output.

    Tolerates the three common shapes: a fenced ```json block, bare JSON, and JSON with
    prose wrapped around it. It takes the **last** one because the model sometimes writes
    an example before the real answer.
    """
    if not text:
        return None
    # Fallback: scan for balanced {...} spans and try them from the end backwards
    if blocks:
        for b in reversed(blocks):
            try:
                return json.loads(b)
            except Exception:
                pass
    # Fallback: scan for balanced {...} spans and try them from the end backwards
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
            if isinstance(o, dict) and "final" in o:
                return o
        except Exception:
            pass
    return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", default="Qwen/Qwen3.5-9B")
    ap.add_argument("--dump", default="candidates")
    # Do NOT set CUDA_VISIBLE_DEVICES here; the scheduler's allocation is already mapped
    # onto cuda:0..N-1, and overwriting it lands the job on someone else's GPU.
    ap.add_argument("--device", default="cuda:0")
    ap.add_argument("--shard", type=int, default=0)
    ap.add_argument("--nshard", type=int, default=1)
    ap.add_argument("--limit", type=int, default=0,
                    help="first N questions. **Biased** -- smoke tests only")
    ap.add_argument("--sample", type=int, default=0,
                    help="random N questions for the ablation. All 445 is impractical "
                         "(20+ hours on one GPU) and the comparison only needs enough "
                         "statistical power -- 150 questions gives a 95%% CI of about +/-8%%")
    ap.add_argument("--seed", type=int, default=20260807)
    ap.add_argument("--brief", type=int, default=1,
                    help="prepend a brevity reminder to the user message. The rule file "
                         "already has a Style section; this repeats it closer to the "
                         "generation point, which measurably matters -- see below")
    ap.add_argument("--max_new", type=int, default=16384,
                    help="this model's thinking traces are very long: even questions it "
                         "answers correctly take 6900-7600 tokens, because it enumerates "
                         "every candidate's coordinates, mirroring the style of the worked "
                         "examples in the rule file. 3072 and 10240 both truncate; 16384 does not")
    ap.add_argument("--thinking", type=int, default=1)
    # ⚠️ **Do not use greedy decoding.** With do_sample=False this model gets stuck in a
    #    self-doubt loop: "So 1:5,2:9,3:6,4:2. / Wait, drawer 6 vs drawer 2... / So
    #    1:5,2:9,3:6,4:2. / Wait,..." repeating until it hits max_new_tokens. Sampling is
    #    also what the model authors recommend for thinking mode.
    ap.add_argument("--temperature", type=float, default=0.6)
    ap.add_argument("--top_p", type=float, default=0.95)
    ap.add_argument("--top_k", type=int, default=20)
    ap.add_argument("--rep_penalty", type=float, default=1.05,
                    help="a second guard against repeated spans")
    ap.add_argument("--warn_tok", type=int, default=30000, help="warn above this input size")
    ap.add_argument("--dry_run", action="store_true",
                    help="print the prompt and token count only; do not load the model")
    ap.add_argument("--resume", type=int, default=1)
    args = ap.parse_args()
    SRC = CANDIDATES if args.dump == "candidates" else os.path.join(os.path.dirname(CANDIDATES), args.dump)
    os.makedirs(OUT, exist_ok=True)

    # The question list is the 445 that already have a reference answer, so every one is comparable
    qs = sorted(os.path.basename(d) for d in glob.glob(os.path.join(SOLVED, "batch*", "q*_*"))
                if os.path.exists(os.path.join(d, "answer.json")))
    if args.sample:
        import random
        rnd = random.Random(args.seed)
        qs = sorted(rnd.sample(qs, min(args.sample, len(qs))))
    qs = [q for i, q in enumerate(qs) if i % args.nshard == args.shard]
    if args.limit:
        qs = qs[:args.limit]
    ckpt = os.path.join(OUT, f"qwen_cot_s{args.shard}.jsonl")
    done = set()
    if args.resume and os.path.exists(ckpt):
        for line in open(ckpt):
            try:
                done.add(json.loads(line)["q"])
            except Exception:
                pass
        print(f"[resume] {len(done)} questions already done")
    sysmsg = open(RULES_EN).read()
    # ⚠️ This reminder **must** go at the start of the user message, not at the end of the
    #    system prompt. The rule file runs to 8000 characters of worked coordinate-by-
    #    coordinate analysis, and the model imitates that style; a "be brief" line buried at
    #    the tail of the system prompt does not counteract it (measured: still 6900-7600
    #    tokens of output).
    BRIEF = ("[Reminder] Three short steps: region -> host -> target. Around 150 words.\n"
             "Don't list every candidate's coordinates; don't re-check a conclusion you\n"
             "already reached.\n\n---\n\n")

    from transformers import AutoTokenizer
    tok = AutoTokenizer.from_pretrained(args.model)
    model = None
    if not args.dry_run:
        import torch
        from transformers import AutoModelForCausalLM
        try:
            from transformers import Qwen3_5ForConditionalGeneration as Cls
        except Exception:
            Cls = AutoModelForCausalLM
        print(f"[load] {args.model}  ({Cls.__name__})", flush=True)
        model = Cls.from_pretrained(args.model, dtype=torch.bfloat16, device_map=args.device)
        model.eval()

    fh = open(ckpt, "a")
    n_ok = n_trunc = n_pfail = n_oob = 0
    for j, k in enumerate(qs):
        if k in done:
            continue
        ct = os.path.join(SRC, k, "candidates.txt")
        mf = os.path.join(SRC, k, "meta.json")
        if not (os.path.exists(ct) and os.path.exists(mf)):
            continue
        m = json.load(open(mf))
        tgt = m["parse"]["target"]["concept"]
        ncand = len(m.get("candidates", {}).get(tgt, []) or [])
        umsg = (BRIEF if args.brief else "") + open(ct).read()
        msgs = [{"role": "system", "content": sysmsg},
                {"role": "user", "content": umsg}]
        text = tok.apply_chat_template(msgs, tokenize=False, add_generation_prompt=True,
                                       enable_thinking=bool(args.thinking))
        ids = tok(text, return_tensors="pt")
        n_in = ids["input_ids"].shape[1]
        if n_in > args.warn_tok:
            print(f"  ⚠️ {k}: input {n_in} tok exceeds {args.warn_tok}", flush=True)
        if args.dry_run:
            if j == 0:
                print("=" * 80); print(text[:1500]); print("..."); print("=" * 80)
            print(f"  {k:<28} input {n_in:>6} tok   candidates {ncand}")
            continue

        import torch
        torch.manual_seed(args.seed + j)      # sampling is stochastic; seed for reproducibility
        with torch.no_grad():
            out = model.generate(**{kk: v.to(model.device) for kk, v in ids.items()},
                                 max_new_tokens=args.max_new,
                                 do_sample=True, temperature=args.temperature,
                                 top_p=args.top_p, top_k=args.top_k,
                                 repetition_penalty=args.rep_penalty,
                                 pad_token_id=tok.pad_token_id or tok.eos_token_id)
        gen = out[0][n_in:]
        # Truncation test: not ending on eos means it hit max_new_tokens
        truncated = bool(gen.shape[0] >= args.max_new and gen[-1].item() != (tok.eos_token_id or -1))
        raw = tok.decode(gen, skip_special_tokens=True)
        # Take only what follows </think>, so JSON drafted mid-reasoning is not mistaken for the answer
        body = raw.split("</think>")[-1] if "</think>" in raw else raw
        obj = extract_json(body)
        rec = dict(q=k, n_in=n_in, n_out=int(gen.shape[0]), truncated=truncated,
                   raw_tail=raw[-400:])
        if obj is None:
            rec.update(parse_fail=True, final=None); n_pfail += 1
        else:
            fin = obj.get("final")
            if not isinstance(fin, list) or any(not isinstance(x, int) for x in fin):
                rec.update(parse_fail=True, final=None, bad_final=repr(fin)[:80]); n_pfail += 1
            else:
                oob = [i for i in fin if i < 0 or i >= ncand]
                if oob:
                    rec.update(oob=oob, final=[], confidence=obj.get("confidence"),
                               kind=obj.get("kind"), note=obj.get("note")); n_oob += 1
                else:
                    rec.update(final=fin, confidence=obj.get("confidence"),
                               kind=obj.get("kind"), note=obj.get("note")); n_ok += 1
        n_trunc += truncated
        fh.write(json.dumps(rec, ensure_ascii=False) + "\n"); fh.flush()
        flag = ("truncated " if truncated else "") \
               + ("parse-fail " if rec.get("parse_fail") else "") \
               + (f"oob{rec.get('oob')} " if rec.get("oob") else "")
        print(f"  [{j+1}/{len(qs)}] {k:<28} in={n_in:>5} out={rec['n_out']:>4} "
              f"final={rec.get('final')}  {flag}", flush=True)

    if args.dry_run:
        print("\n[dry_run] model was not loaded."); return
    tot = n_ok + n_pfail + n_oob
    print(f"\n{'='*70}\n[shard {args.shard}] finished {tot} questions")
    print(f"  answered normally  {n_ok}")
    print(f"  parse failures     {n_pfail}   <- not counted as wrong; tallied separately")
    print(f"  out-of-range ids   {n_oob}   <- answered with a host/container index")
    print(f"  output truncated   {n_trunc}   <- if >0, raise --max_new")
    print(f"\ncheckpoint -> {ckpt}")


if __name__ == "__main__":
    main()
