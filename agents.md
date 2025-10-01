# Agents Overview

## Executive Summary
AI agents working on Capsule must: follow modular development in feature branches, sync with develop regularly (see `BRANCHING.md`), capture learnings in `lessons.md`, test locally before pushing, use lowercase/monochrome aesthetic for UX, and add timestamps to all data operations.

## Purpose
This repository coordinates multiple service-specific components (`api`, `authentication`, `chat`, `config`, `database`, `frontend`, `llm`, and `web`) to deliver the Capsule AI experience. The `agents.md` document captures high-level guidance for defining and maintaining the conversational agents that interact with these services.

## Agent Responsibilities
- **Core Interfaces**: Route user intents through the `chat` module, leveraging the `api` layer for orchestration and the `llm` package for large language model calls.
- **Data Access**: Interact with the `database` package for persistence while respecting authentication flows from the `authentication` module.
- **Configuration**: Use settings exposed via the `config` module; prefer environment-driven overrides defined in `.env` and `render.json` when deploying.
- **Frontend Integration**: Surface agent capabilities through the `frontend` React application and the `web` service wrapper.

## Agent Definition Checklist
1. Identify the agent's goal and supported user journeys.
2. Determine required context (session state, stored records, external APIs).
3. Map intents to handler functions within the `chat` or domain-specific modules.
4. Validate security boundaries, especially around authentication and data reads/writes.
5. Add automated tests alongside the relevant service package.

## Operational Notes
- Keep sensitive configuration outside of source control; reference keys via environment variables.
- Align agent logging with existing observability patterns in `app.py` and service modules.
- Document meaningful behavioral changes in commit messages to aid cross-team coordination.

## Lesson Capture Protocol
Agents should periodically prompt to capture high-value learnings in `lessons.md`:
- Trigger: Every 3-5 significant interactions or when completing complex tasks
- Format: 1-2 line concise entries focused on reusable, axiomatic insights
- Categories: Architecture, code quality, tooling, debugging, performance, security

## Next Steps
Populate this document with deeper agent-specific playbooks as new capabilities are implemented.
