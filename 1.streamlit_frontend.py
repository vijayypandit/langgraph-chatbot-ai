import streamlit as st
from langgraph_backend import chatbot
from langchain_core.messages import HumanMessage

# Setup page configuration and styling
st.set_page_config(page_title="LangGraph Chatbot", page_icon="🧠", layout="centered")

# Initialize session state for message history
if 'message_history' not in st.session_state:
    st.session_state['message_history'] = []

# Set up the thread configuration
CONFIG = {'configurable': {'thread_id': st.session_state.get('thread_id', 'thread-1')}}

# Main screen headers
st.title("🧠 LangGraph ChatBot 🤖")
st.markdown("A lightweight conversational interface using LangGraph memory and Groq API.")
st.markdown("---")

# Render chat display natively
for message in st.session_state['message_history']:
    with st.chat_message(message['role']):
        st.write(message['content'])

user_input = st.chat_input("Ask Anything ...", key='user_input')

if user_input:
    # Append and show the user's question
    st.session_state['message_history'].append({'role': 'user', 'content': user_input.strip()})
    
    try:
        with st.spinner('🤖 Generating response...'):
            # Invoke the LangGraph chatbot
            response = chatbot.invoke(
                {'messages': [HumanMessage(content=user_input.strip())]},
                config=CONFIG
            )
            ai_message = response['messages'][-1].content
            # Append the assistant's reply to the message history
            st.session_state['message_history'].append({'role': 'assistant', 'content': ai_message})

        # Reload the page to display the updated chat history
        st.rerun()
    except Exception as e:
        st.error(f"❌ Error generating response: {str(e)}")


