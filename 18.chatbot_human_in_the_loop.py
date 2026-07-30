from langgraph.prebuilt import ToolNode, tools_condition
from langchain_core.tools import tool
from langchain_groq import ChatGroq
from langchain_core.messages import BaseMessage , HumanMessage
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import StateGraph, START, END
from typing import Annotated, TypedDict
from pydantic import BaseModel, Field
from langgraph.graph.message import add_messages
from langgraph.types import interrupt, Command
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
llm_model = ChatGroq(model="llama-3.3-70b-versatile")

#tool to get real stock price
@tool
def get_stock_price(symbol: str) -> dict:
    """
    This tool Fetch the current stock price for a given stock symbol using a financial API symbol example like this symbols ( 'AAPL, 'TSLA')

    """
    url =f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={symbol}&apikey=O9VZD9TX8Q6CNXJ5"
    r= requests.get(url)
    return r.json()

#Tool to purchae the stock ,but its dummy tool fr simulation...........
@tool
def purchase_stock(symbol: str, quantity: int) -> dict:
    """
    simulate purchasing a given quantity of a stock symbol.

    HUMAM-IN-THE-LOOP
    Before confirming the purchase,this tool will interrupt and wait for human decision ("yes" / anything else ).
    """
    #This pauses the graph and returns contol to the caller.
    decision = interrupt(f"Approve buying {quantity} shares of the {symbol}? (yes/no)")

    if isinstance(decision, str) and decision.lower() =="yes":
        return {
            "status":"success",
            "message":f"Purchase order placed for {quantity} shares of {symbol}",
            "symbol":symbol,
            "quantity":quantity,
        }
    
    else:
        return {
            "status":"Cancelled",
            "message":f"Purchase of {quantity} shares of {symbol} declined by Human",
            "symbol":symbol,
            "quantity":quantity,
        }

tools = [get_stock_price,purchase_stock]
llm_with_tools=llm_model.bind_tools(tools)

class ChatState(TypedDict):
    messages : Annotated[list[BaseMessage],add_messages]

def chat_node(state:ChatState):
    """ LLM node that may answer or request a tool call."""
    messages = state["messages"]
    response = llm_with_tools.invoke(messages)
    return {"messages":[response]}

#Create Tool Node
tool_node = ToolNode(tools)

memory = MemorySaver()

#Create graph nodes, Edges
graph=StateGraph(ChatState)

graph.add_node("chat_node",chat_node)
graph.add_node("tools",tool_node)

graph.add_edge(START,"chat_node")
graph.add_conditional_edges("chat_node",tools_condition)
graph.add_edge("tools","chat_node")

chatbot= graph.compile(checkpointer=memory)


if __name__ == "__main__":

    thread_id="demo-thread"

    while True:
        user_input=input("You : ")
        if user_input.lower().strip() in {"exit","quit"}:
            print("GoodBye...:) ")
            break
        
        #build initial state for this turn
        state = {"messages" : [HumanMessage(content=user_input)]}

        #Run the grpah
        result = chatbot.invoke(
            state,
            config={"configurable":{"thread_id":thread_id}},
        )

        #Check for HIT: interrupt from purchase stock...
        interrupts= result.get("__interrupt__",[])

        if interrupts:
            #Our interrupt payload in the string we passed to interupt
            prompt_to_human = interrupts[0].value
            print(f"HITL: {prompt_to_human}")
            decision = input("Your Decision: ").strip().lower()

            #Resume the graph with human decision yes/no /whatever


            result = chatbot.invoke(
                Command(resume=decision),
                config={"configurable":{"thread_id":thread_id}},

            )

        #Get latest message from Ai assitant...
        messages= result["messages"]
        last_msg= messages[-1]
        print(f"Bot : {last_msg.content}\n")
