# Repository Structure — Trailer Park Empire

## Purpose

This document defines the official repository structure for Trailer Park Empire.

The goals are to:
- keep the repository organized
- prevent AI agents from creating random directories
- ensure consistent file placement
- make the project easy to navigate

All AI agents must follow this structure when creating files.

--------------------------------------------------

Top Level Structure

The repository should contain the following top-level directories:

/docs
/prompts
/game
/backend
/tools

Each directory has a specific purpose and should not overlap responsibilities.

--------------------------------------------------

/docs

The /docs directory contains all project documentation.

Examples of files that belong here:

/docs/FOUNDATION.md
/docs/AI_AGENT_RULES.md
/docs/REPOSITORY_STRUCTURE.md
/docs/GAME_DESIGN.md
/docs/ARCHITECTURE.md

Documentation should never be placed in the root of the repository.

--------------------------------------------------

/prompts

The /prompts directory contains prompts used to guide AI coding agents.

Examples:

/prompts/CLAUDE_SYSTEM_PROMPT.md
/prompts/CODEX_CONTEXT.md

These prompts define the expected behavior of AI agents working in the project.

--------------------------------------------------

/game

The /game directory contains the Godot project.

The Godot project root file "project.godot" must live inside this directory.

Example structure:

/game
project.godot

All runtime game code, scenes, and assets must remain inside /game.

--------------------------------------------------

/backend

The /backend directory contains backend infrastructure and cloud functions.

Example contents:

/backend/firebase.json
/backend/firestore.rules
/backend/functions

This directory should remain minimal until backend features are required.

--------------------------------------------------

/tools

The /tools directory contains developer utilities that are not part of the runtime game.

Examples include:

/tools/data_import
/tools/balance_simulation
/tools/asset_processing

These scripts assist development but are not shipped with the game.

--------------------------------------------------

Godot Project Structure

Inside the /game directory, the Godot project should be organized as follows:

/game
/scenes
/scripts
/assets
/data
/tests
/addons

Each folder has a specific role.

--------------------------------------------------

/game/scenes

Scenes represent major visual structures.

Examples:

/game/scenes/main_scene.tscn
/game/scenes/park_scene.tscn
/game/scenes/trailer_scene.tscn
/game/scenes/ui_scene.tscn

Scenes should be reusable and focused.

--------------------------------------------------

/game/scripts

All gameplay logic lives here.

Scripts should be grouped by domain:

/game/scripts/core
/game/scripts/placement
/game/scripts/economy
/game/scripts/save
/game/scripts/progression
/game/scripts/quests
/game/scripts/utils

Guidelines:
- keep scripts small
- give scripts descriptive names
- avoid large "god classes"

--------------------------------------------------

/game/assets

This folder contains art, audio, and fonts.

/game/assets/art
/game/assets/audio
/game/assets/fonts

Assets should not be mixed with scripts or scene files.

--------------------------------------------------

/game/data

This folder contains game configuration and balancing data.

Examples:

/game/data/buildings.json
/game/data/upgrades.json
/game/data/quests.json

Game balancing values should live in data files whenever possible.

--------------------------------------------------

/game/tests

This folder contains automated tests for game logic.

Suggested layout:

/game/tests/unit
/game/tests/integration
/game/tests/simulation

Tests should focus on:
- economy logic
- placement validation
- timer calculations
- save/load behavior

Tests should not focus on UI layout.

--------------------------------------------------

/game/addons

This folder contains Godot editor extensions and plugins.

Example:

/game/addons/gut

Plugins should be isolated from gameplay scripts.

--------------------------------------------------

File Naming Guidelines

Use clear, descriptive file names.

Good examples:

trailer_placement_system.gd
economy_manager.gd
save_system.gd

Avoid vague names such as:

manager.gd
system.gd
helper.gd

--------------------------------------------------

Directory Creation Rules

AI agents must not create new top-level directories without explanation.

If a new directory is required:
1. explain why it is needed
2. verify it does not duplicate an existing directory
3. ensure it fits the current structure

--------------------------------------------------

Script Design Guidelines

Scripts should follow these principles:
- single responsibility
- readable naming
- minimal dependencies
- short functions

Prefer composition over inheritance.

--------------------------------------------------

Final Rule

The repository structure should remain predictable and stable.

A new developer or AI agent should be able to understand the project layout quickly.

If unsure where something belongs, place it in the most obvious existing directory rather than creating a new one.

End of Document