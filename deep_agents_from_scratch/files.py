# FILE TOOLS + STATE (CLEAN VERSION)

from typing import Annotated, Literal, NotRequired
from typing_extensions import TypedDict
from langchain.agents import AgentState

from langchain_core.tools import tool, InjectedToolCallId
from langchain_core.messages import ToolMessage
from langgraph.prebuilt import InjectedState
from langgraph.types import Command


# STATE

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


# FILE TOOLS

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



# MOCK SEARCH TOOL

@tool
def web_search(query: str) -> str:
    """Mock web search"""

    return """Model Context Protocol (MCP) is an open standard that enables AI models 
to connect with tools, APIs, and external data sources through a unified interface."""






