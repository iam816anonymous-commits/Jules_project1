# Jarvis OS Phase 6: Embodiment + Learning + Self-Improvement

## Learning Graph
```
[ExperienceBuffer]
 ↓
[RewardEngine] -> [AgentMetrics]
 ↓
[PatternExtractor] -> [MistakeTracker]
 ↓
[SkillCompiler] -> [SkillLibrary]
 ↓
[BehaviorOptimizer] -> [AdaptationEngine]
 ↓
[KnowledgeIntegrator] -> [MemorySystem]
```

## Reward Flow
1. **Outcome**: Action result + Reflection analysis.
2. **Success Metrics**: Speed, Accuracy, Recovery count.
3. **Penalties**: Hallucination detection, Policy violations, Timeouts.
4. **Scalar Reward**: Combined score normalized to [0, 1].

## Memory Evolution
- **Short-Term**: `ExperienceBuffer` (Last N events).
- **Episodic**: Postgres storage of full events.
- **Semantic**: Qdrant vector storage of generalized patterns.
- **Procedural**: `SkillLibrary` workflows.

## Skill Lifecycle
- **Discovery**: `PatternExtractor` identifies frequent successful step sequences.
- **Compilation**: `SkillCompiler` converts sequences into a single executable `Skill`.
- **Validation**: Test the skill in a controlled environment.
- **Deployment**: Add to `SkillLibrary` for `Planner` retrieval.
- **Version Control**: Track performance of skill versions over time.

## Adaptation Loop
1. **Analyze**: `MistakeTracker` identifies root causes of failures.
2. **Optimize**: `BehaviorOptimizer` adjusts planner preferences (e.g., use different tool, increase timeouts).
3. **Adapt**: `AdaptationEngine` mutates the `RuntimeKernel` configuration at runtime.
4. **Integrate**: `KnowledgeIntegrator` consolidates lessons into procedural and semantic memory.
