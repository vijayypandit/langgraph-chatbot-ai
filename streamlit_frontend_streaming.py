import streamlit as st
from langgraph_backend import chatbot
from langchain_core.messages import HumanMessage
import importlib
import uuid

# ==============================================================================
# Utility & Helper Functions
# ==============================================================================

def generate_thread_id():
    """Generates a unique identifier (UUID) representing a unique conversation thread."""
    return uuid.uuid4()

def reset_chat():
    """Starts a new conversation thread, generating a new ID and resetting the UI message history."""
    thread_id = generate_thread_id()
    st.session_state['thread_id'] = thread_id
    add_thread(st.session_state['thread_id'])
    st.session_state['message_history'] = []

def add_thread(thread_id):
    """Tracks the thread ID in our global active conversations list if it isn't already present."""
    if thread_id not in st.session_state['chat_threads']:
        st.session_state['chat_threads'].append(thread_id)

def load_conversation(thread_id):
    """Retrieves all past messages associated with a specific thread ID from LangGraph checkpointer."""
    return chatbot.get_state(config={'configurable': {'thread_id': thread_id}}).values['messages']

# ==============================================================================
# Streamlit Session State Setup
# ==============================================================================

# Initialize UI-visible message history
if 'message_history' not in st.session_state:
    st.session_state['message_history'] = []

# Initialize active conversation thread ID
if 'thread_id' not in st.session_state:
    st.session_state['thread_id'] = generate_thread_id()

# Initialize list of all created threads
if 'chat_threads' not in st.session_state:
    st.session_state['chat_threads'] = []

# Register the current active thread in the list of conversations
add_thread(st.session_state['thread_id'])

# ==============================================================================
# Sidebar UI - Thread & Session Manager
# ==============================================================================
st.sidebar.title('LangGraph Chatbot')

# Button to spawn a brand new conversation thread
if st.sidebar.button('New Chat'):
    reset_chat()

st.sidebar.header('My Conversations')

# Render buttons for all active/previous threads to allow quick switching
for thread_id in st.session_state['chat_threads']:
    if st.sidebar.button(str(thread_id)):
        # Switch current active thread
        st.session_state['thread_id'] = thread_id
        
        # Load messages from checkpointer state and update frontend state history
        messages = load_conversation(thread_id)
        temp_messages = []
        for message in messages:
            if isinstance(message, HumanMessage):
                role = 'user'
            else:
                role = 'assistant'
            temp_messages.append({'role': role, 'content': message.content})

        st.session_state['message_history'] = temp_messages

# ==============================================================================
# Main Chat Display (Renders historical messages)
# ==============================================================================
for message in st.session_state['message_history']:
    with st.chat_message(message['role']):
        st.text(message['content'])

# Get user input from the chat bar
user_input = st.chat_input("Ask Anything ...")

# ==============================================================================
# Message Submission & Real-time Output Streaming
# ==============================================================================
if user_input:
    # Save and display user message immediately
    st.session_state['message_history'].append({'role': 'user', 'content': user_input.strip()})
    st.write(user_input)
    
    # Construct the config dictionary pointing to the active thread
    CONFIG = {'configurable': {'thread_id': st.session_state['thread_id']}}
    
    # Stream the response chunks from the chatbot and write them in real-time
    with st.chat_message('Assistant : '):
        ai_message = st.write_stream(
            message_chunk.content for message_chunk, metadata in chatbot.stream(
                {'messages': [HumanMessage(content=user_input)]}, 
                config=CONFIG,
                stream_mode='messages'
            )
        )
    
    # Save the assistant response in history for display persistence
    st.session_state['message_history'].append({'role': 'assistant', 'content': ai_message})


