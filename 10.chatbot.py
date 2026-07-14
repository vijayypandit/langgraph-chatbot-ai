from langgraph_database_backend import chatbot, retrieve_all_threads
from langgraph.prebuilt import ToolNode, tools_condition
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_core.tools import tool
from langchain_groq import ChatGroq
from langchain_core.messages import BaseMessage , HumanMessage
from langgraph.graph import StateGraph, START, END
from typing import Annotated, TypedDict
from pydantic import BaseModel, Field
from langgraph.graph.message import add_messages
from dotenv import load_dotenv
import sqlite3 
from langgraph.checkpoint.sqlite import SqliteSaver
import os
import requests

# Load environment variables from .env file
load_dotenv(override=True)

# Ensure the Groq API key is set in the environment
os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")

# Initialize the Groq Chat LLM with streaming mode enabled
llm_model = ChatGroq(model="llama-3.3-70b-versatile", streaming=True)

#Tools
# 
search_tool = DuckDuckGoSearchRun() 


@tool
def calculator(first_num:float,second_num:float,operation:str) -> dict:
    """
    Perform a basic arithmetic operation on two numbers.
    If the user asks for '+' or 'plus', it means addition.
    If the user asks for '-' or 'minus', it means subtraction.
    Supported inputs include: 'add', '+', 'plus', 'subtract', '-', 'minus', 'multiply', '*', 'divide', '/'.
    """

    try:
        normalized_operation = str(operation).strip().lower()

        if normalized_operation in {"add", "+", "plus"}:
            result = first_num + second_num
        elif normalized_operation in {"sub", "subtract", "-", "minus"}:
            result = first_num - second_num
        elif normalized_operation in {"mul", "multiply", "*", "times"}:
            result = first_num * second_num
        elif normalized_operation in {"div", "divide", "/"}:
            if second_num == 0:
                return {"error": "Division by zero is not allowed."}
            result = first_num / second_num
        else:
            return {"error": "Invalid operation. Please choose from 'add'/'+', 'subtract'/'-', 'multiply'/'*', or 'divide'/'/'"}

        return {"first_num":first_num, "second_num":second_num, "operation":normalized_operation, "result":result}
    except Exception as e:
        return {"error": str(e)}

tools = [search_tool, calculator]

llm_with_tools = llm_model.bind_tools(tools)

# Conversational state schema using add_messages reducer
class ChatState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]

#graph nodes:
def chat_node(state:ChatState):
    """ LLM node that may answer or request a tool call. """
    messages = state['messages']
    response = llm_with_tools.invoke(messages)
    return {"messages": [response]}

tool_node = ToolNode(tools)

# create database connection wil use this same thraed in diff dbs
conn = sqlite3.connect(database='chatbot.db',check_same_thread=False)
checkpointer = SqliteSaver(conn=conn)

#Graph structure
graph = StateGraph(ChatState)
graph.add_node("chat_node",chat_node)
graph.add_node("tools",tool_node)

graph.add_edge(START,"chat_node")
#if the LLM asked for a tool . go to theToolNode: else finish
graph.add_conditional_edges("chat_node", tools_condition)
graph.add_edge("tools","chat_node")


chatbot = graph.compile(checkpointer=checkpointer)

result = chatbot.invoke({"messages":[HumanMessage(content="Find the modulous of 12345 and 23 and give answer like a cricket commentator")]})

print(result['messages'][-1].content)