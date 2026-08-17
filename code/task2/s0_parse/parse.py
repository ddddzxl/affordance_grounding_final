#!/usr/bin/env python3
"""Parse an instruction into a structured constraint graph.

## Four defects this schema fixes, all of them **missing fields** rather than parse quality

1. **Two sources of truth.** The previous schema's `target` was a generic word ("handle"),
   while the precise concept actually fed to the segmenter ("drawer handle") lived in a
   different file. `target.concept` is now the single source of truth.
2. **No host field.** The host had to be derived by stripping the last word, and
   `"power button" -> "power"` **is not an object** -- while the real host (the remote
   control) **is stated in the description**. `target.host` is now produced by language
   understanding, which needs no exception list of any kind.
3. **One `anchor` field carrying two roles.** It served both as "inside what does the ordinal
   count" (the container) and as "what should be visible in the same frame" (the framing
   reference). A table lamp is a good reference and a bad container -- the switch is not on
   the lamp. Now split into `entities[].role` and `relations[].rel`.
4. **No instanceability marker.** "wall" segments to something covering everything.
   `instanceable` is a **general property**, not a special case for one word: any noun that
   is not a countable object in an image is marked false.

## Coverage, measured over all 445 raw instructions

Expressible ~94%; honest residual ~6% (room-level or semantic localisation 23, colour-unique
~3, egocentric 1).

**Colour is deliberately not a field**: it appears in 18% of instructions but is the unique
cue in under 1%. That is a measurement, not an assumption.

## Carried over from the previous iteration, already verified

A closed enumeration plus constrained decoding: measured at zero parse failures, against 50%
failures for free generation.

The `affordance` field was **removed** -- it is a ground-truth label, which the parse stage
cannot and should not see.

    pip install lm-format-enforcer
    python code/task2/s0_parse/parse.py --n_desc 10 --out /tmp/p8.json      # smoke test
"""
import os, sys, json, argparse
import torch

_CODE_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, _CODE_ROOT)
from paths import PARSE, SCENEFUN3D  # noqa: E402
DATA = SCENEFUN3D
OUT_DEFAULT = os.path.join(PARSE, "parse.json")

_ROLE = {"type": "string", "enum": ["target", "host", "container", "landmark"]}
_REL = {"type": "string", "enum": ["contains", "on_top", "has_on_top", "next_to", "near",
                                   "left_of", "right_of", "above", "under", "behind",
                                   "in_front_of", "between"]}
_AXIS = {"type": "string", "enum": ["vertical", "horizontal", "ordinal"]}
_VAL = {"anyOf": [{"type": "string", "enum": ["top", "bottom", "left", "right", "middle"]},
                  {"type": "null"}]}

SCHEMA = {
    "type": "object", "additionalProperties": False,
    "required": ["target", "entities", "relations", "select", "residual"],
    "properties": {
        "target": {
            "type": "object", "additionalProperties": False,
            "required": ["concept", "host"],
            "properties": {
                "concept": {"type": "string"},
                "host": {"anyOf": [{"type": "string"}, {"type": "null"}]},
            },
        },
        "entities": {"type": "array", "items": {
            "type": "object", "additionalProperties": False,
            "required": ["name", "role", "instanceable"],
            "properties": {"name": {"type": "string"}, "role": _ROLE,
                           "instanceable": {"type": "boolean"}}}},
        "relations": {"type": "array", "items": {
            "type": "object", "additionalProperties": False,
            "required": ["rel", "a", "b"],
            "properties": {"rel": _REL, "a": {"type": "string"}, "b": {"type": "string"}}}},
        "select": {"type": "array", "items": {
            "type": "object", "additionalProperties": False,
            "required": ["on", "axis", "value", "index", "from"],
            "properties": {"on": {"type": "string"}, "axis": _AXIS, "value": _VAL,
                           "index": {"anyOf": [{"type": "integer"}, {"type": "null"}]},
                           "from": {"anyOf": [{"type": "string",
                                               "enum": ["top", "bottom", "left", "right"]},
                                              {"type": "null"}]}}}},
        "residual": {"anyOf": [{"type": "string"}, {"type": "null"}]},
    },
}

