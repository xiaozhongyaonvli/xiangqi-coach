# AGENTS.md

## Project Goal
Build the v1.0.0 core rules engine for Chinese Chess (Xiangqi).
No AI, no engine, no analysis in this version.

## Tech Stack
- Language: Python 3.10+
- Test: pytest
- Package layout: src/xiangqi_core

## Commands
- Run tests: pytest
- No external services required.

## Coding Rules
- Keep core logic pure (no UI, no network).
- Small, reviewable changes per PR.
- Add tests for all rule logic.
- Do NOT introduce AI or engine code.

## Definition of Done
- All tests pass
- Core logic only, no app/UI coupling
- Code follows TechSpec_v1.0.0.md

## Repo Navigation
- Core logic: src/xiangqi_core
- Docs: docs/
