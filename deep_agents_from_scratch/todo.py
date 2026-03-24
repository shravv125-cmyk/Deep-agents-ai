# ============================================
# TODO TOOLS (CLEAN VERSION)
# ============================================

from typing import Annotated, Literal, NotRequired
from typing_extensions import TypedDict

from langchain.agents import AgentState
from langchain_core.tools import tool, InjectedToolCallId
from langchain_core.messages import ToolMessage
from langgraph.prebuilt import InjectedState
from langgraph.types import Command


# ============================================
# STATE
# ============================================

class Todo(TypedDict):
    content: str
    status: Literal["pending", "in_progress", "completed"]


class DeepAgentState(AgentState):
    todos: NotRequired[list[Todo]]
    files: NotRequired[dict[str, str]]


# ============================================
# TOOLS
# ============================================

@tool
def write_todos(
    todos: list[Todo],
    state: Annotated[DeepAgentState, InjectedState],
    tool_call_id: Annotated[str, InjectedToolCallId],
) -> Command:
    """Update the todo list."""

    return Command(
        update={
            "todos": todos,
            "messages": [
                ToolMessage(
                    content=f"Updated todos: {todos}",
                    tool_call_id=tool_call_id,
                )
            ],
        }
    )


@tool
def read_todos(
    state: Annotated[DeepAgentState, InjectedState],
) -> str:
    """Read current todos."""

    todos = state.get("todos", [])

    if not todos:
        return "No todos found."

    result = "TODO LIST:\n"
    for i, todo in enumerate(todos, 1):
        result += f"{i}. {todo['content']} ({todo['status']})\n"

    return result


@tool
def web_search(query: str) -> str:
    """Mock web search tool."""

    return """Model Context Protocol (MCP) is an open standard that allows AI models 
to connect with tools, APIs, and external systems using a unified interface."""










# # ================================
# # 1. LOAD ENV VARIABLES
# # ================================
#
# import os
# from dotenv import load_dotenv
#
# # Load .env file from project root (simpler + reliable)
# load_dotenv()
#
# # Debug: check if API key is loaded
# print("API KEY LOADED:", os.getenv("OPENAI_API_KEY") is not None)
#
# # ================================
# # 2. SUPPRESS WARNINGS (OPTIONAL)
# # ================================
#
# import warnings
#
# warnings.filterwarnings(
#     "ignore",
#     message="LangSmith now uses UUID v7",
#     category=UserWarning,
# )
#
# # ================================
# # 3. DEFINE STATE STRUCTURE
# # ================================
#
# from typing import Annotated, Literal, NotRequired
# from typing_extensions import TypedDict
# from langchain.agents import AgentState
#
#
# # Todo item structure
# class Todo(TypedDict):
#     content: str  # task description
#     status: Literal["pending", "in_progress", "completed"]  # task state
#
#
# # Reducer for merging file dictionaries
# def file_reducer(left, right):
#     if left is None:
#         return right
#     elif right is None:
#         return left
#     else:
#         return {**left, **right}
#
#
# # Custom agent state
# class DeepAgentState(AgentState):
#     todos: NotRequired[list[Todo]]  # list of todos
#     files: Annotated[NotRequired[dict[str, str]], file_reducer]  # virtual files
#
#
# # ================================
# # 4. DEFINE TOOLS
# # ================================
#
# from langchain_core.messages import ToolMessage
# from langchain_core.tools import tool
# from langgraph.types import Command
# from langchain_core.tools import InjectedToolCallId
# from langgraph.prebuilt import InjectedState
#
#
# # Tool to WRITE todos
# @tool
# def write_todos(todos: list[Todo], tool_call_id: str) -> Command:
#     """Update the todo list."""
#
#     return Command(
#         update={
#             "todos": todos,  # update state
#             "messages": [
#                 ToolMessage(
#                     content=f"Updated todos: {todos}",
#                     tool_call_id=tool_call_id,
#                 )
#             ],
#         }
#     )
#
#
# # Tool to READ todos
# @tool
# def read_todos(state: Annotated[DeepAgentState, InjectedState]) -> str:
#     """Read current todos."""
#
#     todos = state.get("todos", [])
#
#     if not todos:
#         return "No todos found."
#
#     result = "TODO LIST:\n"
#     for i, todo in enumerate(todos, 1):
#         result += f"{i}. {todo['content']} ({todo['status']})\n"
#
#     return result
#
#
# # Mock web search tool
# @tool
# def web_search(query: str) -> str:
#     """Mock web search tool."""
#
#     return """Model Context Protocol (MCP) is an open standard by Anthropic
# that allows AI models to connect with external tools, databases, and APIs
# through a unified interface."""
#
#
# # ================================
# # 5. CREATE MODEL (FIXED)
# # ================================
#
# from langchain.chat_models import init_chat_model
#
# # ✅ Use OpenAI model (since you likely have OpenAI key)
# model = init_chat_model(
#     model="openai:gpt-4o-mini",  # cheaper + works with OpenAI key
#     temperature=0
# )
#
# # ================================
# # 6. CREATE AGENT
# # ================================
#
# from langchain.agents import create_agent
#
# tools = [write_todos, read_todos, web_search]
#
# SYSTEM_PROMPT = """
# You are a helpful AI agent.
#
# IMPORTANT:
# - Always use web_search for factual questions
# - Maintain todos for multi-step tasks
# """
#
# agent = create_agent(
#     model=model,
#     tools=tools,
#     system_prompt=SYSTEM_PROMPT,
#     state_schema=DeepAgentState,
# )
#
# # ================================
# # 7. RUN AGENT
# # ================================
#
# result = agent.invoke(
#     {
#         "messages": [
#             {
#                 "role": "user",
#                 "content": "Give me a short summary of MCP",
#             }
#         ],
#         "todos": [],  # initial empty todo list
#     }
# )
#
# # ================================
# # 8. PRINT OUTPUT
# # ================================
#
# for msg in result["messages"]:
#     print(msg)