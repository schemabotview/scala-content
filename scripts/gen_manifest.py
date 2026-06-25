#!/usr/bin/env python3
"""Generate scala-content/manifest.json. Pulls exact `## ` headings from each
notebook (dropping "What's covered" / "What's next"), pairs them in order with a
hand-authored (scene, spine, highlight, focus, role) row, and emits the manifest.
SS runs sequentially over the wired sections, matching java-content's convention.
The tts/audio stem = f"{NN}-{SS}-{slug(heading)}"."""
import json, re
from pathlib import Path

NB_DIR = Path.home() / "Projects/scala"
OUT = Path("/Users/maddipotiganesh/Products/scala-content/manifest.json")
DROP = {"what's covered", "what's next"}

def slug(s: str) -> str:
    s = s.lower().replace("`", "")
    s = re.sub(r"[^a-z0-9]+", "-", s).strip("-")
    s = re.sub(r"-+", "-", s)
    # cap at ~42 chars on a word boundary
    if len(s) > 42:
        cut = s[:42].rsplit("-", 1)[0]
        s = cut or s[:42]
    return s.strip("-")

def headings(stem: str):
    nb = json.load(open(NB_DIR / f"{stem}.ipynb"))
    out = []
    for c in nb["cells"]:
        if c["cell_type"] != "markdown":
            continue
        for line in c["source"]:
            t = line.rstrip("\n")
            if t.startswith("## ") and not t.startswith("### "):
                out.append(t[3:].strip())
    return [h for h in out if h.strip().lower().rstrip(".") not in DROP]

