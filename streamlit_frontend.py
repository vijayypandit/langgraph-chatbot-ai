import streamlit as st
from langgraph_backend import chatbot
from langchain_core.messages import HumanMessage
import importlib
import ui_config as ui

# reload UI module so edits appear during Streamlit reloads
importlib.reload(ui)

# Setup page configuration and styling
ui.setup_page_config()
ui.setup_custom_css()

# Initialize session state
if 'message_history' not in st.session_state:
    st.session_state['message_history'] = []

CONFIG = {'configurable': {'thread_id': 'thread-1'}}

# Render sidebar
ui.render_sidebar()

# Render header
ui.render_header()

# Render chat display
ui.render_chat_display()

# Input section
st.markdown("---")
col1, col2 = st.columns([5, 1])

with col1:
    user_input = st.chat_input("✉️ Type your message here...", key="user_input")

with col2:
    send_button = st.button("📤 Send", use_container_width=True)

# Process user input
if user_input or send_button:
    if user_input:
        # Add user message to history
        st.session_state['message_history'].append({'role': 'user', 'content': user_input})
        
        # Get response from chatbot
        with st.spinner("🤔 Thinking..."):
            try:
                response = chatbot.invoke(
                    {'messages': [HumanMessage(content=user_input)]}, 
                    config=CONFIG
                )
                ai_message = response['messages'][-1].content
                
                # Add assistant message to history
                st.session_state['message_history'].append({'role': 'assistant', 'content': ai_message})
                
                st.success("✅ Response generated!")
                st.rerun()
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")

# Render footer
ui.render_footer()

