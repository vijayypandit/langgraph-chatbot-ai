import streamlit as st


def setup_page_config():
    """Configure Streamlit page settings"""
    st.set_page_config(
        page_title=" LangGraph ChatBot 🤖",
        page_icon="🤖",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    if 'message_history' not in st.session_state:
        st.session_state['message_history'] = []


def setup_custom_css():
    """Apply custom CSS styling"""
    bg = '#0b1220'
    surface = '#111827'
    panel = '#161f2e'
    text = '#f8fafc'
    subtext = '#94a3b8'
    accent = '#7c3aed'
    muted = '#64748b'
    shadow = 'rgba(15, 23, 42, 0.35)'

    st.markdown(f"""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Jakarta+Sans:wght@400;500;600;700;800&display=swap');

        :root {{
            --page-bg: {bg};
            --surface: {surface};
            --panel: {panel};
            --text: {text};
            --subtext: {subtext};
            --accent: {accent};
            --muted: {muted};
            --shadow: 0 24px 60px {shadow};
            font-family: 'Jakarta Sans', 'Inter', system-ui, sans-serif;
        }}

        .css-1d391kg {{
            background: var(--page-bg) !important;
        }}

        .stApp {{
            background: radial-gradient(circle at top left, rgba(124, 58, 237, 0.18), transparent 28%),
                        radial-gradient(circle at bottom right, rgba(59, 130, 246, 0.16), transparent 22%),
                        var(--page-bg);
            color: var(--text);
            font-family: 'Jakarta Sans', 'Inter', system-ui, sans-serif;
        }}

        .main-header {{
            display: grid;
            grid-template-columns: auto 1fr;
            align-items: center;
            gap: 1rem;
            padding: 1rem 0 0.5rem;
        }}

        .app-logo {{
            width: 58px;
            height: 58px;
            border-radius: 18px;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            background: linear-gradient(135deg, rgba(124,58,237,1), rgba(59,130,246,1));
            color: white;
            font-weight: 800;
            font-size: 1.3rem;
            box-shadow: 0 18px 40px rgba(59, 130, 246, 0.18);
        }}

        .hero-title {{
            margin: 0;
            color: var(--text);
            font-size: 2.6rem;
            line-height: 1.05;
            font-weight: 800;
        }}

        .hero-subtitle {{
            margin-top: 0.55rem;
            color: var(--subtext);
            font-size: 1rem;
            max-width: 680px;
        }}

        .chat-shell {{
            background: rgba(255,255,255,0.04);
            border: 1px solid rgba(255,255,255,0.08);
            border-radius: 28px;
            padding: 1.5rem;
            box-shadow: 0 20px 45px rgba(0,0,0,0.12);
            backdrop-filter: blur(18px);
        }}

        .chat-window {{
            min-height: 520px;
            max-height: 72vh;
            overflow-y: auto;
            padding-right: 12px;
        }}

        .sidebar-textarea textarea {{
            min-height: 80px !important;
            border-radius: 16px !important;
            padding: 1rem !important;
            background: rgba(255,255,255,0.05) !important;
            color: var(--text) !important;
            border: 1px solid rgba(255,255,255,0.12) !important;
        }}

        .chat-space {{
            margin-bottom: 1rem;
        }}

        .assistant-message, .user-message {{
            display: inline-block;
            border-radius: 24px;
            padding: 16px 18px;
            line-height: 1.6;
            font-size: 1rem;
            max-width: 78%;
            box-shadow: 0 16px 30px rgba(0,0,0,0.08);
            position: relative;
            word-break: break-word;
        }}

        .assistant-message {{
            background: linear-gradient(180deg, rgba(17, 24, 39, 0.98), rgba(31, 41, 55, 0.95));
            color: var(--text);
            margin-bottom: 1rem;
        }}

        .assistant-message::before {{
            content: '🤖';
            position: absolute;
            left: -32px;
            top: 16px;
            font-size: 1.1rem;
        }}

        .user-message {{
            background: linear-gradient(180deg, rgba(79, 70, 229, 0.95), rgba(96, 165, 250, 0.95));
            color: white;
            margin-left: auto;
            margin-bottom: 1rem;
        }}

        .user-message::after {{
            content: '👤';
            position: absolute;
            right: -32px;
            top: 16px;
            font-size: 1.1rem;
        }}

        .status-strip {{
            display: grid;
            grid-template-columns: repeat(3, minmax(0, 1fr));
            gap: 1rem;
            margin: 1rem 0 1.5rem;
        }}

        .status-card {{
            background: var(--surface);
            border: 1px solid rgba(255,255,255,0.08);
            border-radius: 20px;
            padding: 1rem 1.2rem;
            box-shadow: 0 18px 36px rgba(0,0,0,0.08);
        }}

        .status-title {{
            margin: 0 0 0.4rem;
            font-size: 0.9rem;
            color: var(--subtext);
            text-transform: uppercase;
            letter-spacing: 0.08em;
        }}

        .status-value {{
            margin: 0;
            font-size: 1.35rem;
            font-weight: 700;
            color: var(--text);
        }}

        .input-panel {{
            background: var(--surface);
            border-radius: 24px;
            padding: 1rem;
            border: 1px solid rgba(255,255,255,0.1);
            box-shadow: 0 18px 32px rgba(0,0,0,0.08);
        }}

        .stTextInput>div>div>input, .stTextArea>div>div>textarea {{
            border-radius: 18px !important;
            border: 1px solid rgba(148, 163, 184, 0.24) !important;
            padding: 1rem 1.1rem !important;
            min-height: 58px;
            font-size: 1rem;
            background: rgba(255,255,255,0.06) !important;
            color: var(--text) !important;
        }}

        .stButton>button {{
            background: linear-gradient(90deg, var(--accent), #4f46e5) !important;
            color: white !important;
            border: none !important;
            border-radius: 999px !important;
            padding: 0.95rem 1.6rem !important;
            font-weight: 700 !important;
            box-shadow: 0 16px 30px rgba(79, 70, 229, 0.2) !important;
        }}

        .stButton>button:hover {{
            opacity: 0.96 !important;
            transform: translateY(-1px);
        }}

        .footer-note {{
            text-align: center;
            color: var(--subtext);
            margin: 1.5rem 0 0;
            font-size: 0.9rem;
        }}

        .streamlit-expanderHeader {{
            font-weight: 700 !important;
        }}
    </style>
    """, unsafe_allow_html=True)


def render_header():
    """Render main header"""
    st.markdown(
        '<div class="main-header"><span class="app-logo">AI</span><div><h1 class="hero-title">🤖 LangGraph ChatBot 🤖</h1></div></div>',
        unsafe_allow_html=True
    )


def render_sidebar():
    """Render sidebar with settings and stats"""
    with st.sidebar:
        st.markdown("🛠️ Settings 🛠️")
        st.markdown("---")

        st.markdown('### Conversation ❤️📚')
        st.markdown('<div class="status-card"><p class="status-title">Messages 🚀 </p><p class="status-value">{}</p></div>'.format(len(st.session_state['message_history'])), unsafe_allow_html=True)
        st.markdown('<div class="status-card"><p class="status-title">User messages 📨</p><p class="status-value">{}</p></div>'.format(sum(1 for m in st.session_state['message_history'] if m['role'] == 'user')), unsafe_allow_html=True)
        st.markdown('<div class="status-card"><p class="status-title">Assistant replies 🤖</p><p class="status-value">{}</p></div>'.format(sum(1 for m in st.session_state['message_history'] if m['role'] == 'assistant')), unsafe_allow_html=True)

        st.markdown("---")
        if st.button("Clear chat history", use_container_width=True):
            st.session_state['message_history'] = []
            st.session_state.thread_id = str(uuid.uuid4())
            st.success("Chat history cleared")
            st.rerun()

        if st.button("Export conversation", use_container_width=True):
            st.info("Export is not implemented yet")

        st.markdown("---")
        st.markdown("### About")
        st.caption("A modern desktop chat UI using Streamlit and LangGraph. Improve, iterate, and refine the visual experience.")


def render_chat_display():
    """Render chat message display"""
    if len(st.session_state['message_history']) > 0:
        for message in st.session_state['message_history']:
            if message['role'] == 'user':
                st.markdown(
                    f'<div class="chat-space user-message"><strong>User :</strong> {message["content"]}</div>',
                    unsafe_allow_html=True
                )
            else:
                st.markdown(
                    f'<div class="chat-space assistant-message"><strong>AI Assistant:</strong> {message["content"]}</div>',
                    unsafe_allow_html=True
                )


def render_footer():
    """Render footer with message count"""
    st.markdown('<div class="footer-note">Built with Streamlit, LangChain, and LangGraph · Designed for clean desktop chat workflows.</div>', unsafe_allow_html=True)
