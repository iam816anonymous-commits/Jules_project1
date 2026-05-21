# Jarvis OS Phase 5: Cognitive Integration + Agent Execution Fabric

## Cognitive Graph
```
Observation
 ↓
[WorldModel] <-> [BeliefState]
 ↓
[AttentionRouter]
 ↓
[IntentResolver] <-> [GoalManager]
 ↓
[TaskDecomposer]
 ↓
[Planner]
 ↓
[ExecutionMonitor] <-> [ActionValidator]
 ↓
[Executor]
 ↓
[Reflection] -> [SelfModel]
 ↓
[Memory]
```

## Execution Graph
- **State**: `AgentStateMachine` (IDLE -> PLANNING -> EXECUTING -> RECOVERING -> LEARNING).
- **Control**: `CognitiveCycle.tick()` drives the state transitions based on `BeliefState`.
- **Monitor**: `ExecutionMonitor` tracks timeouts, stalls, and retries of individual nodes in the `RuntimeGraph`.

## Belief Flow
1. **Input**: Multimodal observations + legacy beliefs.
2. **Fusion**: `ContextFuser` merges temporal and spatial signals.
3. **Belief Update**: `BeliefState` updates its belief about the user intent, system state, and environment.
4. **Scoring**: `ConfidenceTracker` applies Bayesian-like updates to belief certainties.

## Goal Flow
- **High-Level Goal**: Managed by `GoalManager` (Persistence layer).
- **Decomposition**: `TaskDecomposer` breaks goals into a Directed Acyclic Graph (DAG) of sub-tasks.
- **Priority**: Dynamic re-prioritization based on `AttentionRouter` and `SelfModel` (capabilities/limits).

## Integration Map
- `cognition/` acts as the orchestrator for `core/`, `world_model/`, and `memory/`.
- `ExecutionMonitor` provides real-time feedback to `RecoveryEngine` in `core/`.
- `SelfModel` informs the `Planner` of current capabilities and tool limits.
