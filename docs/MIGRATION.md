# Migration Plan: Phase 2.7 to Phase 4

## Changes
- **Runtime**: Transitioning from a linear ReAct loop to a `RuntimeGraphEngine`.
- **Memory**: Migrating from simple episodic stores to a multi-layered persistent system (Postgres + Qdrant + Redis).
- **Planner**: Moving from single-plan generation to multi-plan scoring and graph nodes.

## Steps
1. **Refactor Internal Modules**: Incrementally wrap existing logic into the new `jarvis/` package.
2. **Schema Migration**: Map existing episodic entries to the new Postgres schema.
3. **Core Replacement**: Hot-swap the `RuntimeKernel` once the Graph Engine is stable.
4. **Compatibility Layer**: Maintain legacy tool interfaces while implementing the new desktop control suite.
