from langgraph.graph import StateGraph, START, END
from typing import TypedDict, Annotated
from langchain_core.messages import BaseMessage, HumanMessage, SystemMessage
from dotenv import load_dotenv
from langgraph.graph.message import add_messages
from langchain_groq import ChatGroq
from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.prebuilt import ToolNode, tools_condition
import sqlite3
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_core.tools import tool
import requests

# load environment variables
load_dotenv()

# define model
llm = ChatGroq(
    model = "meta-llama/llama-4-maverick-17b-128e-instruct",
    temperature = 1
)


# tools :- pre-built and custom
search_tool = DuckDuckGoSearchRun(region="us-en")

@tool
def calculator(first_num: float, second_num: float, operation: str) -> dict:
    """
    Performs a basic arithmetic operation on two numbers.
    Supported operations: add, sub, mul, div
    """
    try:
        if operation == "add":
            result = first_num + second_num
        elif operation == "sub":
            result = first_num - second_num
        elif operation == "mul":
            result = first_num * second_num
        elif operation == "div":
            if second_num == 0:
                return {"error": "Division by zero is not allowed."}
            result = first_num / second_num
        else:
            return {"error": "Unsupported operation '{operation}'"}
        return {"result: ", result}
    except Exception as e:
        return {"error": str(e)}

@tool
def get_stock_price(symbol: str) -> dict:
    """ Fetch latest stock price for a given symbol (e.g. "AAPL", "TSLA")
        using Alpha Vantage with api key in the URL. 
    """
    url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={symbol}&apikey=P7EBPSQM1DEFKVQT"
    r = requests.get(url)
    return r.json()


tools = [get_stock_price, search_tool, calculator]
llm_with_tools = llm.bind_tools(tools)


# define graph state
class ChatState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]


# define functions
def chat_node(state: ChatState):
    messages = state["messages"]
    response = llm_with_tools.invoke(messages)
    return {"messages": [response]}

tool_node = ToolNode(tools)

conn = sqlite3.connect(database="chatbot.db", check_same_thread=False)

# define checkpointer
checkpointer = SqliteSaver(conn=conn)


# define graph
graph = StateGraph(ChatState)

graph.add_node("chat_node", chat_node)
graph.add_node("tools", tool_node)

graph.add_edge(START, "chat_node")
graph.add_conditional_edges("chat_node", tools_condition)
graph.add_edge('tools', 'chat_node')
graph.add_edge("chat_node", END)

chatbot = graph.compile(checkpointer=checkpointer)

