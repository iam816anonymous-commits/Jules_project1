# Jarvis OS Phase 4.5: World Model & Perception Grounding

## Runtime Flow
1. **Perception**: Vision (Screen Observer) + Voice (ASR) + Desktop APIs.
2. **Grounding**: Observation Fusion merges raw signals into the World Model.
3. **Attention**: Attention Manager identifies the most salient entities/tasks.
4. **Planning**: Planner vNext generates graph-based plans grounded in the current World State.
5. **Validation**: Action Validator checks plan feasibility against the World Model.
6. **Execution**: Control Executor performs actions (Mouse/Keyboard/API).
7. **Refinement**: Reflection Engine updates the World Model based on action results.

## World Model Graph
```
WorldState
 ├── Desktop (Graph Root)
 │    ├── Window (VSCode)
 │    │    └── Editor (Focus)
 │    ├── Window (Browser)
 │    │    ├── Tab (GitHub)
 │    │    └── Tab (Docs)
 │    └── Window (Terminal)
 ├── Entities (Tracked objects across frames)
 ├── Active Context (Memory links + Task state)
 └── Confidence (State belief scores)
```

## Vision Pipeline
- **Screen Observer**: Raw capture -> Compression.
- **UI Detector**: Element identification (Buttons, Inputs, Icons).
- **OCR Engine**: Text extraction and spatial mapping.
- **Scene Graph**: Spatial relationship mapping of UI elements.
- **Multimodal Fusion**: Correlating visual elements with OS accessibility trees.

## Voice Pipeline
- **Wake Engine**: Hotword detection.
- **ASR (Automatic Speech Recognition)**: Audio to Text.
- **Voice Router**: Intent classification and routing to Runtime.
- **Dialog Manager**: Managing conversational state and interruptions.
- **TTS (Text to Speech)**: Text to Audio output.

## Integration Map
- `Vision` -> `ObservationFusion` -> `WorldModel`
- `WorldModel` <-> `Planner` (Contextual Planning)
- `WorldModel` <-> `Memory` (Experience Retrieval)
- `ActionValidator` (Pre-flight check against `WorldModel`)
