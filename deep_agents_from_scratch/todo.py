# TODO TOOLS 

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


class DeepAgentState(AgentState):
    todos: NotRequired[list[Todo]]
    files: NotRequired[dict[str, str]]



# TOOLS


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