SYSTEM = """You convert ONE natural-language instruction (referring to a single interactable element in a 3D indoor scan) into a structured JSON graph. Output is FORCED to a JSON schema; choose the semantically correct value for every field.

KEYS
 target.concept : the precise noun phrase to segment with an open-vocabulary segmenter, e.g. "drawer handle", "door handle", "window handle", "light switch", "socket", "power button". Be specific: prefer "drawer handle" over "handle".
 target.host    : the object the target is physically mounted on / part of, if naming it helps ordering ("the second drawer"), else null.
                  "drawer handle"->"drawer";  "cabinet door handle"->"cabinet door";  "window handle"->"window";
                  "power button" of a remote -> "remote control";  "flush button" -> "toilet";
                  a wall light switch or a socket has no meaningful host -> null.
 entities[]     : EVERY physical noun that must be found in the image, listed once each.
                  role: target | host | container | landmark.  container = the furniture that the host/target is IN or ON.
                  instanceable = true if the noun denotes a countable object you could outline in a photo.
                  Set instanceable=false for non-object nouns: wall, floor, ceiling, room, bedroom, kitchen, corner, air.
 relations[]    : {"rel":..., "a":..., "b":...} between entity NAMES.
                  "contains": a physically contains/holds b  ("cabinet" contains "drawer").
                  "has_on_top": b sits on top of a           ("cabinet with the TV on top" -> a=cabinet, b=TV).
                  "on_top": a sits on top of b               ("lamp on the nightstand"     -> a=lamp,    b=nightstand).
                  "next_to"/"near"/"left_of"/"right_of"/"above"/"under"/"behind"/"in_front_of": a is <rel> b.
                  "between": emit TWO relations, a between b1 and a between b2.
 select[]       : which one to pick among candidates. "on" = the entity the ordering applies to
                  (use the HOST when there is one: "the second drawer" orders DRAWERS, not handles).
                  axis "vertical"  + value top|bottom|middle
                  axis "horizontal"+ value left|right|middle
                  axis "ordinal"   + index N + from top|bottom|left|right (null if unstated); value=null
                  Fields not used must be null.
 residual       : short note if something in the sentence cannot be expressed; else null.
                  RECORD ONLY — it drives no logic downstream.

RULES
 - IGNORE colour/material words (red, blue, white, wooden, glass...). They are never the only cue.
 - Room / semantic location ("bedroom door", "leads to the kitchen", "in the corner") is NOT groundable
   (needs global/room-level data we do not have). Do NOT special-case it: parse the sentence as if the room
   word were absent ("Close the bedroom door" -> target "door handle", host "door", no select), and note it
   in `residual`. Whatever instance we find is what we get.
 - Egocentric phrasing ("on your left when exiting") -> residual.
 - "X to the left of Y" is a RELATION (left_of); "the left X" is a SELECT (axis horizontal, value left). Do not confuse them.
 - If the sentence gives no disambiguating cue at all, select:[] and relations:[] are correct.
 - Never invent an entity that is not implied by the sentence."""

