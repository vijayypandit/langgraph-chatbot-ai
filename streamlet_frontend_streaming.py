import streamlit as st
from langgraph_backend import chatbot
from langchain_core.messages import HumanMessage
import importlib
import ui_config as ui
import uuid


# reload UI module so edits appear during Streamlit reloads
importlib.reload(ui)

# Setup page configuration and styling
ui.setup_page_config()
ui.setup_custom_css()

# Create a unique thread id per user session
CONFIG = {'configurable': {'thread_id': st.session_state.get('thread_id', 'thread-1')}}

# Render sidebar
ui.render_sidebar()

# Main screen
st.markdown("<div style='padding-top: 1rem;'></div>", unsafe_allow_html=True)
ui.render_header()
ui.render_chat_display()

st.markdown("---")

user_input = st.chat_input("Ask Anything ...", key='user_input')

if user_input:
    st.session_state['message_history'].append({'role': 'user', 'content': user_input.strip()})
    # with st.chat_message('User : '):
    st.write(user_input)
    # with st.spinner('🤖 Generating Response...'):
    with st.chat_message('Assistant : '):
        ai_message = st.write_stream(
            message_chunk.content for message_chunk , metadata in chatbot.stream(
                {'messages': [HumanMessage(content=user_input)]}, 
                config=CONFIG,
                stream_mode='messages'
            )
        )
    st.session_state['message_history'].append({'role': 'assistant', 'content': ai_message})
    st.rerun()
    
ui.render_footer()

