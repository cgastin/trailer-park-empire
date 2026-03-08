# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Architecture

**docs/FOUNDATION.md is the source of truth.** If a proposed change conflicts with it, the document wins unless the project owner explicitly overrides it.

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

**Current target: Milestone 2** — currency + income + local save

Upcoming: upgrades/quests → Firebase auth/cloud save → monetization.

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
