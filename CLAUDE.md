# CLAUDE.md — scala-content

A **content repo** (not an app) for the `graphl-ux` engine. It holds the **Scala**
concept: notebooks, per-section narration, and the `manifest.json` that wires them.
The app fetches this repo's `manifest.json` + notebooks over the network and renders
them. Read `README.md` first; this file is the working orientation.

This repo is a sibling of `apache-spark-content` and `java-content` and follows the
**same contract** — when in doubt, mirror what those repos do (`apache-spark-content`'s
`CLAUDE.md`/`DESIGN.md`/`MODULES.md` are the mature reference, especially the **TTS
guidelines** and the **fixed semantic palette**).

## The core contract (do not break)

1. **The notebook is the single source of truth** for prose and code. `manifest.json`
   only *wires* sections — never duplicate notebook content here.
2. The app splits each notebook at every `## ` heading into sections (= pages) and
   matches them to the manifest by **normalized heading** (lowercase, backticks
   stripped, whitespace collapsed — see graphl-ux `content/module.ts`). A heading edit
   in a notebook must be mirrored in the manifest `heading`.
3. Section diagram **images are stripped** by the app — a **scene** replaces them.
4. **Scenes live in `graphl-ux`** (`src/scenes`), authored in TypeScript — not here.
   The `scenes/` dir is reserved/empty. Reference a scene by **id** only.

## The Scala scenes (in graphl-ux, not here)

Two dense maps, ported from NodeMap (`scala.ts` / `scala-anatomy.ts`) and registered
in `graphl-ux/src/scenes/index.ts`. They mirror `java-jvm` / `java-anatomy` — same JVM
runtime, Scala-specific source + grammar:

- **`scala-jvm`** — the runtime: source pipeline (`.scala` → `scalac` → `.class`) →
  class loader sub-system → JVM memory areas → execution engine (interpreter / JIT /
  GC) → CPU. Node ids are `sc-*` (e.g. `scalac`, `sc-class-file`, `sc-interpreter`,
  `sc-jit-compiler`, `sc-gc`, `sc-classloader-subsystem`).
- **`scala-anatomy`** — the language grammar: four rhythm rows (Model ▸ Initialize ▸
  Transform ▸ Return) following `Kind  Name  : Type  =  Value`, plus a Memory column.
  Node ids are `sa-*` (e.g. `sa-kind`, `sa-bind-val`, `sa-bind-lazy`, `sa-type`,
  `sa-type-coll`, `sa-type-oop`, `sa-generic`, `sa-adt`, `sa-methods`, `sa-functions`,
  `sa-coll-ops`, `sa-control`, `sa-pattern`, `sa-loops`, `sa-value`, `sa-typed-failure`,
  `sa-hamt`).

Highlighting a container id lights its children, so spotlight the box (`sa-type`,
`sa-coll-ops`) to light a whole group. Always check this list of ids before adding a
`highlight`/`focus`.

## manifest.json shape

Top level: `concept`, `design`, `scenes[]` (id/title/status), `presentations[]` (one
per module). Each presentation: `id`, `title`, `notebook`, `defaultScene`,
`sections[]`. Each section overlay: `heading` (must match a notebook `## ` heading,
normalized), `scene`, `spine` (bool — feed-mode narration), optional `role` (`"hook"`),
optional `audio` (repo-relative `.wav`), optional `highlight` (scene node ids — AMBER,
rest dim), optional `focus` (node id(s) the camera frames).

## Narration

One `.tts` per section, plain spoken prose. Naming `tts/<NN>-<SS>-<slug>.tts` →
`audio/<NN>-<SS>-<slug>.wav`; the stem is shared by the `.tts`, the `.wav`, and the
manifest `audio` field. **Drop the notebook's "What's covered" overview and the
trailing "What's next" outro** — those are reading-only, not narrated, so those two
section indices are left as a gap in the per-module SS numbering. Follow
`apache-spark-content/CLAUDE.md` "TTS guidelines" verbatim (no markdown/code, spell
out symbols/acronyms — e.g. JVM → "java virtual machine", `=>` → "maps to", `val`
unchanged but `lazy val` spoken as words, version `3.3.7` → "three point three point
seven").

The source curriculum at `~/Projects/scala/tts/` has **one `.tts` per notebook** (a
monologue with the coverage-map intro and outro). Per-section files here are
**rewritten** from the notebook prose + that source, anchored to the notebook's `## `
headings — not mechanically sliced.

## When wiring a module

1. Confirm the notebook is in `notebooks/` and its `## ` headings are final.
2. Add a `presentations[]` entry; list every section (each becomes a page).
3. Set `scene` per section (`scala-jvm` for runtime/toolchain topics, `scala-anatomy`
   for language-grammar topics), `spine` for essentials, `role: "hook"` on the first.
4. Author one `tts/<NN>-<SS>-<slug>.tts` per section, set each `audio`, then run
   `scripts/colab_generate_audio.ipynb` to generate + push the `.wav`s.

## Status

- Scaffolded; 9 notebooks copied in from `~/Projects/scala`.
- **Modules 01–09 (Scala 3)** scene-wired AND narrated in `manifest.json`
  (scene/spine/highlight/focus/role + per-section `audio`). Each module's "What's
  covered" and "What's next" sections are intentionally unwired (no audio).
- Per-section `tts/*.tts` scripts rewritten per the TTS guidelines, 1:1 with the
  manifest `audio` stems. `.wav`s pending a Colab generation pass.
- Scenes `scala-jvm` + `scala-anatomy` are authored and registered in graphl-ux, and
  the Scala concept is added to the app catalog (`graphl-ux/src/content/catalog.ts`).
- Not yet pushed to GitHub.
