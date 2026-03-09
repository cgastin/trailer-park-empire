# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Architecture

Read these files before making changes:

- docs/FOUNDATION.md
- docs/AI_AGENT_RULES.md
- docs/REPOSITORY_STRUCTURE.md
- prompts/CLAUDE_SYSTEM_PROMPT.md

docs/FOUNDATION.md is the source of truth.** If a proposed change conflicts with it, the document wins unless the project owner explicitly overrides it.

Trailer Park Empire is a mobile builder/simulation game (think FarmVille). The architecture is **client-heavy**: all gameplay logic runs locally on device. Firebase is only used for auth and cloud save — do not use it for gameplay.

**Stack (fixed — do not change without explicit instruction):**
- Game engine: Godot 4, GDScript only
- Backend: Firebase (minimal — auth + cloud save only)
- Targets: iOS and Android

**Repo layout:**
```
/docs      — project documentation (FOUNDATION.md is the master doc)
/prompts   — AI agent system prompts
/game      — Godot project (all game code lives here)
```

Within `/game`, follow standard Godot 4 conventions:
- `scenes/` — `.tscn` scene files
- `scripts/` — `.gd` script files grouped by domain (see below)
- `assets/` — sprites, audio
- `data/` — JSON config files (prefer data-driven design)

**Script domain subdirectories** (see `docs/REPOSITORY_STRUCTURE.md` for the authoritative layout):
- `scripts/core/` — autoloads and core systems (e.g., `GameState.gd`)
- `scripts/placement/` — lot grid and trailer placement logic
- `scripts/economy/` — currency, income (Milestone 2)
- `scripts/save/` — local persistence (Milestone 2)
- `scripts/progression/` — upgrades, quests (Milestone 3)
- `scripts/utils/` — shared helpers

## Godot / GDScript Rules

- Each `.gd` file should have one focused responsibility — keep scripts small
- Prefer composition over inheritance; avoid deep class hierarchies
- Prefer data-driven systems (JSON in `data/`) over hardcoded values
- Use `@export` for designer-tunable values
- Autoloads (singletons) are for truly global state only (e.g., `GameState`)
- All gameplay runs locally — no network calls in game logic scripts

## System Architecture (Milestone 1)

The current signal flow for trailer placement:

```
LotGrid.lot_clicked  →  TrailerPlacer.place_trailer()
                              ↓
                    writes GameState.lots
                              ↓
                         queue_redraw()
```

Key contracts:
- `GameState.lots` — `Dictionary` keyed by `Vector2i`, values `{"type": "trailer"}`
- `TrailerPlacer` is **not** placed in the scene tree; it is instantiated dynamically in `Main.gd` via `preload()` and added as a child at runtime

Do not re-architect this without reading `docs/FOUNDATION.md` first.

## Development Milestones

**Completed:**
- Milestone 1 — First Playable Prototype (map background, lot grid, trailer placement, placement validation)
- Milestone 2 — Currency, income, local save
- Milestone 3 — Upgrades, unlock rules, simple quests

**Current target: Milestone 4** — Firebase auth + cloud save

Upcoming: Monetization.

## Art & Graphics

**Do not add real sprites or art assets until Milestone 4 is complete.**

Placeholder visuals (colored rectangles) are intentional. The screen layout and visual states are not stable until the core game loop is fully implemented.

After Milestone 4, create `prompts/GRAPHICS_PROMPT.md` to guide art agents. It should cover:
- Art style (pixel art, cartoon, isometric, etc.)
- All visual states: empty lot, placed trailer, upgraded trailer, locked lot
- UI elements needing icons or polish
- Map background and environment
- Color palette

## Git & PR Workflow

**main is protected.** Claude must never push directly to main.

### Branch naming
```
feat/<short-description>     # new feature
fix/<short-description>      # bug fix
chore/<short-description>    # non-gameplay changes (docs, config)
```

### Session startup (run at the start of every session)
```bash
source ~/.zshrc
export GITHUB_APP_ID GITHUB_APP_INSTALLATION_ID GITHUB_APP_KEY_PATH
gh auth login --with-token <<< $(bash tools/get-agent-token.sh)
git pull origin main
```

### Every task follows this flow
1. Run session startup commands above
2. `git checkout -b feat/<description>` — create feature branch
3. Do the work, commit on the branch
4. `git push -u origin <branch>`
5. `gh pr create` — open PR, post the URL to the user
6. User reviews on GitHub and merges
7. Next session starts fresh from step 1

### Commit identity
This repo uses a local git config that attributes commits to the agent:
- `user.name = Claude Sonnet`
- `user.email = claude-sonnet-4-6@noreply.anthropic.com`

Do not change this config. The project owner (Chris Gastin) reviews and merges via GitHub — he does not commit directly to this repo.

### Commit message format
```
<type>: <short summary>

<body — what changed and why>

```

## Godot CLI

Run the Godot editor from the command line (`godot` is on PATH at `/usr/local/bin/godot`, v4.6.1):

```bash
# Open the project in the editor
godot --path game/

# Run the project headlessly (CI / smoke test)
# Note: do NOT use -s with a .tscn — it bypasses autoload registration
godot --path game/ --headless --quit

# Export (requires export templates installed)
godot --path game/ --export-release "Android" build/game.apk
```
