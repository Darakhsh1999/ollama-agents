from llm import LLM
from ollama import ChatResponse
from default_prompts import AGENT_PROMPT

class Agent():

    def __init__(
        self,
        agent_name: str,
        llm: LLM,
        tools: list = None,
        system_prompt: str = None,
        *,
        n_max_steps: int = 10,
        default_system_prompt: bool = False,
        verbose: bool = False,
        ):

        self.agent_name = agent_name
        self.llm = llm
        self.verbose = verbose
        self.n_max_steps = n_max_steps
        self.messages: list[dict[str, str]] = []

        # System prompt
        if system_prompt:
            self.messages.append({"role": "system", "content": system_prompt})
        elif default_system_prompt:
            self.messages.append({"role": "system", "content": AGENT_PROMPT})

        # Tools
        if tools:
            self.bind_tools(tools)
        else:
            self.tools = []
            self.available_tools = {}


    def bind_tools(self, tools: list):

        assert isinstance(tools, list), f"Tools must be a list but got {type(tools)}"
        assert all(callable(tool) for tool in tools), "All tools must be callable"
        if self.tools:
            self.tools += tools
            self.available_tools.update({tool.__name__: tool for tool in tools})
        else:
            self.tools = tools
            self.available_tools = {tool.__name__: tool for tool in tools}

    def generate(self) -> ChatResponse:
        return self.llm.generate(self.messages, self.tools)


    def invoke(self, prompt: str) -> str:

        # Initial user message
        self.messages.append({"role": "user", "content": prompt})
        response = self.generate()
        self.messages.append(response.message)

        # Tool calling loop
        n_steps = 0
        while (tool_call_list := response.message.tool_calls) and (n_steps < self.n_max_steps):
            n_steps += 1
            for tool_call in tool_call_list:
                if function_to_call := self.available_tools.get(tool_call.function.name):
                    if self.verbose:
                        print(f"Calling tool {tool_call.function.name} with arguments {tool_call.function.arguments}")
                    output = function_to_call(**tool_call.function.arguments)
                    self.messages.append({'role': 'tool', 'content': str(output), 'tool_name': tool_call.function.name})
                else:
                    self.messages.append({'role': 'tool', 'content': f"Function {tool_call.function.name} not found", 'tool_name': tool_call.function.name})

            response = self.generate()
            self.messages.append(response.message)
        
        if n_steps == self.n_max_steps:
            raise RuntimeError(f"Agent {self.agent_name} reached maximum number of steps {self.n_max_steps}")

        return response.message.content
    


if __name__ == "__main__":
    llm = LLM("llama3.2", default_system_prompt=True)
    agent = Agent("agent1", llm)
    print(agent.invoke("Hello my name is Bob and I am 30 years old. My favourite color is blue."))