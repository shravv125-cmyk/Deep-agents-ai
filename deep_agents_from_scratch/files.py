# ============================================
# FILE TOOLS + STATE (CLEAN VERSION)
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


def file_reducer(left, right):
    if left is None:
        return right
    if right is None:
        return left
    return {**left, **right}


class DeepAgentState(AgentState):
    files: Annotated[NotRequired[dict[str, str]], file_reducer]


# ============================================
# FILE TOOLS
# ============================================

@tool
def ls(state: Annotated[DeepAgentState, InjectedState]) -> list[str]:
    """List all files in virtual memory"""
    return list(state.get("files", {}).keys())


@tool
def read_file(
    file_path: str,
    state: Annotated[DeepAgentState, InjectedState],
) -> str:
    """Read file content"""

    files = state.get("files", {})

    if file_path not in files:
        return f"File '{file_path}' not found"

    return files[file_path]


@tool
def write_file(
    file_path: str,
    content: str,
    state: Annotated[DeepAgentState, InjectedState],
    tool_call_id: Annotated[str, InjectedToolCallId],
) -> Command:
    """Write content to file"""

    files = state.get("files", {})
    files[file_path] = content

    return Command(
        update={
            "files": files,
            "messages": [
                ToolMessage(
                    content=f"Saved file {file_path}",
                    tool_call_id=tool_call_id,
                )
            ],
        }
    )


# ============================================
# MOCK SEARCH TOOL
# ============================================

@tool
def web_search(query: str) -> str:
    """Mock web search"""

    return """Model Context Protocol (MCP) is an open standard that enables AI models 
to connect with tools, APIs, and external data sources through a unified interface."""








# # ============================================
# # 1. LOAD ENV VARIABLES
# # ============================================
#
# import os
# from dotenv import load_dotenv
#
# # Load .env file (keep it in same directory)
# load_dotenv()
#
# # Debug check
# print("API KEY LOADED:", os.getenv("OPENAI_API_KEY") is not None)
#
# # ============================================
# # 2. SUPPRESS WARNINGS
# # ============================================
#
# import warnings
#
# warnings.filterwarnings(
#     "ignore",
#     message="LangSmith now uses UUID v7",
#     category=UserWarning,
# )
#
# # ============================================
# # 3. DEFINE STATE
# # ============================================
#
# from typing import Annotated, Literal, NotRequired
# from typing_extensions import TypedDict
# from langchain.agents import AgentState
#
#
# # Define Todo structure (optional, not heavily used here)
# class Todo(TypedDict):
#     content: str
#     status: Literal["pending", "in_progress", "completed"]
#
#
# # Reducer to merge file dictionaries
# def file_reducer(left, right):
#     if left is None:
#         return right
#     elif right is None:
#         return left
#     return {**left, **right}
#
#
# # Custom agent state
# class DeepAgentState(AgentState):
#     files: Annotated[NotRequired[dict[str, str]], file_reducer]
#
#
# # ============================================
# # 4. FILE SYSTEM TOOLS
# # ============================================
#
# from langchain_core.tools import tool
# from langchain_core.messages import ToolMessage
# from langchain_core.tools import InjectedToolCallId
# from langgraph.prebuilt import InjectedState
# from langgraph.types import Command
#
#
# # List files
# @tool
# def ls(state: Annotated[DeepAgentState, InjectedState]) -> list[str]:
#     """List all files in virtual memory"""
#     return list(state.get("files", {}).keys())
#
#
# # Read file
# @tool
# def read_file(
#         file_path: str,
#         state: Annotated[DeepAgentState, InjectedState],
# ) -> str:
#     """Read file content"""
#
#     files = state.get("files", {})
#
#     if file_path not in files:
#         return f"File '{file_path}' not found"
#
#     return files[file_path]
#
#
# # Write file
# @tool
# def write_file(
#         file_path: str,
#         content: str,
#         state: Annotated[DeepAgentState, InjectedState],
#         tool_call_id: str,
# ) -> Command:
#     """Write content to file"""
#
#     files = state.get("files", {})
#     files[file_path] = content
#
#     return Command(
#         update={
#             "files": files,
#             "messages": [
#                 ToolMessage(
#                     content=f"Saved file {file_path}",
#                     tool_call_id=tool_call_id,
#                 )
#             ],
#         }
#     )
#
#
# # ============================================
# # 5. MOCK SEARCH TOOL
# # ============================================
#
# @tool
# def web_search(query: str) -> str:
#     """Mock web search"""
#
#     return """Model Context Protocol (MCP) is an open standard that enables AI models
# to connect with external tools, APIs, and data sources through a unified interface."""
#
#
# # ============================================
# # 6. SYSTEM PROMPT
# # ============================================
#
# FILE_USAGE_INSTRUCTIONS = """
# You have access to a virtual file system.
#
# Workflow:
# 1. Use ls() to check files
# 2. Use write_file() to save important info
# 3. Use read_file() when needed
# """
#
# RESEARCH_INSTRUCTIONS = """
# IMPORTANT:
# Use web_search exactly once to answer the question.
# """
#
# SYSTEM_PROMPT = FILE_USAGE_INSTRUCTIONS + "\n\n" + RESEARCH_INSTRUCTIONS
#
# # ============================================
# # 7. MODEL (FIXED)
# # ============================================
#
# from langchain.chat_models import init_chat_model
#
# # Use OpenAI (works with your setup)
# model = init_chat_model(
#     model="openai:gpt-4o-mini",
#     temperature=0
# )
#
# # ============================================
# # 8. CREATE AGENT
# # ============================================
#
# from langchain.agents import create_agent
#
# tools = [ls, read_file, write_file, web_search]
#
# agent = create_agent(
#     model=model,
#     tools=tools,
#     system_prompt=SYSTEM_PROMPT,
#     state_schema=DeepAgentState,
# )
#
# # ============================================
# # 9. VISUALIZE AGENT (OPTIONAL)
# # ============================================
#
# from IPython.display import Image, display
#
# try:
#     display(Image(agent.get_graph(xray=True).draw_mermaid_png()))
# except:
#     print("Graph visualization not supported.")
#
# # ============================================
# # 10. RUN AGENT
# # ============================================
#
# result = agent.invoke(
#     {
#         "messages": [
#             {
#                 "role": "user",
#                 "content": "Give me an overview of MCP",
#             }
#         ],
#         "files": {},  # initialize virtual file system
#     }
# )
#
# # ============================================
# # 11. PRINT OUTPUT
# # ============================================
#
# print("\n=== OUTPUT ===\n")
#
# for msg in result["messages"]:
#     print(msg)