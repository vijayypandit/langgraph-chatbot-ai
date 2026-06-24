# 🧠 LangGraph ChatBot — AI Conversations That Never Forget 🤖✨

> A stateful, multi-turn conversational AI chatbot powered by **LangGraph**, **Groq (Llama 3.3 70B)**, **SQLite persistence**, and a polished **Streamlit** web UI with real-time token streaming.

---

## 🚀 Key Features

- 💾 **Persistent Chat Storage** — Conversations are saved to a local SQLite database (`chatbot.db`). Your chats survive server restarts, browser refreshes, and machine reboots.
- ⚡ **Real-Time Token Streaming** — Watch the AI think in real-time. Tokens are rendered as they arrive from Groq, with typewriter-style streaming output.
- 🔁 **Multi-Turn Memory** — The chatbot retains full context across turns using LangGraph's native checkpointing state machine.
- 📂 **Multi-Thread Conversation Switcher** — Create, switch between, and revisit past conversation threads via the sidebar — all loaded directly from the database.
- 🧠 **LangGraph State Machine** — Deterministic, graph-based dialogue management with a `StateGraph`, typed state schema, and the `add_messages` reducer.
- 🎨 **Premium Dark Mode UI** — Custom-styled Streamlit interface with branded headers, CSS injections, and a clean layout.

---

## 🏗️ Architecture & Flow Diagrams

### 1️⃣ System Interaction Flow (Database-Backed)

This diagram shows how the user, Streamlit frontend, LangGraph backend, and Groq LLM communicate, with SQLite checkpointing at the center:

```mermaid
flowchart LR
  U["👤 User"] -->|Sends Chat Input| UI["🖥️ Streamlit Frontend"]
  UI -->|chatbot.stream with thread config| BG["🧠 LangGraph Database Backend"]
  BG -->|LLM API Request| LLM["⚡ Groq Llama 3.3 70B"]
  LLM -->|Token Stream Response| BG
  BG -->|Renders streamed tokens| UI
  UI -->|Displays to User| U

  BG <-.->|"Saves & Loads Thread State"| CP[("💾 chatbot.db SQLite")]
```

### 2️⃣ LangGraph State Machine (Backend Graph)

This diagram illustrates the internal state graph definition — a simple but powerful single-node graph with checkpointed persistence:

```mermaid
flowchart TD
  START["🟢 START"] -->|"Incoming HumanMessage + thread_id config"| ChatNode["🧠 chat_node"]
  ChatNode -->|"1. Load historical messages from SQLite checkpoint\n2. Call Groq LLM to generate response\n3. Append AIMessage to state"| CP[("💾 SqliteSaver Checkpoint")]
  CP -->|"Persist updated state to chatbot.db"| END_NODE["🔴 END"]
```

---

## 💡 Why SQLite? — The Problem We Solved

### ❌ The Problem: Memory-Only Storage (`InMemorySaver`)

The original version of this chatbot used LangGraph's `InMemorySaver` checkpointer. This means:

| ⚠️ Issue | 📝 What Happens |
|---|---|
| **Server restart** | All conversations are permanently lost |
| **Browser refresh** | Previous thread messages disappear from the sidebar |
| **Multiple sessions** | No way to revisit or continue past conversations |
| **Deployment** | Every deployment wipes the entire chat history |

> [!WARNING]
> With `InMemorySaver`, your chatbot has **amnesia** after every restart. The state lives only in Python process memory — once the process dies, everything is gone.

### ✅ The Solution: SQLite Database Persistence (`SqliteSaver`)

We replaced `InMemorySaver` with `SqliteSaver` from `langgraph-checkpoint-sqlite`. This writes every conversation checkpoint to a local **SQLite database file** (`chatbot.db`), which means:

| ✅ Benefit | 📝 What Changes |
|---|---|
| **Survives restarts** | Conversations persist across server restarts, machine reboots, and crashes |
| **Thread recovery** | All previous thread IDs and their full message histories are recoverable on startup |
| **Zero infrastructure** | SQLite is a single file — no external database server, no Docker, no cloud dependency |
| **Instant setup** | The database file is auto-created on first run. No migrations, no schema setup |
| **Multi-thread support** | Each conversation thread is identified by a unique `thread_id` and stored independently |

