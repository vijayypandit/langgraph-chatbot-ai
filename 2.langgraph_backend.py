from langchain_groq import ChatGroq
from langchain_core.messages import BaseMessage
from langgraph.graph import StateGraph, START, END
from typing import Annotated, TypedDict
from pydantic import BaseModel, Field
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph.message import add_messages
from dotenv import load_dotenv
import os

load_dotenv(override=True)
os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")

# Initialize ChatGroq LLM
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

# StateGraph compilation with in-memory checkpointing
checkpointer = InMemorySaver()

graph = StateGraph(ChatState)
graph.add_node("chat_node", chat_node)
graph.add_edge(START, "chat_node")
graph.add_edge("chat_node", END)

chatbot = graph.compile(checkpointer=checkpointer)


