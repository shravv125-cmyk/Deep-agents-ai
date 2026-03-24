# Deep-agents-ai
Deep Agents is a Python project that demonstrates building intelligent AI agents .

# 🤖 Deep Agents (LangChain + NVIDIA API)

This project demonstrates how to build **AI agents with tools, memory, and multi-agent support** using LangChain and NVIDIA API (OpenAI-compatible endpoint).

---

## 🚀 Features

* ✅ Custom AI Agent using LangChain
* 🧰 Tool usage (calculator, file system, todos, web search)
* 📂 Virtual file system (read/write files)
* 📝 Todo management system
* 🧠 Multi-agent support (math + research agents)
* 🔌 NVIDIA API integration (OpenAI-compatible)

---

## 📁 Project Structure

```
deepAgents/
│
├── main.py                     # Main entry point (runs everything)
├── .env                        # API keys (DO NOT SHARE)
│
├── deep_agents_from_scratch/
│   ├── __init__.py
│   ├── files.py                # File tools (ls, read, write)
│   ├── todo.py                 # Todo tools
│   └── state.py                # Agent state definition
│
└── venv/                       # Virtual environment
```

---

## ⚙️ Setup Instructions

### 1. Clone the repo

```
git clone <your-repo-url>
cd deepAgents
```

---

### 2. Create virtual environment

```
python -m venv venv
venv\Scripts\activate   # Windows
```

---

### 3. Install dependencies

```
pip install -r requirements.txt
```

---

### 4. Setup `.env` file (IMPORTANT)

Create a `.env` file in root folder:

```
OPENAI_API_KEY=nvapi-your_key_here
NVIDIA_API_KEY=nvapi-your_key_here
```

⚠️ Rules:

* No quotes
* No spaces
* Format must be `KEY=value`

---

## ▶️ Run the Project

```
python main.py
```

---

## 🧠 How It Works

### 1. `main.py`

* Entry point of the project
* Creates agents
* Runs `.invoke()` to process user queries

---

### 2. Other Files

| File       | Role               |
| ---------- | ------------------ |
| `files.py` | File system tools  |
| `todo.py`  | Todo management    |
| `state.py` | Agent memory/state |

👉 These files are **imported and used**, not directly executed.

---

### 3. Agent Flow

```
User Input
   ↓
Agent (LangChain)
   ↓
Decides which tool to use
   ↓
Tool executes (files/todos/etc.)
   ↓
Final Answer
```

---

## 🤖 Example Queries

* `What is 3.1 * 4.2?`
* `Save 'Hello World' in test.txt and read it`
* `Explain Model Context Protocol (MCP)`

---

## 🔥 Multi-Agent Example

You can run multiple agents:

```python
math_result = math_agent.invoke({...})
research_result = research_agent.invoke({...})
```

---

## ⚠️ Common Errors & Fixes

### ❌ `.env` parsing error

✔ Fix format:

```
KEY=value
```

---

### ❌ API key not set

✔ Ensure:

```
print(os.getenv("OPENAI_API_KEY"))
```

---

### ❌ Import errors

✔ Ensure correct folder structure
✔ Add `__init__.py` in folders

---

## 🧠 Key Concepts

* **main.py runs everything**
* Other files = tools (run only when called)
* Agents run only when `.invoke()` is used

---

## 📌 Notes

* Do NOT share your API keys publicly
* NVIDIA API works via OpenAI-compatible interface
* You can extend with more tools easily

---

## 🚀 Future Improvements

* Add real web search (Tavily)
* Add memory persistence
* Add UI (Streamlit)
* Parallel agents

---

## 👨‍💻 Author
Shravani Kadam