# (scene, spine, [highlight...], [focus...], role|None) per wired section, in order.
J = "scala-jvm"; A = "scala-anatomy"
MAP = {
"01-intro-and-setup": (J, [
  (J, True,  [], [], "hook"),
  (J, True,  ["sc-classloader-subsystem","sc-exec-engine"], ["sc-top","sc-bottom"], None),
  (J, True,  ["scalac","sc-source-code"], ["sc-pipeline"], None),
  (J, True,  ["sc-source-code","scalac","sc-class-file","sc-interpreter","sc-jit-compiler","sc-gc"], ["sc-top","sc-bottom"], None),
  (J, True,  ["sc-class-file","sc-classloader-subsystem"], ["sc-classloader-subsystem"], None),
  (J, False, ["sc-exec-engine"], ["sc-bottom"], None),
  (J, False, ["scalac"], ["sc-pipeline"], None),
  (J, True,  ["sc-pipeline"], ["sc-pipeline"], None),
  (J, False, ["sc-interpreter"], ["sc-exec-engine"], None),
  (J, False, ["sc-source-code","scalac","sc-class-file"], ["sc-pipeline"], None),
  (J, False, ["sc-class-file"], ["sc-pipeline"], None),
  (J, True,  ["sc-source-code"], ["sc-pipeline"], None),
  (J, False, ["sc-source-code"], ["sc-pipeline"], None),
  (J, True,  ["sc-classloader-subsystem","sc-exec-engine"], ["sc-top","sc-bottom"], None),
]),
"02-values-types-and-expressions": (A, [
  (A, True,  ["sa-bind-val","sa-bind-var"], ["sa-kind"], "hook"),
  (A, True,  ["sa-bind-lazy"], ["sa-kind"], None),
  (A, True,  ["sa-type","sa-primitive"], ["sa-type"], None),
  (A, True,  ["sa-name","sa-type"], ["sa-init-row"], None),
  (A, False, ["sa-type"], ["sa-type"], None),
  (A, True,  ["sa-primitive"], ["sa-type"], None),
  (A, False, ["sa-value-primitive","sa-primitive"], ["sa-value"], None),
  (A, False, ["sa-primitive"], ["sa-type"], None),
  (A, False, ["sa-type"], ["sa-type"], None),
  (A, True,  ["sa-ctrl-expr","sa-control"], ["sa-verbs"], None),
  (A, False, ["sa-loop-while"], ["sa-loops"], None),
  (A, True,  ["sa-method-call"], ["sa-methods"], None),
  (A, False, ["sa-type"], ["sa-init-row"], None),
]),
"03-functions-and-methods": (A, [
  (A, True,  ["sa-bind-def","sa-method-def"], ["sa-methods"], "hook"),
  (A, True,  ["sa-fn-lambda"], ["sa-functions"], None),
  (A, True,  ["sa-method-def","sa-fn-lambda"], ["sa-methods","sa-functions"], None),
  (A, True,  ["sa-fn-hof"], ["sa-functions"], None),
  (A, True,  ["sa-fn-lambda"], ["sa-functions"], None),
  (A, False, ["sa-method-def"], ["sa-methods"], None),
  (A, False, ["sa-method-def"], ["sa-methods"], None),
  (A, False, ["sa-fn-hof","sa-method-def"], ["sa-functions"], None),
  (A, False, ["sa-method-def"], ["sa-methods"], None),
  (A, False, ["sa-method-def"], ["sa-methods"], None),
  (A, True,  ["sa-fn-lambda","sa-fn-closure"], ["sa-functions"], None),
  (A, False, ["sa-method-def"], ["sa-methods"], None),
  (A, False, ["sa-method-def"], ["sa-methods"], None),
]),
"04-collections": (A, [
  (A, True,  ["sa-type-coll"], ["sa-type"], "hook"),
  (A, True,  ["sa-type-coll"], ["sa-type"], None),
  (A, True,  ["sa-hamt"], ["sa-memory"], None),
  (A, True,  ["sa-coll-list"], ["sa-type-coll"], None),
  (A, True,  ["sa-coll-vector"], ["sa-type-coll"], None),
  (A, True,  ["sa-coll-set"], ["sa-type-coll"], None),
  (A, True,  ["sa-coll-map"], ["sa-type-coll"], None),
  (A, False, ["sa-array"], ["sa-type"], None),
  (A, False, ["sa-tuple"], ["sa-type"], None),
  (A, True,  ["sa-type-coll"], ["sa-type"], None),
  (A, True,  ["sa-coll-ops"], ["sa-verbs"], None),
  (A, True,  ["sa-op-map","sa-op-filter","sa-op-flatmap"], ["sa-coll-ops"], None),
  (A, True,  ["sa-op-fold"], ["sa-coll-ops"], None),
  (A, True,  ["sa-op-groupby"], ["sa-coll-ops"], None),
  (A, False, ["sa-op-filter"], ["sa-coll-ops"], None),
  (A, True,  ["sa-op-zip"], ["sa-coll-ops"], None),
  (A, False, ["sa-coll-ops"], ["sa-coll-ops"], None),
  (A, False, ["sa-coll-ops"], ["sa-coll-ops"], None),
  (A, False, ["sa-op-map","sa-op-filter"], ["sa-coll-ops"], None),
  (A, True,  ["sa-loop-for","sa-loop-desugar"], ["sa-loops"], None),
  (A, False, ["sa-coll-ops"], ["sa-coll-ops"], None),
  (A, False, ["sa-coll-ops"], ["sa-coll-ops"], None),
]),
"05-oop-classes-traits-case-classes-enums": (A, [
  (A, True,  ["sa-class"], ["sa-type-oop"], "hook"),
  (A, False, ["sa-method-def"], ["sa-type-oop"], None),
  (A, True,  ["sa-object"], ["sa-type-oop"], None),
  (A, True,  ["sa-class","sa-object","sa-bind-def"], ["sa-type-oop"], None),
  (A, True,  ["sa-trait"], ["sa-type-oop"], None),
  (A, True,  ["sa-oop-mammal","sa-oop-walker"], ["sa-model"], None),
  (A, False, ["sa-oop-animal","sa-trait"], ["sa-model"], None),
  (A, True,  ["sa-case-class"], ["sa-type-oop"], None),
  (A, False, ["sa-case-class","sa-new-coll"], ["sa-type-oop"], None),
  (A, False, ["sa-object","sa-case-class"], ["sa-type-oop"], None),
  (A, True,  ["sa-enum","sa-adt"], ["sa-type-oop"], None),
  (A, False, ["sa-enum"], ["sa-type-oop"], None),
  (A, False, ["sa-adt","sa-trait","sa-case-class"], ["sa-type-oop"], None),
  (A, True,  ["sa-pat-match"], ["sa-pattern"], None),
]),
"06-pattern-matching-option-try-either": (A, [
  (A, True,  ["sa-pat-match"], ["sa-pattern"], "hook"),
  (A, True,  ["sa-pat-match","sa-pat-unapply"], ["sa-pattern"], None),
  (A, True,  ["sa-pat-unapply","sa-case-class"], ["sa-pattern"], None),
  (A, False, ["sa-pat-unapply","sa-tuple"], ["sa-pattern"], None),
  (A, False, ["sa-ctrl-guard"], ["sa-control"], None),
  (A, False, ["sa-pat-unapply","sa-loop-for"], ["sa-pattern"], None),
  (A, True,  ["sa-adt","sa-pat-match"], ["sa-pattern"], None),
  (A, False, ["sa-pat-match","sa-fn-lambda"], ["sa-pattern"], None),
  (A, True,  ["sa-typed-failure"], ["sa-results"], None),
  (A, True,  ["sa-typed-failure","sa-op-map","sa-op-flatmap"], ["sa-results"], None),
  (A, True,  ["sa-typed-failure"], ["sa-results"], None),
  (A, True,  ["sa-typed-failure"], ["sa-results"], None),
  (A, True,  ["sa-loop-for","sa-typed-failure"], ["sa-loops"], None),
  (A, False, ["sa-typed-failure"], ["sa-results"], None),
]),
"07-generics-variance-advanced-types": (A, [
  (A, True,  ["sa-generic"], ["sa-type"], "hook"),
  (A, True,  ["sa-generic"], ["sa-type"], None),
  (A, True,  ["sa-generic","sa-coll-list"], ["sa-type"], None),
  (A, False, ["sa-generic"], ["sa-type"], None),
  (A, False, ["sa-generic"], ["sa-type"], None),
  (A, True,  ["sa-generic","sa-method-area"], ["sa-memory"], None),
  (A, False, ["sa-type","sa-generic"], ["sa-type"], None),
  (A, False, ["sa-type","sa-trait"], ["sa-type"], None),
  (A, True,  ["sa-adt","sa-type"], ["sa-type"], None),
  (A, False, ["sa-type","sa-pat-match"], ["sa-type"], None),
  (A, False, ["sa-type"], ["sa-type"], None),
  (A, False, ["sa-trait","sa-oop-mammal"], ["sa-model"], None),
  (A, False, ["sa-type"], ["sa-type"], None),
  (A, True,  ["sa-generic","sa-type"], ["sa-type"], None),
]),
"08-givens-and-extensions": (A, [
  (A, True,  ["sa-method-def"], ["sa-init-row"], "hook"),
  (A, True,  ["sa-method-def","sa-kind"], ["sa-init-row"], None),
  (A, True,  ["sa-bind-val","sa-value-object"], ["sa-init-row"], None),
  (A, False, ["sa-type-oop"], ["sa-init-row"], None),
  (A, True,  ["sa-trait","sa-generic"], ["sa-type"], None),
  (A, False, ["sa-method-call"], ["sa-methods"], None),
  (A, True,  ["sa-method-def","sa-method-call"], ["sa-methods"], None),
  (A, False, ["sa-method-def","sa-trait"], ["sa-methods"], None),
  (A, False, ["sa-generic"], ["sa-type"], None),
  (A, False, ["sa-method-def"], ["sa-methods"], None),
  (A, False, ["sa-value-object"], ["sa-value"], None),
  (A, False, ["sa-trait","sa-generic"], ["sa-type"], None),
  (A, False, ["sa-method-def"], ["sa-init-row"], None),
]),
"09-concurrency-and-error-handling": (A, [
  (A, True,  ["sa-typed-failure"], ["sa-results"], "hook"),
  (A, True,  ["sa-stack","sa-heap"], ["sa-memory"], None),
  (A, True,  ["sa-op-map","sa-op-flatmap","sa-typed-failure"], ["sa-coll-ops"], None),
  (A, True,  ["sa-loop-for"], ["sa-loops"], None),
  (A, False, ["sa-op-map","sa-typed-failure"], ["sa-coll-ops"], None),
  (A, False, ["sa-typed-failure"], ["sa-results"], None),
  (A, False, ["sa-stack"], ["sa-memory"], None),
  (A, False, ["sa-fn-lambda"], ["sa-functions"], None),
  (A, False, ["sa-typed-failure"], ["sa-results"], None),
  (A, True,  ["sa-typed-failure"], ["sa-results"], None),
  (A, True,  ["sa-typed-failure"], ["sa-results"], None),
  (A, False, ["sa-value-object"], ["sa-value"], None),
  (A, False, ["sa-value-object"], ["sa-value"], None),
  (A, True,  ["sa-typed-failure","sa-effects"], ["sa-results"], None),
]),
}

