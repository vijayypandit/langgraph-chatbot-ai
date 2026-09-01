# Short-Term Memory (STM) in LangGraph ChatBot

## 📑 Quick Navigation

| Section | Purpose |
|---------|---------|
| [⚡ What is STM?](#overview) | Understand STM concepts |
| [🏗️ Architecture](#architecture-overview) | System design overview |
| [📋 Implementations](#implementation-approaches) | Four STM approaches |
| [🛠️ Quick Start](#quick-start-guide) | Get started in 5 minutes |
| [🔧 Troubleshooting](#troubleshooting) | Common issues & solutions |

---

## 📊 Overview

**Short-Term Memory (STM)** is the chatbot's conversation history within a single chat thread. It enables multi-turn dialogue by maintaining full message context.

| Aspect | STM | LTM |
|--------|-----|-----|
| **Scope** | Single conversation | All conversations |
| **Storage** | Message list (MessagesState) | Key-value store |
| **Persistence** | Via checkpointer | Always persistent |
| **Primary Use** | Conversation context | User facts & preferences |

---

## 🎯 Why STM Matters

- ✨ Enable multi-turn conversations with full context
- ✨ Manage token limits efficiently (trimming/summarization)
- ✨ Persist conversations across restarts (optional)
- ✨ Support multiple independent chat threads

---

## 🏗️ Architecture Overview

### Core Components

| Component | Purpose |
|-----------|---------|
| **MessagesState** | Stores all conversation messages as a list |
| **StateGraph** | LangGraph engine that orchestrates message flow |
| **Checkpointer** | Persists state (InMemory or PostgreSQL) |
| **Thread ID** | Unique identifier for conversation isolation |

### System Flow

```
User Input
    ↓
[LangGraph State Graph]
    ├─ Load message history (via Checkpointer)
    ├─ Invoke LLM with full context
    └─ Append AI response to state
    ↓
[Save to Checkpointer]
    ↓
Next Invocation (same thread_id)
    ├─ Retrieve previous messages
    └─ Continue conversation
```

---

## 📋 Implementation Approaches

### 1️⃣ Basic In-Memory STM

**File**: [`_stm.ipynb`](_stm.ipynb)

**Key Features**: 📝
- RAM-based storage with thread isolation
- Complete message history per thread
- Data cleared on app restart

**Use When**: Learning basics, testing locally

---

### 2️⃣ Persistent STM with PostgreSQL

**File**: [`_stm_persistance.ipynb`](_stm_persistance.ipynb)

**Key Features**: 💾
- Database-backed state persistence
- Multi-user conversation isolation
- Indefinite conversation recovery

**Use When**: Production deployments, multi-user scenarios

---

### 3️⃣ Token-Limited STM (Trimming)

**File**: [`_stm_trimming.ipynb`](_stm_trimming.ipynb)

**Key Features**: 🧹
- Implements `trim_messages()` strategy
- Token counting via `count_tokens_approximately()`
- Configurable max token threshold
- Strategies: `"last"` (recommended), `"first"`, `"sliding_window"`

**Why Trim?**: Reduce API costs, stay within token limits, improve focus

**Use When**: Long conversations, cost optimization needed

---

### 4️⃣ Summarization-Based STM

**File**: [`_stm_summarization.ipynb`](_stm_summarization.ipynb)

**Key Features**: 📚
- Compress old messages into AI-generated summaries
- Keep recent messages in full
- Preserves context while reducing tokens

**Use When**: Advanced long-conversation handling, maximum context preservation

---

## ⚖️ STM vs LTM Comparison

| Feature | STM | LTM |
|---------|-----|-----|
| **Storage** | Message array | Key-value store |
| **Lifespan** | Single thread | Across all conversations |
| **Retrieval** | Automatic (full history) | Manual queries |
| **Persistence** | Optional | Always persistent |
| **Use Case** | Conversation flow | User facts & knowledge |

**Recommended Hybrid Approach**:
- Use **STM** for conversation context
- Use **LTM** for persistent user preferences
- See [LTM documentation](./LTM_README.md) for cross-conversation knowledge

---

## ⚡ Quick Start Guide

### 📋 Prerequisites
- 🐍 Python 3.9+
- 📦 LangGraph, LangChain libraries
- 🔑 API key (Groq, Google, OpenAI, etc.)
- 📂 PostgreSQL (optional, for persistence)

### 🚀 Getting Started

1. 📖 Open [`_stm.ipynb`](_stm.ipynb)
2. ▶️ Run cells in order (basic STM)
3. 🧪 Test multi-turn with same `thread_id`
4. 🔄 Try different checkpointers (InMemory → PostgreSQL)
5. 🧹 Add trimming for long conversations

---

## 🎯 Core Concepts

### MessagesState
Stores messages as `{role, content}` pairs. LangGraph's `add_messages` reducer automatically manages deduplication and ordering.

### Thread ID
Unique identifier for conversation isolation. Each thread maintains independent STM.

### Checkpointer
Persistence layer:
- **InMemorySaver**: Fast, ephemeral (good for development)
- **PostgresSaver**: Durable, shareable (good for production)

---

## 🔧 Troubleshooting

### ❓ Memory not retained?
**✅ Solution**: Use same `thread_id` across invocations. Verify checkpointer is configured correctly.

### ❓ Database connection fails?
**✅ Solution**: Verify PostgreSQL is running on port 5432 and connection string is correct.

### ❓ Token limit errors?
**✅ Solution**: Enable trimming with `trim_messages()` or use summarization strategy.

### ❓ Messages growing indefinitely?
**✅ Solution**: Implement trimming strategy ("`last`" keeps recent messages, "`first`" keeps old ones).

---

## 📚 Learning Path

1. 🌟 **Start Here**: [`_stm.ipynb`](_stm.ipynb) — Basic STM concept
2. 📈 **Next**: [`_stm_trimming.ipynb`](_stm_trimming.ipynb) — Token management
3. 🚀 **Advanced**: [`_stm_persistance.ipynb`](_stm_persistance.ipynb) — Database persistence
4. ⭐ **Expert**: [`_stm_summarization.ipynb`](_stm_summarization.ipynb) — Sophisticated strategies

---

## ✅ Quick Checklist

- [ ] 📦 Install LangGraph and dependencies
- [ ] 🔑 Set up `.env` with API keys
- [ ] 📊 Create MessagesState graph
- [ ] 💾 Add checkpointer (InMemory or PostgreSQL)
- [ ] 🧠 Implement LLM node function
- [ ] 🧪 Test with same thread_id across invocations
- [ ] ✓ Verify message history retained
- [ ] 🧹 (Optional) Add trimming for long conversations
- [ ] 🎨 (Optional) Implement summarization strategy

---

### 🌈 **Your Chatbot Now Has Memory! 🧠✨**

Happy building! 🚀

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
