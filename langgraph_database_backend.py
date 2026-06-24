from langchain_groq import ChatGroq
from langchain_core.messages import BaseMessage , HumanMessage
from langgraph.graph import StateGraph, START, END
from typing import Annotated, TypedDict
from pydantic import BaseModel, Field
from langgraph.checkpoint.sqlite import SqliteSaver
import sqlite3
from langgraph.graph.message import add_messages
from dotenv import load_dotenv
import os
import time

# Load environment variables from .env file
load_dotenv(override=True)

# Ensure the Groq API key is set in the environment
os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")

# Initialize the Groq Chat LLM with streaming mode enabled
llm_model = ChatGroq(model="llama-3.3-70b-versatile", streaming=True)
print(f"Using model: {llm_model.model_name}")

# Conversational state schema using add_messages reducer
class ChatState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]

# Graph Node
def chat_node(state: ChatState):
    messages = state['messages']
    response = llm_model.invoke(messages)
    return {"messages": [response]}

# create database connection wil use this same thraed in diff dbs

conn = sqlite3.connect(database='chatbot.db',check_same_thread=False)

# StateGraph compilation with in-memory checkpointing
checkpointer = SqliteSaver(conn=conn)

graph = StateGraph(ChatState)
graph.add_node("chat_node", chat_node)
graph.add_edge(START, "chat_node")
graph.add_edge("chat_node", END)

chatbot = graph.compile(checkpointer=checkpointer)

def retrieve_all_threads():
    all_threads = set()
    for checkpoint in  checkpointer.list(None):
        all_threads.add(checkpoint.config['configurable']['thread_id'])

    return list(all_threads)