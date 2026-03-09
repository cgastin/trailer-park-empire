# AI Agent Rules — Trailer Park Empire

## Purpose

This document defines the **rules that all AI coding agents must follow** when working on this repository.

These rules exist to prevent:

- architecture drift
- unnecessary complexity
- inconsistent code patterns
- accidental project rewrites

All AI agents must read and follow:

docs/FOUNDATION.md  
docs/AI_AGENT_RULES.md
docs/REPOSITORY_STRUCTURE.md

before making significant code changes.

---

# Core Rule

**Do not redesign the project.**

The architecture defined in `FOUNDATION.md` is intentional.

If a requested change conflicts with it, explain the issue rather than rewriting the architecture.

---

# Technology Restrictions

The project must use the following technologies.

Game Engine  
Godot

Language  
GDScript

Backend  
Firebase (minimal usage)

Target Platforms  
iOS  
Android

Do not introduce:

- Unity
- Unreal
- Node backends
- custom servers
- additional frameworks

unless explicitly instructed by the project owner.

---

# Simplicity Rule

The project intentionally favors **simple implementations**.

Avoid introducing:

- unnecessary abstractions
- deep inheritance hierarchies
- design patterns that add complexity without clear benefit
- premature optimization

Prefer the **simplest working implementation**.

---

# Folder Structure Rules

The repository structure should remain stable.

```
/docs
/prompts
/game
```


Inside `/game` the Godot project lives.

Do not create new top-level directories unless necessary.

---

# File Creation Guidelines

When creating files:

- place them in the correct directory
- use descriptive names
- avoid generic names like `manager.gd` or `system.gd` unless appropriate
- keep scripts small and focused

---

# Script Design Rules

All gameplay scripts should follow these principles:

- single responsibility
- readable naming
- minimal dependencies
- small functions

Prefer **composition over inheritance**.

Avoid large “god classes”.

---

# Gameplay Logic Rules

The project uses a **local-first gameplay architecture**.

Core gameplay logic must run on the client.

Examples:

- grid placement
- building timers
- income generation
- quests
- progression

Do not require backend calls for normal gameplay actions.

---

# Backend Usage Rules

Firebase should be used only for:

- authentication
- cloud save
- player identity

Later additions may include:

- purchase validation
- reward validation

Do not build complex backend APIs.

---

# Testing Rules

Tests should focus on **game logic**, not visuals.

Good candidates for testing:

- placement validation
- economy calculations
- timer logic
- save/load serialization

Avoid writing tests for UI layout.

---

# Code Style Guidelines

Code should be easy for humans and AI to read.

Guidelines:

- descriptive variable names
- short functions
- clear comments when logic is non-obvious
- avoid clever or overly compact code

Readable code is more important than minimal code.

---

# Feature Development Process

When implementing a new feature:

1. Build the **simplest working version first**
2. Keep the feature local if possible
3. Avoid adding dependencies
4. Document major changes

---

# When Unsure

If a task conflicts with these rules:

1. explain the conflict
2. propose a simpler alternative
3. ask for clarification

Do not make large architectural changes without explanation.

---

# Goal of the Project

The goal is to demonstrate that a **playable commercial mobile game can be built primarily by AI agents**.

Success criteria:

- the game is playable
- the architecture remains simple
- the codebase remains understandable
- the project can ship

The project prioritizes **shipping a game** over building perfect architecture.

---

# End of Document