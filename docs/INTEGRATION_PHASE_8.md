# Jarvis OS Phase 8: Cognition ↔ Perception ↔ Action Connection

## Integration Graph
```
[Perception]         [Cognition]         [Action]
 Vision/OCR ------> Observation ------> Planner
 WindowManager ---> Fusion -----------> Execution Graph
 BrowserContext --> Belief Update ----> Policy/Validator
 Clipboard -------> World Model <----- Control Executor
```

## Runtime Graph
- **Root**: `RuntimeKernel`
- **Loop**: `CognitiveCycle` (0.5s intervals)
- **State**: `WorldState` (Sync via `ObservationFusion`)
- **Persistence**: `MemoryStore` (SQLite)

## Execution Flow
1. **Request**: `GoalManager` accepts high-level intent.
2. **Decompose**: `TaskDecomposer` generates sub-task DAG.
3. **Plan**: `Planner` generates grounded actions for the current DAG node.
4. **Validate**: `PolicyEngine` (Risk) -> `ActionValidator` (Grounding).
5. **Execute**: `ControlExecutor` dispatches to OS (pyautogui/Playwright).
6. **Synchronize**: Post-action `observe()` + prediction comparison.

## Observation Flow
1. **Vision**: Capture screen -> Run OCR Engine -> Run UI Detector.
2. **OS**: Query `WindowManager` (active, bounds) + `DeviceManager`.
3. **Browser**: Query `BrowserController` for active tabs/DOM elements.
4. **Merge**: `ObservationFusion` resolves conflicts and outputs `UnifiedObservation`.

## Belief Update Flow
1. **Predict**: Belief state estimates next state after `execute()`.
2. **Observe**: Real-time perception gathering.
3. **Diff**: Compare prediction vs. actual (Delta identification).
4. **Update**: Bayesian-like update of `BeliefState` confidence.
5. **Persist**: `MemoryStore` records the state transition.