FEWSHOT = [
    ("Open the top left drawer of the cabinet with the TV on top",
     {"target": {"concept": "drawer handle", "host": "drawer"},
      "entities": [{"name": "drawer handle", "role": "target", "instanceable": True},
                   {"name": "drawer", "role": "host", "instanceable": True},
                   {"name": "cabinet", "role": "container", "instanceable": True},
                   {"name": "TV", "role": "landmark", "instanceable": True}],
      "relations": [{"rel": "contains", "a": "cabinet", "b": "drawer"},
                    {"rel": "has_on_top", "a": "cabinet", "b": "TV"}],
      "select": [{"on": "drawer", "axis": "vertical", "value": "top", "index": None, "from": None},
                 {"on": "drawer", "axis": "horizontal", "value": "left", "index": None, "from": None}],
      "residual": None}),
    ("Open the fifth drawer of the cabinet located to the left of the TV",
     {"target": {"concept": "drawer handle", "host": "drawer"},
      "entities": [{"name": "drawer handle", "role": "target", "instanceable": True},
                   {"name": "drawer", "role": "host", "instanceable": True},
                   {"name": "cabinet", "role": "container", "instanceable": True},
                   {"name": "TV", "role": "landmark", "instanceable": True}],
      "relations": [{"rel": "contains", "a": "cabinet", "b": "drawer"},
                    {"rel": "left_of", "a": "cabinet", "b": "TV"}],
      "select": [{"on": "drawer", "axis": "ordinal", "value": None, "index": 5, "from": None}],
      "residual": None}),
    ("Turn on the ceiling light using the switch next to the TV",
     {"target": {"concept": "light switch", "host": None},
      "entities": [{"name": "light switch", "role": "target", "instanceable": True},
                   {"name": "TV", "role": "landmark", "instanceable": True}],
      "relations": [{"rel": "next_to", "a": "light switch", "b": "TV"}],
      "select": [], "residual": None}),
    ("Plug the device in the left socket between the radiator and the closet",
     {"target": {"concept": "socket", "host": None},
      "entities": [{"name": "socket", "role": "target", "instanceable": True},
                   {"name": "radiator", "role": "landmark", "instanceable": True},
                   {"name": "closet", "role": "landmark", "instanceable": True}],
      "relations": [{"rel": "between", "a": "socket", "b": "radiator"},
                    {"rel": "between", "a": "socket", "b": "closet"}],
      "select": [{"on": "socket", "axis": "horizontal", "value": "left", "index": None, "from": None}],
      "residual": None}),
    ("Turn on the TV using the left remote on the nightstand",
     {"target": {"concept": "power button", "host": "remote control"},
      "entities": [{"name": "power button", "role": "target", "instanceable": True},
                   {"name": "remote control", "role": "host", "instanceable": True},
                   {"name": "nightstand", "role": "container", "instanceable": True}],
      "relations": [{"rel": "on_top", "a": "remote control", "b": "nightstand"}],
      "select": [{"on": "remote control", "axis": "horizontal", "value": "left",
                  "index": None, "from": None}],
      "residual": None}),
    ("Close the bedroom door",
     {"target": {"concept": "door handle", "host": "door"},
      "entities": [{"name": "door handle", "role": "target", "instanceable": True},
                   {"name": "door", "role": "host", "instanceable": True}],
      "relations": [], "select": [],
      "residual": "'bedroom' is a room-level locator, not groundable"}),
    ("Open the left window behind the shutters",
     {"target": {"concept": "window handle", "host": "window"},
      "entities": [{"name": "window handle", "role": "target", "instanceable": True},
                   {"name": "window", "role": "host", "instanceable": True},
                   {"name": "shutters", "role": "landmark", "instanceable": True}],
      "relations": [{"rel": "behind", "a": "window", "b": "shutters"}],
      "select": [{"on": "window", "axis": "horizontal", "value": "left", "index": None, "from": None}],
      "residual": None}),
    ("Second from the right closet door",
     {"target": {"concept": "door handle", "host": "closet door"},
      "entities": [{"name": "door handle", "role": "target", "instanceable": True},
                   {"name": "closet door", "role": "host", "instanceable": True},
                   {"name": "closet", "role": "container", "instanceable": True}],
      "relations": [{"rel": "contains", "a": "closet", "b": "closet door"}],
      "select": [{"on": "closet door", "axis": "ordinal", "value": None, "index": 2, "from": "right"}],
      "residual": None}),
]


def build_msgs(text):
    m = [{"role": "system", "content": SYSTEM}]
    for u, a in FEWSHOT:
        m += [{"role": "user", "content": u},
              {"role": "assistant", "content": json.dumps(a, ensure_ascii=False)}]
    m.append({"role": "user", "content": text})
    return m


