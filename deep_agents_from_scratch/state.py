from typing import NotRequired
from typing_extensions import TypedDict


class DeepAgentState(TypedDict, total=False):
    todos: list
    files: dict