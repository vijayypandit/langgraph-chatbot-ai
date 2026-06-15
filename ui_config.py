import streamlit as st

def setup_page_config():
    """Configure Streamlit page settings"""
    st.set_page_config(
        page_title="🤖 LangGraph ChatBot",
        page_icon="🤖",
        layout="wide",
        initial_sidebar_state="expanded"
    )

def setup_custom_css():
    """Apply custom CSS styling"""
    # Always use dark theme
    bg = '#0b1220'
    panel = '#0f1724'
    text = '#e6eef8'
    subtext = '#a8b3c7'
    assistant_bg = '#14222b'

    st.markdown(f"""
    <style>
        :root {{
            --app-bg: {bg};
            --panel-bg: {panel};
            --text-color: {text};
            --subtext-color: {subtext};
        }}
        .main-header {{
            text-align: left;
            color: var(--text-color);
            font-size: 1.8rem;
            font-weight: 700;
            margin: 0 0 0.25rem 0;
            display:flex;
            align-items:center;
            gap:12px;
        }}
        .app-logo {{
            width:42px;
            height:42px;
            border-radius:8px;
            background: linear-gradient(135deg,#ff7f0e 0%, #ffb380 100%);
            display:inline-block;
            box-shadow: 0 4px 12px rgba(0,0,0,0.08);
            color: white;
            font-weight:700;
            text-align:center;
            line-height:42px;
        }}
        .subtitle {{
            color: var(--subtext-color);
            font-size: 0.95rem;
            margin-bottom: 1rem;
        }}
        .card {{
            background: var(--panel-bg);
            padding: 12px;
            border-radius: 10px;
            box-shadow: 0 6px 18px rgba(11,34,64,0.04);
            margin-bottom: 12px;
        }}
        .chat-space {{
            margin-bottom: 1rem;
        }}
        .user-message {{
            background-color: #ff7f0e;
            color: white;
            border-radius: 8px;
            padding: 12px;
            margin-bottom: 10px;
            text-align: left;
            margin-left: 20%;
        }}
        .assistant-message {{
            background-color: {assistant_bg};
            color: var(--text-color);
            border-radius: 8px;
            padding: 12px;
            margin-bottom: 10px;
            text-align: left;
            margin-right: 20%;
        }}
        .message-count {{
            text-align: center;
            color: var(--subtext-color);
            font-size: 0.85em;
            margin-top: 1rem;
        }}
        /* style the input area */
        .stButton>button{{
            background: linear-gradient(90deg,#ff7f0e,#ffb380);
            color: white;
            border: none;
        }}
    </style>
    """, unsafe_allow_html=True)

def render_header():
    """Render main header"""
    # logo (simple gradient box with initials) and title
    st.markdown(
        '<div class="main-header"><span class="app-logo">LG</span><div style="display:inline-block"><div>LangGraph ChatBot</div><div class="subtitle">Conversational assistant powered by LangChain & Groq</div></div></div>',
        unsafe_allow_html=True
    )

def render_sidebar():
    """Render sidebar with settings and stats"""
    with st.sidebar:
        st.markdown("### 🎯 Chat Settings")
        st.markdown("---")

        # Small app card
        st.markdown('<div class="card"><strong>LangGraph</strong><br/><small>Smart chat assistant</small></div>', unsafe_allow_html=True)

        # Model selector (informational)
        st.markdown("**Model**")
        model = st.selectbox("", ["Llama 3.1 8B (Groq)"], index=0, help="Model used for responses (info only)")

        # Thread id
        thread_id = st.text_input("Thread ID", value=st.session_state.get('thread_id','thread-1'))
        st.session_state['thread_id'] = thread_id

        st.markdown("---")
        st.markdown("**Theme**")
        st.write("Dark mode only")
        st.markdown("---")

        # Statistics
        st.markdown(f"### 📊 Statistics")
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Total", len(st.session_state['message_history']))
        with col2:
            user_count = sum(1 for m in st.session_state['message_history'] if m['role'] == 'user')
            st.metric("You", user_count)

        st.markdown("---")

        # Actions
        if st.button("🗑️ Clear Chat History", use_container_width=True):
            st.session_state['message_history'] = []
            st.success("Chat history cleared!")
            st.rerun()

        if st.button("⬆️ Export Chat", use_container_width=True):
            st.info("Export feature coming soon")

        st.markdown("---")

        # About / Credits
        st.markdown("### ℹ️ About")
        st.caption("This demo uses LangGraph to orchestrate LLM calls.\nDesigned for desktop use.")

def render_chat_display():
    """Render chat message display"""
    # Render messages directly on the main page (no outer container)
    if len(st.session_state['message_history']) == 0:
        st.info("👋 Start a conversation by typing a message below!")
    else:
        for message in st.session_state['message_history']:
            if message['role'] == 'user':
                st.markdown(f'<div class="chat-space user-message">👤 You: {message["content"]}</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="chat-space assistant-message">🤖 AI Assistant: {message["content"]}</div>', unsafe_allow_html=True)

def render_footer():
    """Render footer with message count"""
    st.markdown("---")
    st.markdown('<div class="message-count">💬 Messages in this session: {}</div>'.format(len(st.session_state['message_history'])), unsafe_allow_html=True)
    st.markdown('<div style="text-align: center; color: #999; font-size: 0.8em; margin-top: 1rem;">Built with Streamlit, LangChain & LangGraph</div>', unsafe_allow_html=True)
