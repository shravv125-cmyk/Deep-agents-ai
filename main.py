
# 1. LOAD ENV VARIABLES


from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv("NVIDIA_API_KEY")

if not api_key:
    raise ValueError("❌ NVIDIA_API_KEY not set")

print("✅ NVIDIA KEY LOADED")



# 2. SUPPRESS WARNINGS

import warnings
warnings.filterwarnings("ignore")



# 3. IMPORT TOOLS (FIXED)

from typing import Literal, Union
from langchain_core.tools import tool


from deep_agents_from_scratch.files import (
    ls,
    read_file,
    write_file,
)

from deep_agents_from_scratch.todo import (
    write_todos,
    read_todos,
    web_search,
    DeepAgentState,
)



# 4. CALCULATOR TOOL


@tool
def calculator(
    operation: Literal["add", "subtract", "multiply", "divide"],
    a: Union[int, float],
    b: Union[int, float],
):
    """Perform basic arithmetic operations."""

    if operation == "divide" and b == 0:
        return {"error": "Division by zero is not allowed."}

    if operation == "add":
        return a + b
    elif operation == "subtract":
        return a - b
    elif operation == "multiply":
        return a * b
    elif operation == "divide":
        return a / b
    else:
        return {"error": "Invalid operation"}



# 5. MODEL (NVIDIA)


from langchain_openai import ChatOpenAI

lc_model = ChatOpenAI(
    model="openai/gpt-oss-120b",
    api_key="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",
    base_url="https://integrate.api.nvidia.com/v1",
    temperature=0,
)



# 6. CREATE AGENT


from langchain.agents import create_agent

tools = [
    calculator,
    ls,
    read_file,
    write_file,
    write_todos,
    read_todos,
    web_search,
]

SYSTEM_PROMPT = """
You are a smart AI agent.

Rules:
- Use calculator for math
- Use file tools for storage
- Use todos for task tracking
- Use web_search for knowledge
"""

agent = create_agent(
    model=lc_model,
    tools=tools,
    system_prompt=SYSTEM_PROMPT,
    state_schema=DeepAgentState,
).with_config({"recursion_limit": 20})



# 7. RUN AGENT


print("\n=== AGENT OUTPUT ===\n")

agent_result = agent.invoke(
    {
        "messages": [
            {"role": "user", "content": "What is 3.1 * 4.2?"}
        ],
        "files": {},   # ✅ REQUIRED
        "todos": [],   # ✅ REQUIRED
    }
)

for msg in agent_result["messages"]:
    if hasattr(msg, "content") and msg.content:
        print(msg.content)


# from langchain.agents import create_agent
#
#  MATH AGENT (focused on calculator)
# math_agent = create_agent(
#     model=lc_model,
#     tools=[calculator],
#     system_prompt="You are a math expert. Always use calculator.",
#     state_schema=DeepAgentState,
# ).with_config({"recursion_limit": 10})


#  RESEARCH AGENT (focused on knowledge)
# research_agent = create_agent(
#     model=lc_model,
#     tools=[web_search],
#     system_prompt="You are a research assistant. Use web_search.",
#     state_schema=DeepAgentState,
# ).with_config({"recursion_limit": 10})
#
# results = [
#     ("MATH AGENT", math_agent),
#     ("RESEARCH AGENT", research_agent),
# ]
#
# for name, result in results:
#     print(f"\n=== {name} FINAL OUTPUT ===\n")
#
#     if not isinstance(result, dict):
#         print(" ERROR: result is not a dict")
#         print("Type:", type(result))
#         continue
#
#     for msg in reversed(result.get("messages", [])):
#         if hasattr(msg, "content") and msg.content:
#             print(msg.content)
#             break



# 8. DIRECT NVIDIA API CALL

from openai import OpenAI

client = OpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key="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"
)

print("\n=== DIRECT MODEL OUTPUT ===\n")

completion = client.chat.completions.create(
    model="openai/gpt-oss-120b",
    messages=[
        {"role": "user", "content": "Explain Model Context Protocol simply"}
    ],
    temperature=0.7,
    max_tokens=300,
)

if not completion.choices:
    print(" No response")
else:
    message = completion.choices[0].message

    reasoning = getattr(message, "reasoning_content", None)
    content = message.content

    if reasoning:
        print("\n🧠 Reasoning:\n", reasoning)

    if content:
        print("\n💬 Answer:\n", content)
    else:
        print("\n⚠️ Model returned no final answer, only reasoning.")




