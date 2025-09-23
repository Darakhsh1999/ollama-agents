# ollama-agents
Agentic framework implemented exclusively around Ollama models. 

![Ollama Agent](assets/ollama-agent.png)

## 🚀 Quickstart

### Prebuilt Agent

```python
from ollama_agents import Agent

agent = Agent(model="qwen3:4b")
agent.run("Hello, how are you?")
```

### Custom Agent

```python
from ollama_agents import Agent

agent = Agent(model="qwen3:4b")
agent.run("Hello, how are you?")
```

## 🛠️ Getting Started

### Prerequisites

- Python 3.12 or higher
- ollama (see [installation instructions](#installing-ollama))
- pydantic
- ipykernel


### Installing Ollama

1. Visit the [Ollama website](https://ollama.com/) and follow the installation instructions for your operating system.

2. Once installed, download a Ollama model (e.g., qwen3:4b):
   ```bash
   ollama pull qwen3:4b
   ```


## 📜 License
This repository is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
