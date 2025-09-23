# ollama-agents
Agentic framework implemented exclusively around Ollama models. 

![Ollama Agent](assets/ollama-agent.png)

## 🚀 Quickstart

### Prebuilt Agent

```python
from llms import LLM
from prebuilt_agents import CodingAgent

# Initialize the LLM
llm = LLM("qwen3:4b")

# Initialize the prebuilt agent
coding_agent = CodingAgent(llm, verbose=True)

# Invoke the agent
output = coding_agent.invoke("Convert the 35 degrees celsius to fahrenheit.")

print(output)
>>> example output: 95.0
```

### Custom Agent

```python
from llms import LLM
from agents import Agent

# Initialize the LLM
llm = LLM("qwen3:4b")

# Initialize the custom agent
agent = Agent(llm, verbose=True)

# Invoke the agent
output = agent.invoke("Hello, how are you?")

print(output)
```

## Quick demo

![Quick demo](assets/quick-demo.gif)

## 🛠️ Getting Started

### Prerequisites

- Python 3.12 or higher
- ollama (see [installation instructions](#installing-ollama))
- pydantic
- ipykernel

### Installation
Setup and installation using `uv`:

Install dependencies:
```bash
uv sync
```

Activate the virtual environment:
```bash
source .venv/bin/activate
```


### Installing Ollama

1. Visit the [Ollama website](https://ollama.com/) and follow the installation instructions for your operating system.

2. Once installed, download a Ollama model (e.g., qwen3:4b):
   ```bash
   ollama pull qwen3:4b
   ```


## 📜 License
This repository is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Roadmap

The core framework features are already implemented. Future plans and roadmap goals are defined in the [Roadmap](ROADMAP.md) file.



