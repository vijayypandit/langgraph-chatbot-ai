# Long-Term Memory (LTM) in LangGraph ChatBot

## 📑 Quick Navigation

| Section | Purpose |
|---------|---------|
| [🧠 What is LTM?](#what-is-ltm) | Understand LTM concepts |
| [🛠️ Basic Methods Reference](#basic-methods-reference) | Core operations at a glance |
| [📁 Namespaces](#namespace-system) | How to organize data |
| [🚀 Implementation Files](#implementation-files) | Three-step learning path |
| [⚡ Quick Start](#quick-start-guide) | Get started in 5 minutes |
| [🔧 Troubleshooting](#troubleshooting) | Common issues & solutions |

---

## 🧠 What is LTM?

**Long-Term Memory (LTM)** is a persistent key-value store that keeps user information, preferences, and knowledge accessible across all conversations and sessions.

| Aspect | LTM | STM |
|--------|-----|-----|
| **Lifespan** | Across all conversations | Single conversation |
| **Storage** | Key-value pairs (namespaces) | Message list |
| **Query** | Semantic search + exact lookup | All messages included |
| **Use Case** | Persistent knowledge | Current context |

**Why Use LTM?**
- ✅ Store user preferences & profiles permanently
- ✅ Extract & detect duplicate memories automatically
- ✅ Personalize responses based on stored context
- ✅ Search memories semantically using AI embeddings

---

## 🛠️ Basic Methods Reference

Essential LTM operations you'll use most:

| Method | Purpose | Syntax | File Reference |
|--------|---------|--------|-----------------|
| **➕ PUT** | Store data in namespace | `store.put(namespace, key, value)` | [`_ltm_basics.ipynb`](_ltm_basics.ipynb) |
| **🔍 GET** | Retrieve specific value by key | `store.get(namespace, key)` | [`_ltm_basics.ipynb`](_ltm_basics.ipynb) |
| **🔎 SEARCH** | Find all items in namespace (or semantically) | `store.search(namespace, query="text", limit=5)` | [`_ltm_basics.ipynb`](_ltm_basics.ipynb) |
| **✏️ UPDATE** | Modify existing value | `store.put(namespace, key, new_value)` | [`_ltm_implementation.ipynb`](_ltm_implementation.ipynb) |
| **🗑️ DELETE** | Remove data | `store.delete(namespace, key)` | N/A |

### Common Use Cases & Methods

**Store User Profile Info**
```python
namespace = ("user", "u1", "details")
store.put(namespace, "name", {"data": "John Doe"})
```
📁 See: [`_ltm_implementation.ipynb`](_ltm_implementation.ipynb)

**Retrieve Stored Memories**
```python
items = store.search(namespace)  # Get all user memories
for item in items:
    print(item.value)
```
📁 See: [`_ltm_basics.ipynb`](_ltm_basics.ipynb)

**Search Semantically (AI-Powered)**
```python
results = store.search(namespace, query="What sports does user like?", limit=1)
```
📁 See: [`_ltm_basics.ipynb`](_ltm_basics.ipynb)

**Filter Duplicate Memories**
```python
# Extract only NEW memories (is_new=true)
if mem.is_new:
    store.put(namespace, key, mem.text)
```
📁 See: [`_ltm_no_deupliicate_mem.ipynb`](_ltm_no_deupliicate_mem.ipynb)

---

## 📚 Core Concepts

### 🔄 Key Differences from STM

| Aspect | STM | LTM |
|--------|-----|-----|
| **Lifespan** | Single conversation | Across all conversations |
| **Storage** | Message array | Key-value store |
| **Organization** | Linear (by timestamp) | Hierarchical (by namespace) |
| **Query Method** | Automatic (full history) | Manual (specific keys/search) |
| **Retrieval** | All messages included | Targeted queries only |
| **Primary Goal** | Conversation context | Persistent knowledge |

### LTM Architecture

```
APPLICATION LAYER (Users, Conversations, Sessions)
           ↓
   LONG-TERM MEMORY STORE
   (Persistent Key-Value Store)
           ↓
   ┌─────────────┬─────────────┬──────────────┐
   │    USER     │   DOMAIN    │  KNOWLEDGE   │
   │ PROFILES    │  KNOWLEDGE  │   BASE       │
   └─────────────┴─────────────┴──────────────┘
           ↓              ↓              ↓
      Namespace      Namespace      Namespace
     ("user")       ("domain")      ("facts")
   ├─ Key1 →     ├─ Key1 →      ├─ Key1 →
   ├─ Key2 →     ├─ Key2 →      ├─ Key2 →
   └─ Key3 →     └─ Key3 →      └─ Key3 →
```

---

## 📁 Namespace System

A **namespace** is a hierarchical tuple that groups related data together. Think of it like a folder structure.

**Format**: `(category, subcategory, identifier)`

**Examples**:
```python
# 👤 User profiles
("user", "u1", "details")          # User u1's info
("user", "u1", "preferences")      # User u1's preferences

# 📚 Domain knowledge  
("domain", "python", "concepts")   # Python learning materials
("domain", "langraph", "examples") # LangGraph code examples

# 💬 Conversations
("conversation", "u1", "project_x") # Discussion about project X
```

**Best Practices**:
- 🎯 Keep namespaces 3-4 levels deep
- 🎯 Use consistent naming conventions
- 🎯 Separate frequently-queried data into different namespaces
- 🎯 Use meaningful names reflecting data type

📁 See: [`_ltm_implementation.ipynb`](_ltm_implementation.ipynb) for namespace usage in chat nodes

---

## 🚀 Implementation Files

### 1️⃣ Foundations — Basic Store Operations

**[`_ltm_basics.ipynb`](_ltm_basics.ipynb)** — Foundation-level LTM implementation

**Covers**: 🏗️
- InMemoryStore initialization
- Basic PUT/GET/SEARCH operations
- Namespace creation and management
- Data retrieval patterns
- Embedding model integration (Gemini embeddings)
- Semantic search implementation

**Key Concepts**: 📝
- Creating namespaces as hierarchical tuples
- Storing user data (preferences, interests)
- Retrieving data with key lookups
- Semantic similarity search using embeddings

**Implementation Highlights**: 🎯
- Stores sample user data like "User likes travelling", "User likes Pasta"
- Demonstrates semantic search queries: "which game user mostly likes to play?"
- Shows how embeddings enable finding related memories without exact key matches

---

### 2️⃣ Personalized Chat with Memory Extraction (First Implementation)

**[`_ltm_implementation.ipynb`](_ltm_implementation.ipynb)** — LangGraph integration with memory extraction

**Covers**: 🎨
- Integrating LTM store with LangGraph state graphs
- Automatic memory extraction from user messages
- Personalized system prompts based on stored memories
- Building context-aware chat responses

**Key Workflow**: 🔄
1. **Memory Storage Phase**: Extracts user information from messages and stores in LTM
2. **Personalization Phase**: Retrieves stored user memories and injects into system prompt
3. **Chat Response Phase**: LLM responds with personalized context based on user profile

**What It Does**: 🤖
- Creates a chat node that runs through LangGraph
- Stores user profile information (Name, Age, Profession) in namespaces
- Retrieves memories when responding to queries
- Formats user details into system prompt for personalized responses
- Uses memory to reference user context in conversation (e.g., "Since you're a Backend Engineer...")

**Limitation Identified**: 
- Stores all extracted memories without checking for duplicates
- Same user information may be stored multiple times if mentioned repeatedly
- This leads to memory bloat and redundant storage

---

### 3️⃣ Duplicate-Free Memory Extraction (Improved Implementation) ⭐

**[`_ltm_no_deupliicate_mem.ipynb`](_ltm_no_deupliicate_mem.ipynb)** — LangGraph with smart de-duplication

**Covers**:
- Memory extraction with duplicate detection
- Structured decision-making for memory storage
- Atomic memory items with novelty checking
- Preventing redundant information storage

**Key Enhancements Over Step 2**: ⭐
- **MemoryItem Model**: Pydantic model that marks each extracted memory as `is_new` (true) or duplicate (false)
- **MemoryDecision Model**: Structured output that decides whether to store memories and filters duplicates
- **Duplicate Detection Logic**: Compares extracted information against existing memories using semantic understanding
- **Smart Storage**: Only stores memories marked as `is_new=true`, preventing duplication

**What It Does**: ✈️
1. Extracts atomic user memories from each message
2. Loads existing memories from the store
3. Uses an extractor LLM to analyze if each extracted memory is truly NEW
4. Only persists memories that add genuinely new information
5. Responds with "Noted..." while filtering redundant data

**De-duplication Strategy**: 🎣
- Each memory compared against existing user details
- Semantic similarity check: "Is this basically the same meaning as something already stored?"
- Only incremental knowledge gets saved, not repetitive information
- Keeps memory store clean and organized

---

## 📈 Learning Progression

```
Step 1: FOUNDATIONS
  ↓
[_ltm_basics.ipynb]
├─ Store initialization
├─ Namespace design
├─ PUT/GET/SEARCH operations
└─ Semantic search with embeddings

  ↓
Step 2: FIRST IMPLEMENTATION (With Duplicates)
  ↓
[_ltm_implementation.ipynb]
├─ LangGraph integration
├─ Automatic memory extraction
├─ Personalized chat responses
└─ Issue: Duplicate memories stored

  ↓
Step 3: IMPROVED IMPLEMENTATION (Without Duplicates)
  ↓
[_ltm_no_deupliicate_mem.ipynb]
├─ Smart de-duplication logic
├─ Structured decision-making (Pydantic models)
├─ Novelty detection for each memory
└─ Clean, non-redundant memory storage
```

---

## ⚖️ LTM vs STM Comparison

| Feature | STM (Short-Term) | LTM (Long-Term) |
|---------|------------------|-----------------|
| **Scope** | Single conversation | All conversations |
| **Storage** | Message list | Key-value store |
| **Organization** | Sequential (time-based) | Hierarchical (namespace) |
| **Retrieval** | Automatic | Manual query |
| **Persistence** | Optional | Permanent |
| **Data Type** | Messages only | Any data type |
| **Search** | Full history | Semantic search |
| **Query Example** | "Show all messages" | "Find user preferences for u123" |
| **Update Pattern** | Append only | Put/Update/Delete |

**Integration Strategy**:
- Use STM for current conversation flow
- Use LTM to enhance responses with persistent knowledge
- Combine both for intelligent, context-aware chatbots

---

## ⚡ Quick Start Guide

### 📋 Prerequisites
- 🐍 Python 3.9+
- 📦 LangGraph library
- 🔑 Embedding model API key (Google Gemini or OpenAI)

### Setup Steps

1. **Install Dependencies**
   - Install langchain, langgraph, langchain-google-genai
   - Set up `.env` with API keys

2. **Initialize Store**
   - Create InMemoryStore instance
   - Configure embeddings model
   - Set embedding dimensions

3. **Define Namespaces**
   - Plan data organization structure
   - Create namespace tuples for categories
   - Document namespace hierarchy

4. **Implement Operations**
   - Add data via PUT operations
   - Retrieve via GET operations
   - Search via semantic search

5. **Test Persistence**
   - Store data across multiple operations
   - Verify data retrieval
   - Test namespace isolation

### Progression Path

```
Level 1: Basic Store Operations
    ↓ [_ltm_basics.ipynb]
    │ - Namespace creation
    │ - PUT/GET/SEARCH operations
    │ - Semantic search fundamentals
    │
    ├─→ Level 2: Personalized Chat with Memory (First Try)
    │       [_ltm_implementation.ipynb]
    │       - LangGraph integration
    │       - Automatic memory extraction
    │       - Personalized responses
    │       - Issue: Duplicates stored
    │
    └─→ Level 3: Smart De-duplication (Production Ready)
            [_ltm_no_deupliicate_mem.ipynb]
            - Duplicate detection
            - Structured decision-making
            - Clean memory storage
            - Novelty-aware extraction
```

---

## 🎯 Key Takeaways

1. **🧠 LTM = Persistent Knowledge Storage**: Unlike STM, LTM survives beyond single conversations
2. **Namespaces = Data Organization**: Hierarchical tuples organize and isolate related data
3. **Key-Value Model = Flexible Storage**: Store any data type (objects, strings, lists, numbers)
4. **Semantic Search = Intelligent Retrieval**: Find related data using AI embeddings
5. **Scalable Architecture**: Design namespaces for growth and maintainability

---

## 📚 Learning Path

1. **Start Here**: [`_ltm_basics.ipynb`](_ltm_basics.ipynb) — Understand store initialization, namespaces, and basic operations
2. **Next**: [`_ltm_implementation.ipynb`](_ltm_implementation.ipynb) — Learn LangGraph integration and memory extraction (identify the duplicate issue)
3. **Advanced**: [`_ltm_no_deupliicate_mem.ipynb`](_ltm_no_deupliicate_mem.ipynb) — Master smart de-duplication and production-ready patterns
4. **Expert**: Design your own cross-conversation knowledge management systems with custom de-duplication strategies

---

## 🔧 Troubleshooting

### Issue: Data not persisting
**✅ Solution**: Verify InMemoryStore is created once and reused across operations. In-memory storage clears on app restart; for persistence, use database-backed store.

### ❓ Issue: Namespace conflicts
**✅ Solution**: Use consistent, hierarchical naming. Ensure namespace tuples are unique for different data types.

### ❓ Issue: Semantic search returns irrelevant results
**✅ Solution**: Verify embeddings model is properly initialized. Check query text relevance to stored data. Adjust similarity threshold if needed.

### ❓ Issue: API errors with embedding model
**✅ Solution**: Verify API key in `.env` file. Confirm model name matches provider's available models. Check API rate limits.

---

## 📖 Related Documentation

- [LangGraph Store Documentation](https://python.langchain.com/docs/langgraph)
- [LangChain Embeddings](https://python.langchain.com/docs/concepts/embedding)
- [Semantic Search Concepts](https://www.langchain.com/docs/concepts/semantic_search)
- [Vector Databases Overview](https://www.langchain.com/docs/concepts/vectorstores)
- [STM README](./STM_README.md) — Short-term memory reference

---

## ✅ Checklist for LTM Implementation

**Foundation Level** (from `_ltm_basics.ipynb`):
- [ ] 📦 Install required dependencies (langraph, langchain, embeddings model)
- [ ] 🔑 Set up API keys in `.env` file
- [ ] 💾 Initialize InMemoryStore with embeddings
- [ ] 📂 Design namespace hierarchy
- [ ] ➕ Implement PUT operations for sample data
- [ ] 🔍 Test GET operations
- [ ] ✓ Verify namespace isolation
- [ ] 🔎 Implement semantic search

**Memory Extraction Level** (from `_ltm_implementation.ipynb`):
- [ ] 🔗 Integrate LTM store with LangGraph
- [ ] 🧩 Build chat node that accesses memory store
- [ ] 🧠 Implement automatic memory extraction from user messages
- [ ] 🎨 Create personalized system prompt with retrieved memories
- [ ] ✔️ Test end-to-end chat with memory context

**De-duplication Level** (from `_ltm_no_deupliicate_mem.ipynb`):
- [ ] 🏗️ Create Pydantic models for MemoryItem and MemoryDecision
- [ ] 🤖 Build memory extractor with structured output
- [ ] 🔄 Implement duplicate detection logic
- [ ] 🧹 Filter memories by `is_new` flag
- [ ] 💎 Store only genuinely new information
- [ ] 📊 Test de-duplication with repeated messages
- [ ] 🔐 Verify memory store contains no redundant entries

**Production Ready**:
- [ ] 📦 Plan database-backed persistence for reliability
- [ ] 👤 Design user-specific memory management
- [ ] 🧹 Implement memory aging/cleanup policies
- [ ] 🔗 Test cross-conversation memory consistency
- [ ] 📈 Monitor memory growth and storage efficiency

---

### 🌈 **Ready to build persistent knowledge systems!**

Happy coding! 🚀 💾 ✨
