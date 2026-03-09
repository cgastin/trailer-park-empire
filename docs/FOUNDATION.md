# Trailer Park Empire — Project Foundation

## Purpose

This document defines the **technical foundation and development rules** for the Trailer Park Empire project.

All AI agents (Claude Code, Codex, Copilot) and contributors must follow the architecture and principles defined here.

This document exists to keep the project:

- simple
- consistent
- maintainable
- aligned with the original vision

If a proposed change conflicts with this document, **the document wins unless explicitly updated by the project owner.**

---

# Project Overview

Trailer Park Empire is a **mobile simulation / builder game** inspired by games like:

- FarmVille
- Hay Day
- SimCity BuildIt

The player builds and manages a trailer park by placing trailers and structures, collecting income over time, and expanding their park.

The gameplay is **asynchronous** and **not real-time multiplayer**.

Players will:

- place trailers on lots
- collect income
- upgrade structures
- unlock new content
- expand their trailer park empire

---

# Project Goals

## Technical Goal

Demonstrate that a **commercial mobile game can be built primarily with AI coding agents**.

The project intentionally explores **AI-assisted development workflows**.

## Business Goal

Release a mobile game that can eventually monetize through:

- in-app purchases
- premium currency
- starter packs
- optional ads

## Development Goal

Optimize for:

- fast iteration
- minimal infrastructure
- AI-friendly code
- small developer team (solo developer + AI)

---

# Technology Stack

The technology stack is fixed unless explicitly changed by the project owner.

## Game Engine

Godot

## Programming Language

GDScript

## Backend

Firebase (used minimally)

## Target Platforms

- iOS
- Android

## Source Control

GitHub

---

# Core Architecture Philosophy

The project follows a **client-heavy architecture**.

Gameplay simulation should run locally whenever possible.

The backend should only support the game when necessary.

---

# Local-First Gameplay

Most game logic must run on the client.

Examples of client-side systems:

- grid placement
- building timers
- income generation
- quests
- progression
- map state
- inventory display

The game should remain playable even with minimal network connectivity.

---

# Minimal Backend

Firebase will initially be used only for:

- authentication
- cloud save
- basic player identity

Later server features may include:

- purchase validation
- premium currency validation
- reward validation

Do not add backend complexity unless necessary.

---

# Avoid Unnecessary Complexity

Do NOT add the following unless explicitly required:

- multiplayer
- real-time networking
- microservices
- complex backend APIs
- large dependency chains
- premature optimization

This is a **solo developer project assisted by AI agents**.

Simplicity is a priority.

---

# AI-Friendly Code Principles

Because much of the code will be written by AI agents, the codebase must remain easy to understand.

Guidelines:

- small focused scripts
- descriptive names
- minimal inheritance
- avoid tight coupling
- prefer composition
- prefer data-driven systems
- avoid clever but confusing code

Readable code is more important than clever code.

---

# Folder Structure
```
The repository should follow this structure:
/trailer-park-empire

/docs
FOUNDATION.md

/prompts
CLAUDE_SYSTEM_PROMPT.md

/game
Godot project
```

The `/game` directory contains the actual Godot project.

Documentation should always live inside `/docs`.

AI prompts should live inside `/prompts`.

---

# Development Milestones

The project will be developed in small milestones.

## Milestone 1 — First Playable Prototype

Goal:

Allow the player to place a trailer on a lot.

Required features:

- map background
- lot grid
- trailer placement
- placement validation

No backend required.

---

## Milestone 2 — Basic Game Loop

Add:

- simple currency
- income generation
- basic UI
- local save system

---

## Milestone 3 — Progression

Add:

- upgrades
- unlock rules
- simple quests

---

## Milestone 4 — Cloud Identity

Add:

- anonymous authentication (guest play without sign-in)
- Sign in with Apple (required for iOS App Store)
- Sign in with Google
- Facebook Login
- cloud save backup
- account linking (upgrade anonymous session to a named account)

---

## Milestone 5 — Monetization

Add:

- premium currency
- purchase validation
- starter pack

---

# Development Workflow

AI agents should:

1. Read this document before making architectural changes
2. Follow the technology stack
3. Avoid unnecessary complexity
4. Keep systems modular

Human oversight acts as:

- creative director
- architecture reviewer
- final decision maker

---

# Guiding Philosophy

The goal is not to build the most complex architecture.

The goal is to **ship a real playable commercial game built primarily by AI agents**.

Priorities:

1. Playable
2. Simple
3. Maintainable
4. Expandable

Perfect architecture is less important than **finishing the game**.

---

# End of Document