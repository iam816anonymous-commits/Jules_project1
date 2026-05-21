# Jarvis OS Phase 7: Validation + Hardening + Deployment

## Validation Scenarios
1. **Research & Summarize**: Browser search -> fetch -> summarize -> save to local markdown.
2. **Autonomous Coding**: Open IDE (VSCode stub) -> create project -> implement function -> run test -> fix on failure.
3. **Fault Tolerance**: Browser crash during task -> relaunch -> resume context from `WorldState`.
4. **Perception Stress**: Rapid window movement -> re-ground `DesktopGraph` -> verify focus consistency.
5. **Multimodal Conflict**: Voice interruption while executing a desktop plan -> pause -> handle intent -> resume/re-plan.

## Chaos Test Cases
- **UI Corruption**: Randomize OCR results for 500ms to test confidence decay.
- **Process Crash**: Terminate active application (Browser/Terminal) mid-task.
- **Planner Deadlock**: Inject circular dependencies in `RuntimeGraph`.
- **Memory Corruption**: Corrupt working memory hash to trigger `RecoveryEngine`.

## Benchmarking Metrics
- **Completion Rate**: Goal reached / Total attempts (Target >= 85%).
- **Recovery Rate**: Errors recovered / Total errors (Target > 70%).
- **Hallucination %**: Actions taken on invalid state / Total actions (Target < 10%).
- **Latency**: End-to-end cognitive cycle tick time (ms).
- **Safety**: Unsafe actions blocked / Total unsafe actions (Target 100%).

## Deployment & Packaging
- **Launcher**: Bootstrap the `RuntimeKernel` and `FastAPI` backend.
- **Profile Manager**: Handle user configurations and persistent memory mounts.
- **Validation Report**: Automated generation of test results and maturity estimates.