TITLES = {
  "01-intro-and-setup": "Intro & Setup",
  "02-values-types-and-expressions": "Values, Types & Expressions",
  "03-functions-and-methods": "Functions & Methods",
  "04-collections": "Collections",
  "05-oop-classes-traits-case-classes-enums": "OOP — Classes, Traits, Case Classes & Enums",
  "06-pattern-matching-option-try-either": "Pattern Matching, Option, Try & Either",
  "07-generics-variance-advanced-types": "Generics, Variance & Advanced Types",
  "08-givens-and-extensions": "Givens & Extensions",
  "09-concurrency-and-error-handling": "Concurrency & Error Handling",
}

presentations = []
stems_index = {}   # stem -> list of (filename) for tts cross-check
for stem, (default_scene, rows) in MAP.items():
    nn = stem.split("-")[0]
    heads = headings(stem)
    assert len(heads) == len(rows), f"{stem}: {len(heads)} headings vs {len(rows)} rows"
    sections = []
    files = []
    for i, (h, (scene, spine, hi, fo, role)) in enumerate(zip(heads, rows), start=1):
        ss = f"{i:02d}"
        st = f"{nn}-{ss}-{slug(h)}"
        sec = {"heading": h, "scene": scene, "spine": spine}
        if role:
            sec["role"] = role
        if hi:
            sec["highlight"] = hi
        if fo:
            sec["focus"] = fo
        sec["audio"] = f"audio/{st}.wav"
        sections.append(sec)
        files.append(st)
    stems_index[stem] = files
    presentations.append({
        "id": f"{nn}-{slug(TITLES[stem])}",
        "title": TITLES[stem],
        "notebook": f"notebooks/{stem}.ipynb",
        "defaultScene": default_scene,
        "sections": sections,
    })

manifest = {
    "concept": "Scala",
    "design": "DESIGN.md",
    "scenes": [
        {"id": "scala-jvm", "title": "Scala on the JVM", "status": "built"},
        {"id": "scala-anatomy", "title": "Scala — Anatomy", "status": "built"},
    ],
    "presentations": presentations,
}

OUT.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n")
n = sum(len(v) for v in stems_index.values())
print(f"wrote {OUT} — {len(presentations)} modules, {n} wired sections")
# also dump the stem list for the tts step
Path("/Users/maddipotiganesh/Products/scala-content/scripts/tts_stems.txt").write_text(
    "\n".join(f"{stem}\t{f}\t{h}"
             for stem in MAP
             for f, h in zip(stems_index[stem], headings(stem))) + "\n")
print("wrote scripts/tts_stems.txt")
