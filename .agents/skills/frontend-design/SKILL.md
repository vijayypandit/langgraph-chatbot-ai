# Frontend Design Skill — Langgraph Chatbot

Purpose
- Capture frontend requirements and produce a Streamlit-based frontend design and starter implementation for the Langgraph Chatbot.

Captured requirements (from user)
- Primary goal: Chat-only (simple chat UI)
- Pages: Chat
- Theme: Light + Dark toggle
- Branding: Pick a palette (developer will choose)
- Interactivity: Real-time (live typing / streaming responses)
- Responsiveness: Desktop-only
- Framework: Streamlit
- Deliverables: Skill + full frontend implementation

Deliverables produced by this skill
- A written skill specification (this file) summarizing requirements.
- Wireframe and component list describing UI structure.
- Streamlit template components and CSS to integrate with `streamlit_frontend.py`.
- Minimal working demo code that connects to existing backend endpoints in the repo.

Component list / Wireframe (desktop)
- Header: app title + theme toggle
- Chat window (main): scrollable message list, message bubbles (user vs bot)
- Input area: text input, send button, optional file upload
- Status area: model/connection status, streaming indicator (typing)

UX Details
- Streaming responses: use Streamlit's `st.empty()` and `.write()` to progressively render tokens.
- Theme toggle: store selection in session state and swap a small CSS file or inline styles.
- Message history: keep limited in session state, allow clearing.

Implementation plan
1. Add `assets/styles.css` with light/dark variants and small bubble styles.
2. Update `streamlit_frontend.py` to consume the existing backend (e.g. `langgraph_backend.py`) endpoints, implement streaming display, and theme toggle.
3. Add helper `ui.py` module with reusable components: `render_message()`, `render_chat_window()`, `render_input()`.
4. Add a `demo` flag and small README section showing how to run locally.

Files to create (suggested)
- `.agents/skills/frontend-design/SKILL.md` (this file)
- `frontend_ui.py` — reusable Streamlit UI helpers
- `assets/styles.css` — application styles
- `streamlit_frontend_template.py` — optional template (small changes to existing `streamlit_frontend.py`)

How to run / test (developer)
```powershell
cd E:\Projects\Project1Demo\Langgraph-ChatBot
python -m venv venv
.\venv\Scripts\activate.bat
pip install -r requirements.txt
streamlit run streamlit_frontend.py
```

Notes and assumptions
- This skill assumes the backend exposes an HTTP or function API the frontend can call to send/receive messages (if not, the template will include a stubbed local echo mode).
- Desktop-only simplifies responsive CSS.

Next steps I can take now
- Generate `frontend_ui.py` + `assets/styles.css` and a modified `streamlit_frontend.py` template implementing streaming chat.
- Or, if you prefer, I can first produce wireframe images or Figma-ready specs.

Please confirm which next step you want me to take.