> [!IMPORTANT]
> SQLite was chosen because it is **zero-configuration**, **serverless**, and **file-based** — perfect for a local development chatbot. For production deployments with multiple concurrent users, consider upgrading to `PostgresSaver` or `AsyncSqliteSaver`.

### 🔄 Before vs. After Comparison

```mermaid
flowchart LR
  subgraph BEFORE["❌ Before: InMemorySaver"]
    direction TB
    B1["User sends message"] --> B2["State saved in RAM"]
    B2 --> B3["Server restarts"]
    B3 --> B4["💀 All conversations LOST"]
  end

  subgraph AFTER["✅ After: SqliteSaver"]
    direction TB
    A1["User sends message"] --> A2["State saved to chatbot.db"]
    A2 --> A3["Server restarts"]
    A3 --> A4["✅ All conversations RESTORED"]
  end
```

---

## 🗄️ Database Integration Deep Dive: How SQLite Persistence Works

### 1️⃣ The Role of the Checkpointer

In LangGraph, the **checkpointer** is a state persistence layer that sits between the graph execution engine and permanent storage:

- 💾 **Saving State**: Every time a graph node completes execution (like `chat_node`), the checkpointer captures a full snapshot of the current state — including the entire message history — and writes it to `chatbot.db`.
- 📖 **Loading State**: When a new query arrives with a `configurable: {thread_id: ...}` config, the checkpointer intercepts the execution, queries SQLite for the last saved state belonging to that `thread_id`, and loads it back into the graph so the LLM has complete conversational context.

> [!NOTE]
> The checkpointer is **transparent** to the graph logic. The `chat_node` function doesn't know or care whether state comes from memory or a database — it just receives messages and returns a response. This is the power of LangGraph's abstraction.

### 2️⃣ Backend SQLite Setup

