import os
from re import M
import os
from typing import Annotated, List, TypedDict

from langgraph.graph import END, START, StateGraph
from langgraph.graph.message import AnyMessage, add_messages
from langgraph.prebuilt import ToolNode
from langgraph.checkpoint.memory import MemorySaver
from langchain_openai import ChatOpenAI
from langchain_mistralai import ChatMistralAI
from langchain_core.tools import tool as lc_tool

from tools import calculate_expression, fetch_url, get_current_time


class ChatState(TypedDict):
    messages: Annotated[List[AnyMessage], add_messages]


# Wrap plain functions as LangChain Tools so the model can call them
@lc_tool
def calc(expression: str) -> str:
    """Evaluate a math expression. Use for arithmetic like 2*(3+4)."""
    return calculate_expression(expression)


@lc_tool
def web_get(url: str) -> str:
    """Fetch the text content of a URL. Provide the full URL including scheme."""
    return fetch_url(url)


@lc_tool
def now() -> str:
    """Get the current UTC time in ISO 8601 format."""
    return get_current_time()


TOOLS = [calc, web_get, now]
tool_node = ToolNode(TOOLS)


def call_model(state: ChatState) -> dict:
    # Bind tools so the model can decide to call them via function/tool calls
    model = ChatMistralAI(
        model="mistral-large-latest",
        temperature=0.2,
    ).bind_tools(TOOLS)

    model = ChatOpenAI(
        model="qwen-3-32b",
        temperature=0.2,
        api_key=os.getenv("API_KEY"),
        base_url=os.getenv("BASE_URL"),
    ).bind_tools(TOOLS)

    response = model.invoke(state["messages"])
    return {"messages": [response]}


def route_tools(state: ChatState):
    last = state["messages"][-1]
    # If the model requested any tool calls, go to the tools node; otherwise end
    if getattr(last, "tool_calls", None):
        return "tools"
    return END


def create_graph():
    builder = StateGraph(ChatState)
    builder.add_node("model", call_model)
    builder.add_node("tools", tool_node)
    builder.add_edge(START, "model")
    builder.add_conditional_edges(
        "model",
        route_tools,
        {"tools": "tools", END: END},
    )
    # After tools run, go back to the model to incorporate tool results
    builder.add_edge("tools", "model")
    # Persistent across invocations via thread_id within process lifetime
    checkpointer = MemorySaver()
    return builder.compile(checkpointer=checkpointer)


graph = create_graph()


