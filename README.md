# 🧠 LangGraph ChatBot (Streamlit + Groq)

A lightweight **LangGraph-powered chatbot** with a polished **Streamlit UI**, supporting **multi-turn conversations using `thread_id`** for continuity. 🤖✨

---

## 🚀 What this project does
- Lets users chat in a browser via **Streamlit**.
- Uses **LangGraph** (`StateGraph`) to manage conversational state.
- Calls the **Groq Llama model** to generate responses.
- Uses LangGraph **checkpointing (`InMemorySaver`)** so messages stay consistent across turns when the same `thread_id` is reused. 🔁

---

## 🧩 Key idea: `thread_id` for conversation continuity
LangGraph checkpointing can keep track of conversation state per **thread**.

In this project:
- The Streamlit frontend generates a `thread_id` (UUID) and stores it in `st.session_state`.
- Every call to the backend includes:
  ```python
  config = {"configurable": {"thread_id": thread_id}}
  ```
- The backend passes that config into `chatbot.invoke(...)`.

✅ Result: each time the user asks a follow-up question, the chatbot continues the same conversation instead of starting fresh.

---

## 🏗️ Architecture & Flow

### High-level flow
```mermaid
flowchart LR
  U[User] -->|Chat input| UI[Streamlit Frontend]
  UI -->|chatbot.invoke / stream| BG[LangGraph Backend]
  BG -->|LLM call| LLM[Groq Llama (llama-3.3-70b-versatile)]
  LLM --> BG
  BG -->|Message output| UI
  UI --> U

  BG -. checkpoint .-> CP[InMemorySaver]
  BG <-->|configurable.thread_id| CP
```

### Conversation flow (one turn)
1. **User sends a message** in the UI.
2. UI wraps the message as a LangChain message (`HumanMessage`).
3. UI calls the LangGraph app with:
   - `{'messages': [HumanMessage(...)]}`
   - `config={'configurable': {'thread_id': <uuid>}}`
4. Backend runs `chat_node`:
   - invokes the Groq model
   - returns the assistant message
5. LangGraph checkpoint stores conversation progress for that `thread_id`.
6. UI renders the assistant response. ✅

---

## 📁 Project structure (key files)

- **`langgraph_backend.py`** 🧠
  - Defines the LangGraph `StateGraph`.
  - Implements `chat_node()` that calls Groq Llama.
  - Compiles the graph with `InMemorySaver()` checkpointing.

- **`streamlit_frontend.py`** 🖥️
  - Streamlit entry point (main UI).
  - Generates/reads `thread_id` from `st.session_state`.
  - Calls `chatbot.invoke(...)` with the `thread_id` config.

- **`streamlet_frontend_streaming.py`** 🌊
  - Alternative streaming-focused frontend.
  - Uses `chatbot.stream(...)` to render partial output.
  - Note: contains a small session-state key mismatch: `threaD_id` (capital **D**). 

- **`ui_config.py`** 🎨
  - Custom Streamlit CSS + UI rendering helpers (header/sidebar/chat layout).

---

## ▶️ How to run

### 1) Install dependencies
```bash
pip install -r requirements.txt
```

### 2) Set environment variables
You need your **Groq API key**:
- Create a `.env` file (project root) with:
  ```env
  GROQ_API_KEY=your_key_here
  ```

### 3) Start the UI
Run the standard (invoke) frontend:
```bash
streamlit run streamlit_frontend.py
```

Or try the streaming frontend:
```bash
streamlit run streamlet_frontend_streaming.py
```

---

## 📝 Notes
- **Checkpointing**: This project currently uses `InMemorySaver()`, meaning conversation continuity works while the app is running (not persisted to disk across restarts).
- **Model**: The backend uses `llama-3.3-70b-versatile` through **Groq**.
- **Streaming frontend**: There is a session-state typo (`threaD_id`). If you want perfect thread continuity there too, align the key name to `thread_id`.

---

## 👏 Built with
- 🤖 LangGraph
- 🧠 LangChain
- 🔥 Groq LLM
- 🖥️ Streamlit

---

If you want, the next improvement would be swapping `InMemorySaver()` with a persistent checkpointer (e.g., SQLite/Redis) so conversations survive restarts. 💾🚀

