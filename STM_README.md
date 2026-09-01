# Short-Term Memory (STM) in LangGraph ChatBot

## 📑 Table of Contents

1. [Overview](#overview)
2. [Architecture Overview](#architecture-overview)
   - [Core Components](#core-components)
   - [System Architecture Flow](#system-architecture-flow)
   - [Thread & Configuration Model](#thread--configuration-model)
3. [Implementation Approaches](#implementation-approaches)
   - [1️⃣ Basic In-Memory STM](#1️⃣-basic-in-memory-stm)
   - [2️⃣ Persistent STM with PostgreSQL](#2️⃣-persistent-stm-with-postgresql)
   - [3️⃣ Token-Limited STM](#3️⃣-token-limited-stm)
   - [4️⃣ Summarization-Based STM](#4️⃣-summarization-based-stm)
4. [STM vs LTM — Comparison Matrix](#stm-vs-ltm--comparison-matrix)
5. [Quick Start Guide](#quick-start-guide)
6. [Implementation Details](#implementation-details)
7. [Key Takeaways](#key-takeaways)
8. [Learning Path](#learning-path)
9. [Troubleshooting](#troubleshooting)
10. [Related Documentation](#related-documentation)
11. [Checklist for Your Own Implementation](#checklist-for-your-own-implementation)

---

## Overview

**Short-Term Memory (STM)** refers to the ability of a chatbot to remember and maintain conversation context **within a single chat session or thread**. It's the chatbot's immediate working memory that enables:

- Retention of all messages within an active conversation
- Context preservation across multiple conversation turns
- Access to complete message history for coherent responses
- Memory management to optimize token usage and API costs

**Key Concept**: STM exists only during an active conversation session. Unless persisted via a checkpointer, STM is cleared once the session ends.

---

## Architecture Overview

### Core Components

**1. MessagesState** — Core data structure  
Stores all messages in order and maintains conversation history automatically.

**2. StateGraph** — Execution engine  
Manages data flow through nodes and edges, orchestrating message processing.

**3. Checkpointers** — Persistence layer  
Saves conversation state at each step:
- `InMemorySaver`: RAM-based storage (fast, ephemeral)
- `PostgresSaver`: Database storage (persistent, multi-session)

### System Architecture Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                        USER INTERACTION                         │
└────────────────────────────┬──────────────────────────────────┘
                             │ 
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                   LANGGRAPH STATE GRAPH                         │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  MessagesState (Stores all conversation messages)        │  │
│  │  ├─ User Message 1                                       │  │
│  │  ├─ AI Response 1                                        │  │
│  │  ├─ User Message 2                                       │  │
│  │  └─ AI Response 2                                        │  │
│  └──────────────────────────────────────────────────────────┘  │
│                             │                                   │
│                             ▼                                   │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │          Node: call_model (LLM Processing)               │  │
│  │  Receives → Full message history                         │  │
│  │  Processes → Invoke LLM with context                     │  │
│  │  Returns → New AI response                               │  │
│  └──────────────────────────────────────────────────────────┘  │
│                             │                                   │
│                             ▼                                   │
│          New Message Added to MessagesState                    │
└────────────────────────────┬──────────────────────────────────┘
                             │
                             ▼
                   ┌─────────────────────┐
                   │   CHECKPOINTER      │
                   │ (Memory Persistence)│
                   │                     │
                   │ ▪ InMemorySaver     │
                   │   OR                │
                   │ ▪ PostgresSaver     │
                   └─────────────────────┘
                             │
                             ▼
                    ┌────────────────────┐
                    │  Retrieve on Next  │
                    │  Invocation with   │
                    │  Same thread_id    │
                    └────────────────────┘
```

---

## Thread & Configuration Model

```
Application Layer
    │
    ├─ User Session 1 (thread_id: "user-123-chat-1")
    │   └─ Message History: [M1, M2, M3, ...]
    │
    ├─ User Session 2 (thread_id: "user-123-chat-2")
    │   └─ Message History: [M1, M2, ...]
    │
    └─ User Session 3 (thread_id: "user-456-chat-1")
        └─ Message History: [M1, ...]

Each thread maintains independent STM via unique thread_id identifier
```

---

## Implementation Approaches

### 1️⃣ Basic In-Memory STM — [`_stm.ipynb`](_stm.ipynb)

**Purpose**: Foundation-level STM using RAM-based storage with thread-based conversation tracking.

**Key Features**:
- In-memory storage with thread-based isolation
- Complete message history per thread
- Data cleared on application restart

See [_stm.ipynb](_stm.ipynb) for implementation.



---

### 2️⃣ Persistent STM with PostgreSQL — [`_stm_persistance.ipynb`](_stm_persistance.ipynb)

**Purpose**: Database-backed STM enabling conversation persistence across application restarts and multi-user environments.

**Key Features**:
- Database persistence across application restarts
- Multi-user conversation isolation
- Indefinite conversation recovery

See [_stm_persistance.ipynb](_stm_persistance.ipynb) for PostgreSQL setup.

---

### 3️⃣ Token-Limited STM — [`_stm_trimming.ipynb`](_stm_trimming.ipynb)

**Purpose**: Memory-conscious approach for managing token usage in long conversations by trimming message history.

**Key Features**:
- Implements `trim_messages()` strategy
- Token counting via `count_tokens_approximately()`
- Configurable maximum token threshold
- "Last N messages" retention strategy

**Why Trimming Matters**:
- LLMs have token limits (4K–200K typically)
- Long conversations consume high token counts
- Older messages often less relevant than recent ones
- Trimming reduces API costs and keeps context focused

**Trimming Strategies**:
- `"last"` — Keep most recent messages (recommended)
- `"first"` — Keep oldest messages
- `"sliding_window"` — Balanced approach

See [_stm_trimming.ipynb](_stm_trimming.ipynb) for implementation.

---

### 4️⃣ Summarization-Based STM — [`_stm_summarization.ipynb`](_stm_summarization.ipynb)

**Purpose**: Advanced approach compressing old messages into AI-generated summaries while retaining recent messages in full.

**Advantages**:
- Preserves context through summarization
- Reduces token count effectively
- Better long-conversation performance

See [_stm_summarization.ipynb](_stm_summarization.ipynb) for patterns.

---

## STM vs LTM — Comparison Matrix

| Dimension | Short-Term Memory (STM) | Long-Term Memory (LTM) |
|-----------|------------------------|------------------------|
| **Storage Mechanism** | Message array in MessagesState | Key-value store with namespaces |
| **Lifespan** | Single conversation thread | Across all conversations |
| **Retrieval Pattern** | Automatic (full history) | Manual query (specific keys) |
| **Persistence** | Optional (via checkpointer) | Persistent by default |
| **Primary Use** | Current conversation context | User facts, preferences, history |
| **Query Example** | "What did user say 3 turns ago?" | "What language does user prefer?" |
| **Scalability** | Good for single conversation | Good for cross-conversation patterns |

**Recommended Hybrid Approach**:
- Use STM for conversation flow and context
- Use LTM for persistent user preferences and knowledge
- Reference [LTM documentation](../LTM_README.md) for long-term storage

---

## Quick Start Guide

### Prerequisites
- Python 3.9+
- LangGraph, LangChain libraries
- PostgreSQL (optional)
- API key (Groq, Google, etc.)

### Getting Started

1. Open [`_stm.ipynb`](_stm.ipynb) for basic implementation
2. Follow notebook cells in order
3. Test multi-turn conversation with same `thread_id`

---

## Implementation Details

**Messages**: Stored as {role, content} pairs in MessagesState

**Thread ID**: Unique identifier for conversation isolation

**State Retrieval**: Use `graph.get_state(config)` to load saved conversation

Refer to notebook files for detailed patterns.

---

## Key Takeaways

1. **STM = Conversation History**: It's the list of messages in the current chat
2. **Thread ID = Unique Conversation ID**: Multiple threads = multiple independent conversations
3. **Checkpointer = Memory Saver**: InMemory (fast) vs Postgres (persistent)
4. **Trimming = Context Management**: Keep token usage under control for long conversations
5. **MessagesState = The Data Structure**: LangGraph's built-in state for managing messages

---

## Learning Path

1. **Start Here**: [_stm.ipynb](_stm.ipynb) — Understand basic STM concept
2. **Next**: [_stm_trimming.ipynb](_stm_trimming.ipynb) — Learn to manage token limits
3. **Advanced**: [_stm_persistance.ipynb](_stm_persistance.ipynb) — Add database persistence
4. **Future**: [_stm_summarization.ipynb](_stm_summarization.ipynb) — Sophisticated STM strategies

---

## Troubleshooting

**Memory not retained?** — Ensure same `thread_id` is used across invocations

**Database connection fails?** — Verify PostgreSQL connection string and port (5432)

**Token limit errors?** — Enable trimming with `trim_messages()` strategy

See notebook files for implementation-specific solutions.

---

## Related Documentation

- [LangGraph Official Docs](https://python.langchain.com/docs/langgraph)
- [LangChain Messages](https://python.langchain.com/docs/concepts/messages)
- [LangGraph Persistence](https://python.langchain.com/docs/langgraph/concepts/persistence)
- [Token Counting](https://python.langchain.com/docs/concepts/tokens)

---

## Checklist for Your Own Implementation

- [ ] Install LangGraph and dependencies
- [ ] Set up `.env` with API keys
- [ ] Create MessagesState graph
- [ ] Add InMemorySaver checkpointer
- [ ] Implement `call_model` node function
- [ ] Test with same thread_id across multiple invocations
- [ ] Verify message history is retained
- [ ] (Optional) Add PostgresSaver for persistence
- [ ] (Optional) Add trimming for long conversations

---

**Happy chatting! Your AI now has a short-term memory. 🧠✨**
