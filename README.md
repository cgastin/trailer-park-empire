# Trailer Park Empire

A mobile simulation/builder game built with Godot 4 and GDScript. Place trailers, collect income, upgrade your lots, and expand your empire — think FarmVille meets trailer park life.

> **Experiment:** This game is being built primarily by AI coding agents (Claude Code) with a solo human developer directing and reviewing. It explores AI-assisted game development end-to-end.

---

## Gameplay

- Place trailers on a grid of lots
- Collect passive income over time
- Upgrade trailers and unlock new lot types
- Complete quests to progress
- Save progress locally (cloud save coming in Milestone 4)

---

## Development Status

| Milestone | Status | Description |
| --- | --- | --- |
| 1 — Prototype | ✅ Done | Map, lot grid, trailer placement, validation |
| 2 — Game Loop | ✅ Done | Currency, income ticks, local save |
| 3 — Progression | ✅ Done | Upgrades, unlock rules, simple quests |
| 4 — Cloud Identity | 🔄 In Progress | Firebase auth + cloud save |
| 5 — Monetization | ⬜ Upcoming | Premium currency, IAP, starter packs |

---

## Tech Stack

| Layer | Technology |
| --- | --- |
| Game engine | [Godot 4.6](https://godotengine.org/) |
| Language | GDScript |
| Backend | Firebase (auth + cloud save only) |
| Targets | iOS, Android |
| Source control | GitHub |

---

## Prerequisites

- [Godot 4.6.1](https://godotengine.org/download) — download and install, or install via Homebrew on macOS:

  ```bash
  brew install --cask godot
  ```

- No other dependencies required for local development

---

## Running Locally

**Open in the Godot editor:**

```bash
godot --path game/
```

**Run headlessly (smoke test / CI):**

```bash
godot --path game/ --headless --quit
```

**Export (requires export templates installed in Godot):**

```bash
# Android
godot --path game/ --export-release "Android" build/game.apk

# iOS
godot --path game/ --export-release "iOS" build/game.ipa
```

If `godot` is not on your PATH, open the `game/` folder directly in the Godot editor via **File → Open Project**.

---

## Project Structure

```text
trailer-park-empire/
├── game/                    # Godot project
│   ├── scenes/              # .tscn scene files
│   ├── scripts/             # GDScript files, grouped by domain
│   │   ├── autoloads/       # Global singletons (GameState)
│   │   ├── economy/         # Currency, income
│   │   ├── save/            # Local persistence
│   │   ├── progression/     # Upgrades, quests
│   │   └── ui/              # HUD, menus
│   ├── assets/              # Sprites, audio (placeholder until M4)
│   └── data/                # JSON config (trailers, quests, unlocks)
├── docs/                    # Project documentation
│   └── FOUNDATION.md        # Architecture source of truth
├── prompts/                 # AI agent system prompts
└── tools/                   # Dev tooling scripts
```

---

## Architecture Notes

- **Client-heavy**: all gameplay logic runs locally on device
- **Data-driven**: game config lives in `game/data/*.json`
- **Firebase is minimal**: only auth + cloud save — no gameplay logic touches the backend
- Full architecture details: [`docs/FOUNDATION.md`](docs/FOUNDATION.md)

---

## Contributing / Development Workflow

This repo uses a branch + PR workflow. `main` is protected.

```bash
# Create a feature branch
git checkout -b feat/your-feature

# Make changes, commit, push
git push -u origin feat/your-feature

# Open a PR — do not push directly to main
```

See [`CLAUDE.md`](CLAUDE.md) for AI agent instructions and commit conventions.

---

## License

Private — all rights reserved.
