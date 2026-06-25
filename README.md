# scala-content

A **content repo** for the `graphl-ux` learning app (sibling repo). It holds the
**Scala** concept — notebooks, per-section narration scripts, and the `manifest.json`
that wires sections to scenes — fetched by the app **at runtime** over raw GitHub.

There is **nothing to build, run, or test** here. Correctness is verified by the
`graphl-ux` app consuming this content. (The one executable is
`scripts/colab_generate_audio.ipynb` — a Colab tool that turns `tts/` scripts into
`audio/` `.wav`s.)

## Layout

```
manifest.json   # wires each module: notebook ref + per-section overlay (scene/spine/role/audio/highlight/focus)
notebooks/      # the teaching .ipynb (prose + code source of truth) — 01..09
tts/            # per-section narration scripts (plain spoken prose)
audio/          # generated .wav narration (per-section) — generated on Colab
scenes/         # reserved/empty — real scenes live in the graphl-ux app (src/scenes)
scripts/        # colab_generate_audio.ipynb — tts/*.tts -> audio/*.wav on a Colab GPU
```

## The contract (shared with apache-spark-content / java-content)

1. **The notebook is the single source of truth** for a module's prose and code.
   The `manifest.json` only *wires* — it must never duplicate notebook content.
2. The app splits each notebook at every `## ` heading into **sections** (= pages),
   matched to the manifest overlay by **normalized heading text** (case / backticks /
   whitespace insensitive). A heading edit in a notebook must be mirrored here.
3. A section's diagram **images are stripped** by the app — a **scene** replaces them.
4. **Scenes live in `graphl-ux`** (`src/scenes`), authored in TypeScript — not here.
   The Scala concept's two maps are `scala-jvm` and `scala-anatomy`. Here you only
   reference a scene **by id** in the manifest.

## Narration (per-section TTS)

One `.tts` script **per section**, plain spoken prose — what a teacher would say at a
whiteboard. Naming: `tts/<NN>-<SS>-<slug>.tts` → `audio/<NN>-<SS>-<slug>.wav`, where
`NN` is the module number and `SS` the section order. The stem is shared by the
`.tts`, the `.wav`, and the manifest `audio` field. The notebook's "What's covered"
overview and trailing "What's next" outro are dropped — they are reading-only.

See `apache-spark-content/CLAUDE.md` "TTS guidelines" for the full style rules (plain
prose, no markdown/code, spell out symbols and acronyms).

## How content is served

The app fetches this repo at runtime over **raw GitHub**:
`https://raw.githubusercontent.com/schemabotview/scala-content/main/…`
A content change is live once pushed to `main` — no app rebuild needed.

## Source of notebooks

Notebooks are copied as-is from the runnable curriculum at `~/Projects/scala`.

## Status

- Scaffolded; 9 notebooks copied in.
- **Modules 01–09 (Scala 3)** are scene-wired in `manifest.json` — each section
  mapped to `scala-jvm` (runtime/toolchain topics) or `scala-anatomy` (language
  topics) with `spine`/`highlight`/`focus`/`role`. The "What's covered" overview and
  "What's next" outro of each module are intentionally unwired.
- **Modules 01–09 are fully narrated** — per-section `tts/*.tts` scripts rewritten per
  the TTS guidelines, each wired to a matching `audio/*.wav` stem in the manifest.
- The per-section `.wav`s still need a Colab generation pass (`tts/` → `audio/`).
- Scenes `scala-jvm` + `scala-anatomy` are authored and registered in graphl-ux, and
  the Scala concept is in the app's catalog (`graphl-ux/src/content/catalog.ts`).
- **Not yet pushed to GitHub.**
