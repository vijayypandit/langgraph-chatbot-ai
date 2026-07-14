from langgraph.prebuilt import ToolNode, tools_condition
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_core.tools import tool
from langchain_groq import ChatGroq
from langchain_core.messages import BaseMessage, SystemMessage
from langgraph.graph import StateGraph, START, END
from typing import Annotated, TypedDict
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

# System Instruction for Professional Formatting
SYSTEM_INSTRUCTION = """You are a professional and helpful assistant. When providing responses, follow these formatting guidelines:

📋 **Formatting Guidelines:**
• Use professional and relevant emojis (✅, ⚠️, 📊, 🔍, 💡, ✨, etc.) to enhance readability in point explanation or where you think require as well.
• Use **bullet points (•)** to list related items or features
• Use **numbered lists (1, 2, 3...)** for sequential steps, priorities, or procedures
• Use **bold text** for important terms and key concepts
• Keep responses organized and easy to scan
• Use proper spacing between sections for clarity

📝 **Examples:**
✅ For information lists: Use bullet points
🎯 For step-by-step instructions: Use numbered lists
💡 For key insights: Use emojis to highlight important points
📊 For comparisons: Use tables or structured formatting

⚠️ **IMPORTANT - Tool Usage:**
• When you need to use tools (search, calculator, stock price, etc.), use them silently WITHOUT showing the tool invocation details
• NEVER display tool function calls or code in your response
• Only provide the final answer/result from the tool
• Make the tool usage completely transparent to the user

Always maintain a professional tone while making responses engaging and visually appealing."""

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



@tool
def get_stock_price(symbol: str) -> dict:
    """
    This tool Fetch the current stock price for a given stock symbol using a financial API symbol example like this symbols ( 'AAPL, 'TSLA')

    """
    url =f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={symbol}&apikey=O9VZD9TX8Q6CNXJ5"
    r= requests.get(url)
    return r.json()

    # -----------------
tools = [search_tool, calculator, get_stock_price]

llm_with_tools = llm_model.bind_tools(tools)

# Conversational state schema using add_messages reducer
class ChatState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]

#graph nodes:
def chat_node(state:ChatState):
    """ LLM node that may answer or request a tool call. """
    messages = state['messages']
    # Prepend system instruction to guide LLM formatting
    messages_with_system = [SystemMessage(content=SYSTEM_INSTRUCTION)] + messages
    response = llm_with_tools.invoke(messages_with_system)
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

# Helper Function to retrieve all unique thread IDs from the checkpointer
def retrieve_all_threads():
    all_threads = set()
    for checkpoint in  checkpointer.list(None):
        all_threads.add(checkpoint.config['configurable']['thread_id'])

    return list(all_threads)