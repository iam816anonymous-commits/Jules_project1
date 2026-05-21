# Database Schema: Qdrant and Redis

## Qdrant (Semantic Memory)
**Collection**: `jarvis_semantic_memory`
**Vector Size**: 1536 (OpenAI Ada 002) or 768 (BGE-small)

**Payload Structure**:
```json
{
  "text": "Extracted text or summary of an event",
  "timestamp": "ISO-8601",
  "tags": ["research", "coding", "error"],
  "metadata": {
    "episode_id": 123,
    "confidence": 0.95
  }
}
```

## Redis (Working Memory)
**Keyspace Strategy**: `jarvis:runtime:{session_id}:state`

**Data Structure**:
- **Active State (Hash)**: `state`, `goal`, `confidence`, `last_observation`
- **Context (JSON)**: Full active context window components.
- **Lock (String)**: Distributed lock for runtime execution.
- **Timeline (List)**: LPUSH events for real-time UI updates.