In [langgraph_database_backend.py](file:///e:/Projects/Project1Demo/Langgraph-ChatBot/langgraph_database_backend.py), we establish a persistent SQLite connection and wire it into the graph compilation:

```python
import sqlite3
from langgraph.checkpoint.sqlite import SqliteSaver

# Create SQLite database connection
# check_same_thread=False allows Streamlit's multi-threaded runtime to reuse this connection
conn = sqlite3.connect(database='chatbot.db', check_same_thread=False)

# Instantiate the SQLite checkpointer
checkpointer = SqliteSaver(conn=conn)

# Compile the state graph with persistent checkpointing
chatbot = graph.compile(checkpointer=checkpointer)
```

> [!TIP]
> The `check_same_thread=False` flag is **critical** when running with Streamlit. Streamlit's execution model re-runs the script on every interaction from a different thread — without this flag, SQLite raises a `ProgrammingError`.

### 3️⃣ Retrieving Saved Threads

To populate the sidebar with all previously saved conversations on startup, we query the checkpointer for every unique `thread_id` stored in the database:

```python
def retrieve_all_threads():
    all_threads = set()
    for checkpoint in checkpointer.list(None):
        all_threads.add(checkpoint.config['configurable']['thread_id'])
    return list(all_threads)
```

### 4️⃣ Loading a Past Conversation

When the user clicks a thread in the sidebar, we retrieve its full message history directly from the SQLite checkpoint:

```python
def load_conversation(thread_id):
    state = chatbot.get_state(config={'configurable': {'thread_id': thread_id}})
    return state.values.get('messages', [])
```

### 5️⃣ The Database File: `chatbot.db`

- 📍 **Location**: Created automatically in the project root directory on first run
- 📦 **Format**: Standard SQLite3 database file
- 🗃️ **Tables**: Managed internally by `SqliteSaver` — includes `checkpoints` and `checkpoint_writes` tables
- 🔍 **Inspection**: Use the included [view_checkpoints.py](file:///e:/Projects/Project1Demo/Langgraph-ChatBot/view_checkpoints.py) utility to dump all stored threads and messages

```bash
python view_checkpoints.py
```

---

## 🧩 The `thread_id` & Multi-Conversation Frontend

In [streamlit_frontend_database.py](file:///e:/Projects/Project1Demo/Langgraph-ChatBot/streamlit_frontend_database.py), the frontend manages multiple conversation threads powered by SQLite storage:

### 1️⃣ Initializing Thread List from Database

On every app startup, the frontend populates its sidebar thread list directly from `chatbot.db` — so previous conversations are immediately available:

```python
if 'chat_threads' not in st.session_state:
    st.session_state['chat_threads'] = retrieve_all_threads()
```

### 2️⃣ Creating New Conversations

Each new conversation generates a unique UUID as its `thread_id`. This UUID becomes the key that the checkpointer uses to isolate that conversation's state in the database:

```python
def generate_thread_id():
    return uuid.uuid4()

def reset_chat():
    thread_id = generate_thread_id()
    st.session_state['thread_id'] = thread_id
    add_thread(st.session_state['thread_id'])
    st.session_state['message_history'] = []
```

### 3️⃣ Switching Between Threads

Clicking a thread button in the sidebar loads its entire message history from the database checkpoint and updates the frontend display:

```python
for thread_id in st.session_state['chat_threads']:
    if st.sidebar.button(str(thread_id)):
        st.session_state['thread_id'] = thread_id
        messages = load_conversation(thread_id)
        # Convert LangChain message objects to Streamlit display format
        temp_messages = []
        for message in messages:
            role = 'user' if isinstance(message, HumanMessage) else 'assistant'
            temp_messages.append({'role': role, 'content': message.content})
        st.session_state['message_history'] = temp_messages
```

---

## 🌊 Real-Time Streaming Output

Instead of making the user wait for the full assistant response (which can take several seconds for long answers), we stream tokens live as they are generated by Groq.

### 1️⃣ Enabling LLM-Level Streaming

The Groq Chat model is initialized with `streaming=True` to enable token-level output:

```python
llm_model = ChatGroq(model="llama-3.3-70b-versatile", streaming=True)
```

### 2️⃣ Frontend Streaming Implementation

The compiled graph is executed using `chatbot.stream(...)` with `stream_mode='messages'`, which yields `(message_chunk, metadata)` tuples as tokens arrive. Streamlit's `st.write_stream(...)` renders them with a typewriter effect:

```python
with st.chat_message('Assistant : '):
    ai_message = st.write_stream(
        message_chunk.content for message_chunk, metadata in chatbot.stream(
            {'messages': [HumanMessage(content=user_input)]},
            config=CONFIG,
            stream_mode='messages'
        )
    )
```

---

## 📁 Project Structure

| 📄 File | 📝 Description |
|---|---|
| [langgraph_database_backend.py](file:///e:/Projects/Project1Demo/Langgraph-ChatBot/langgraph_database_backend.py) 🗄️ | **SQLite-backed backend** — State graph with `SqliteSaver` checkpointer and `retrieve_all_threads()` query function |
| [streamlit_frontend_database.py](file:///e:/Projects/Project1Demo/Langgraph-ChatBot/streamlit_frontend_database.py) 🌊 | **Database-backed streaming frontend** *(Recommended)* — Loads past threads on launch, streams responses, saves to SQLite |
| [langgraph_backend.py](file:///e:/Projects/Project1Demo/Langgraph-ChatBot/langgraph_backend.py) 🧠 | Legacy memory-only backend using `InMemorySaver` |
| [streamlit_frontend_streaming.py](file:///e:/Projects/Project1Demo/Langgraph-ChatBot/streamlit_frontend_streaming.py) 🖥️ | Legacy memory-only streaming frontend |
| [streamlit_frontend.py](file:///e:/Projects/Project1Demo/Langgraph-ChatBot/streamlit_frontend.py) 🖥️ | Legacy memory-only static (non-streaming) frontend |
| [view_checkpoints.py](file:///e:/Projects/Project1Demo/Langgraph-ChatBot/view_checkpoints.py) 🛠️ | Developer utility — dumps all thread checkpoints and message histories from `chatbot.db` |
| [main.py](file:///e:/Projects/Project1Demo/Langgraph-ChatBot/main.py) 📌 | Basic entry point placeholder |
| [requirements.txt](file:///e:/Projects/Project1Demo/Langgraph-ChatBot/requirements.txt) 📦 | Pip dependency list |
| [pyproject.toml](file:///e:/Projects/Project1Demo/Langgraph-ChatBot/pyproject.toml) ⚙️ | Project metadata and uv/pip dependency specification |
| [.env](file:///e:/Projects/Project1Demo/Langgraph-ChatBot/.env) 🔑 | Environment variables (API keys) — **not tracked in git** |

---

## 🔀 Three Frontend Modes Explained

This project ships with three frontend implementations, each demonstrating a different level of capability:

```mermaid
flowchart TD
  subgraph V3["✅ v3: Database + Streaming (Recommended)"]
    direction LR
    V3F["streamlit_frontend_database.py"] --> V3B["langgraph_database_backend.py"]
    V3B --> V3D[("chatbot.db")]
  end

  subgraph V2["⚡ v2: Memory + Streaming"]
    direction LR
    V2F["streamlit_frontend_streaming.py"] --> V2B["langgraph_backend.py"]
    V2B --> V2M["RAM only"]
  end

  subgraph V1["📦 v1: Memory + Static"]
    direction LR
    V1F["streamlit_frontend.py"] --> V1B["langgraph_backend.py"]
    V1B --> V1M["RAM only"]
  end
```

| Version | Frontend | Backend | Persistence | Streaming | Status |
|---|---|---|---|---|---|
| **v3** ⭐ | `streamlit_frontend_database.py` | `langgraph_database_backend.py` | ✅ SQLite | ✅ Yes | **Recommended** |
| **v2** | `streamlit_frontend_streaming.py` | `langgraph_backend.py` | ❌ RAM only | ✅ Yes | Legacy |
| **v1** | `streamlit_frontend.py` | `langgraph_backend.py` | ❌ RAM only | ❌ No | Legacy |

---

## ▶️ Setup & How to Run

### 1️⃣ Prerequisites

- 🐍 **Python 3.14+** (as specified in `pyproject.toml`)
- 🔑 A **Groq API key** — get one free at [console.groq.com](https://console.groq.com)

### 2️⃣ Install Dependencies

```bash
# Using pip
pip install -r requirements.txt

# Or using uv (recommended)
uv sync
```

### 3️⃣ Configure Environment Variables

Create a `.env` file in the project root directory:

```env
GROQ_API_KEY=your_groq_api_key_here
```

> [!CAUTION]
> Never commit your `.env` file to version control. It is already listed in `.gitignore` to prevent accidental exposure of your API keys.

### 4️⃣ Activate Virtual Environment

```bash
# Windows PowerShell
.\.venv\Scripts\Activate.ps1

# Windows Command Prompt
.\.venv\Scripts\activate.bat

# macOS / Linux
source .venv/bin/activate
```

### 5️⃣ Launch the Application

**Recommended** — Database-backed streaming version:
```bash
streamlit run streamlit_frontend_database.py
```

**Alternative** — Legacy in-memory versions:
```bash
# Streaming (memory-only)
streamlit run streamlit_frontend_streaming.py

# Static (memory-only)
streamlit run streamlit_frontend.py
```

---

## 🛠️ Developer Utilities

### 🔍 Inspect Database Contents

Use the included [view_checkpoints.py](file:///e:/Projects/Project1Demo/Langgraph-ChatBot/view_checkpoints.py) script to inspect all saved threads and their full conversation histories:

```bash
python view_checkpoints.py
```

**Example output:**
```
=== THREAD ID: a1b2c3d4-e5f6-... ===
[*] Checkpoint: ckpt_abc123
  - HUMAN: What is LangGraph?
  - AI: LangGraph is a framework for building stateful...

=== THREAD ID: f7g8h9i0-j1k2-... ===
[*] Checkpoint: ckpt_def456
  - HUMAN: Explain quantum computing
  - AI: Quantum computing leverages quantum mechanical...
```

---

## 🗺️ Roadmap & Future Improvements

- 🐘 **PostgreSQL support** — Replace SQLite with `PostgresSaver` for production multi-user deployments
- 🔐 **User authentication** — Add login/session management so threads are private per user
- 📝 **Thread naming** — Auto-generate descriptive thread names from the first message instead of showing raw UUIDs
- 🔄 **Async checkpointing** — Migrate to `AsyncSqliteSaver` for non-blocking database writes
- 📊 **Usage analytics** — Track token counts, response times, and conversation lengths
- 🧹 **Thread management** — Add ability to delete, rename, or archive old conversations

---

> Built with ❤️ using [LangGraph](https://langchain-ai.github.io/langgraph/) · [Groq](https://groq.com/) · [Streamlit](https://streamlit.io/) · [SQLite](https://www.sqlite.org/)
