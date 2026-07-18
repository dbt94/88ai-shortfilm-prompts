# Changelog

All notable changes to this project. This repo is a bilingual methodology
+ prompt library + Claude Code Skill for cinematic AI-video prompts.

## v0.5.0 — 2026-07-18

Library → product round: 21 genres, a real prompt builder, and a
consistency planner for multi-shot projects.

### Added
- **4 new genres** (bilingual, 5-stage worked examples) — library now at
  **21 genres**: vertical micro-drama, hard sci-fi space, car commercial,
  dance film.
- **`templates/project-planner.md`** (+`.zh`) — subject registry +
  atmosphere lock + shot list. The Skill now walks users through it before
  writing shot 1 of any 3+ shot piece (the biggest predictor of whether a
  multi-shot film drifts by shot 3–4). Wired into `SKILL.md`/`SKILL.zh.md`,
  cheat sheets, and eval cases.
- **Prompt builder v2** (`docs/build.html` + `/en/build.html`):
  - All **21 genres**, data extracted from `templates/` at build time
    (`docs/assets/builder-data.js` via `generate_pages.py`) — single source
    of truth, no more hand-written genre data.
  - Outputs the **full multi-shot prompt** (same content as the template
    library), not a skeleton; unfilled variables keep `{{...}}` placeholders.
  - Dedicated **negative-prompt box** with its own copy button.
  - **`?g=<slug>` deep links** — share a genre directly.
  - Copy appends a site attribution line.
- README (EN/中文): builder screenshot + updated pitch (21 genres, full
  multi-shot output).

### Fixed
- Unified the negative-prompt heading in `family-recipe-farewell.zh.md` /
  `elderly-cat-companion.zh.md`(「反向提示词」→「负面提示词」) so extraction
  and library terminology are consistent.
- `SKILL.zh.md` caught up with the project-planner rules added to `SKILL.md`.

## v0.4.0 — 2026-06-24

Big content + web round: from a few genres to a broad, searchable library.

### Added
- **14 new cinematic video-prompt genres** (bilingual EN/中文, 5-stage worked
  examples) — bringing the library to **17 genres**:
  product commercial, food ASMR, talking-animal vlog, movie trailer,
  cyberpunk city, claymation / stop-motion, nature timelapse,
  found-footage / CCTV horror, anime → live-action, music video,
  sports slow-motion, fashion film, travel vlog, drone / FPV.
- **Web showcase upgrade** (`docs/`, live at prompts.aiolaola.com):
  - Left-sidebar category layout (replaces top tabs).
  - **English mirror site** at `/en/` with bilingual `hreflang`.
  - **Static per-prompt pages (SSG)** via `scripts/generate_pages.py` —
    each prompt now renders into crawlable HTML with its own
    title/description/canonical/JSON-LD + copy button (62 pages).
  - `sitemap.xml` (65 URLs), `robots.txt`, JSON-LD (WebSite + HowTo),
    Open Graph cover image (`docs/assets/og-cover.png`).
  - Ecosystem nav links (aiOlaOla / AO / SP) with UTM attribution.
- Each genre teaches one distinct camera/technique lesson; SKILL template
  table and README kept in sync (EN + 中文).

### Fixed
- Viral-tab crash in the gallery (`render()` now handles non-section cats).
- Canonical / sitemap URLs aligned to Cloudflare's extensionless serving.
- `travel-vlog` intro montage-structure typo (`food` → `move`).

### Quality
- Multi-agent quality audit across all 17 genres (34 files): 7 hard rules,
  5-stage structure, EN/中文 parity, internal links, and IP-safety all pass.

## v0.3.1

- Skill files moved to `skills/shortfilm-prompt/` (plugin root) with a
  `.claude/skills/` symlink, fixing an empty marketplace install.

## v0.3.0

- Research-grounded upgrade: model table, machine-readable index, cheat
  sheet, negative-prompt prefab, failure-case gallery, dead-link CI.

## v0.2.0 · v0.1.0

- Initial methodology + prompt library + Claude Code Skill, built from
  Mx-Shell's *Zombie Scavenger* method.