def sanity(pj):
    """Read-only structural check; constrained decoding should make it unreachable.

    Returns a list of problems. **It reports, it never repairs** -- silently fixing a parse
    would hide the very failures this is here to surface.
    """
    bad = []
    names = {e["name"] for e in pj.get("entities", [])}
    if pj["target"]["concept"] not in names:
        bad.append("target.concept is not in entities")
    h = pj["target"].get("host")
    if h and h not in names:
        bad.append("target.host is not in entities")
    for r in pj.get("relations", []):
        for k in ("a", "b"):
            if r[k] not in names:
                bad.append(f"relation.{k}={r[k]!r} is not in entities")
    for s in pj.get("select", []):
        if s["on"] not in names:
            bad.append(f"select.on={s['on']!r} is not in entities")
        if s["axis"] == "ordinal" and s.get("index") is None:
            bad.append("ordinal select is missing index")
        if s["axis"] in ("vertical", "horizontal") and not s.get("value"):
            bad.append(f"{s['axis']} select is missing value")
    for e in pj.get("entities", []):
        if e["name"].lower() in {"wall", "floor", "ceiling", "room", "corner"} and e["instanceable"]:
            bad.append(f"{e['name']!r} should have instanceable=false")
    return bad


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", default="Qwen/Qwen3.5-9B")
    ap.add_argument("--out", default=OUT_DEFAULT)
    ap.add_argument("--visits", default=None)
    ap.add_argument("--n_desc", type=int, default=0, help="0 = all; >0 = smoke test")
    ap.add_argument("--max_new", type=int, default=420)
    args = ap.parse_args()
    os.makedirs(os.path.dirname(args.out), exist_ok=True)

    import transformers.tokenization_utils as _tu, transformers                    # noqa
    if not hasattr(_tu, "PreTrainedTokenizerBase"):                                # lm-format-enforcer shim
        _tu.PreTrainedTokenizerBase = transformers.PreTrainedTokenizerBase
    from transformers import AutoTokenizer, AutoModelForCausalLM
    from lmformatenforcer import JsonSchemaParser
    from lmformatenforcer.integrations.transformers import build_transformers_prefix_allowed_tokens_fn

    tok = AutoTokenizer.from_pretrained(args.model, trust_remote_code=True)
    model = AutoModelForCausalLM.from_pretrained(args.model, dtype=torch.bfloat16,
                                                 device_map="cuda", trust_remote_code=True).eval()
    prefix_fn = build_transformers_prefix_allowed_tokens_fn(tok, JsonSchemaParser(SCHEMA))

    visits = args.visits.split(",") if args.visits else \
        sorted(d for d in os.listdir(DATA) if d.isdigit())
    res = {"_meta": f"parse_v8 by {args.model}; schema=task2_v8_plan.md §2.2; "
                    f"constrained JSON decoding(lm-format-enforcer)"}
    n = nbad = 0
    for v in visits:
        f = f"{DATA}/{v}/{v}_descriptions.json"
        if not os.path.exists(f):
            continue
        res.setdefault(v, {})
        for d in json.load(open(f))["descriptions"]:
            if args.n_desc and n >= args.n_desc:
                break
            t = d["description"]
            # ⚠️ Recent transformers may return a BatchEncoding (dict-like) from
            #    apply_chat_template rather than a Tensor, and passing that straight to
            #    generate raises AttributeError on inputs_tensor.shape. Handle both.
            enc = tok.apply_chat_template(build_msgs(t), add_generation_prompt=True,
                                          return_tensors="pt")
            ids = enc["input_ids"] if hasattr(enc, "keys") else enc
            ids = ids.to("cuda")
            with torch.no_grad():
                out = model.generate(input_ids=ids, max_new_tokens=args.max_new, do_sample=False,
                                     prefix_allowed_tokens_fn=prefix_fn,
                                     pad_token_id=tok.eos_token_id)
            txt = tok.decode(out[0][ids.shape[1]:], skip_special_tokens=True).strip()
            try:
                pj = json.loads(txt)
            except Exception as ex:
                print(f"  [PARSE_FAIL] {v} {d['desc_id'][:8]} {ex}: {txt[:120]}", flush=True)
                res[v][d["desc_id"]] = {"text": t, "_fail": txt[:400]}; n += 1; nbad += 1; continue
            pj["text"] = t
            issues = sanity(pj)
            if issues:
                pj["_sanity"] = issues; nbad += 1
            res[v][d["desc_id"]] = pj
            n += 1
            print(f"  [{n:3d}] {v} {d['desc_id'][:8]} «{t[:44]}»"
                  f"{'  ⚠ ' + '; '.join(issues) if issues else ''}", flush=True)
        if args.n_desc and n >= args.n_desc:
            break
    json.dump(res, open(args.out, "w"), indent=1, ensure_ascii=False)
    print(f"\n[parse] {n} instructions, {nbad} with sanity issues -> {args.out}")


if __name__ == "__main__":
    main()
