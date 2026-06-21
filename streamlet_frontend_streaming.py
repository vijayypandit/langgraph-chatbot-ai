import streamlit as st
from langgraph_backend import chatbot
from langchain_core.messages import HumanMessage
import importlib
# import ui_config as ui
import uuid


# # reload UI module so edits appear during Streamlit reloads
# importlib.reload(ui)

# # Setup page configuration and styling
# ui.setup_page_config()
# ui.setup_custom_css()
# ******************************Util Setup ***********************************
def generate_thread_id():
    thread_id = uuid.uuid4()
    return thread_id

def reset_chat():
    thread_id = generate_thread_id()
    st.session_state['thread_id']=thread_id
    add_thread(st.session_state['thread_id'])
    st.session_state['message_history']=[]

def add_thread(thread_id):
    if thread_id not in st.session_state['chat_threads']:
        st.session_state['chat_threads'].append(thread_id)

def load_conversation(thread_id):
    return chatbot.get_state(config={'configurable':{'thread_id':thread_id}}).values['messages']

# ******************************Session Setup ***********************************
if 'message_history' not in st.session_state:
    st.session_state['message_history'] = []

if 'thread_id' not in st.session_state:
    st.session_state['thread_id'] = generate_thread_id()

if 'chat_threads' not in st.session_state:
    st.session_state['chat_threads'] = []

add_thread(st.session_state['thread_id'])


#******************************SIDEBAR UI****************************************
st.sidebar.title('LangGraph Chatbot')

if st.sidebar.button('New Chat'):
    reset_chat()

st.sidebar.header('My Conversations')

for thread_id in st.session_state['chat_threads']:
    if st.sidebar.button(str(thread_id)):
        st.session_state['thread_id'] = thread_id
        messages = load_conversation(thread_id)

        temp_messages = []
        for message in messages:
            if isinstance(message, HumanMessage):
                role = 'user'
            else:
                role='assistant'
            temp_messages.append({'role':role,'content':message.content})


        st.session_state['message_history'] = temp_messages

        
# st.sidebar.text(st.session_state['thread_id'])

#Loading conversation history
for message in st.session_state['message_history']:
    with st.chat_message(message['role']):
        st.text(message['content'])

# Render sidebar
# ui.render_sidebar()

# Main screen
# st.markdown("<div style='padding-top: 1rem;'></div>", unsafe_allow_html=True)
# ui.render_header()
# ui.render_chat_display()

# st.markdown("---")

user_input = st.chat_input("Ask Anything ...")

if user_input:
    st.session_state['message_history'].append({'role': 'user', 'content': user_input.strip()})
    # with st.chat_message('User : '):
    st.write(user_input)
    # with st.spinner('🤖 Generating Response...'):
    CONFIG= {'configurable':{'thread_id':st.session_state['thread_id']}}
    
    with st.chat_message('Assistant : '):
        ai_message = st.write_stream(
            message_chunk.content for message_chunk , metadata in chatbot.stream(
                {'messages': [HumanMessage(content=user_input)]}, 
                config=CONFIG,
                stream_mode='messages'
            )
        )
    st.session_state['message_history'].append({'role': 'assistant', 'content': ai_message})
    # st.rerun()
    
# ui.render_footer()

