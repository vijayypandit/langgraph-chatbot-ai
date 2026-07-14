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
import asyncio


# Load environment variables from .env file
load_dotenv(override=True)

# Ensure the Groq API key is set in the environment
os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")

# Initialize the Groq Chat LLM with streaming mode enabled
llm_model = ChatGroq(model="llama-3.3-70b-versatile", streaming=True)

#Tools
# 


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

tools = [calculator]

# Bind the tools to the LLM model to create a new LLM instance that can utilize these tools
llm_with_tools = llm_model.bind_tools(tools)

# Conversational state schema using add_messages reducer
class ChatState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]


def build_graph():

    #graph nodes:
    async def chat_node(state:ChatState):
        """ LLM node that may answer or request a tool call. """
        messages = state['messages']
        response = await llm_with_tools.ainvoke(messages)
        return {"messages": [response]}

    tool_node = ToolNode(tools)
#Graph structure
    graph = StateGraph(ChatState)
    graph.add_node("chat_node",chat_node)
    graph.add_node("tools",tool_node)

    graph.add_edge(START,"chat_node")
    graph.add_conditional_edges("chat_node", tools_condition)
    graph.add_edge("tools","chat_node")

    chatbot = graph.compile()
    return chatbot

async def main():
    chatbot = build_graph()

    #runningt the graph with a sample input
    result = await chatbot.ainvoke({"messages":[HumanMessage(content="Find the multiply of 5 and 5 and give answer like a cricket commentator")]})
    print(result['messages'][-1].content)

if __name__ == '__main__':
    asyncio.run(main())