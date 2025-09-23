from llm import LLM
from ollama import ChatResponse
from default_prompts import AGENT_PROMPT, REACT_AGENT_PROMPT
from typing import Callable
from pydantic import BaseModel

class Agent():

    def __init__(
        self,
        agent_name: str,
        llm: LLM,
        tools: list[Callable] = None,
        system_prompt: str = None,
        *,
        structured_output: BaseModel = None,
        n_max_steps: int = 10,
        default_system_prompt: bool = False,
        verbose: bool = False,
        ):

        self.agent_name = agent_name
        self.llm = llm
        self.verbose = verbose
        self.n_max_steps = n_max_steps
        self.messages: list[dict[str, str]] = []
        self.tools = []
        self.structured_output = structured_output
        

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
            self.available_tools: dict[str, Callable] = {}
        
        # Structured output
        if structured_output:
            assert issubclass(structured_output, BaseModel), "Structured output must be a pydantic BaseModel"


    def bind_tools(self, tools: list):

        if "tools" not in self.llm.capabilities:
            raise ValueError(f"Model {self.llm.model_name} does not support tool/function calling")

        assert isinstance(tools, list), f"Tools must be a list but got {type(tools)}"
        assert all(callable(tool) for tool in tools), "All tools must be callable"
        if self.tools:
            self.tools += tools
            self.available_tools.update({tool.__name__: tool for tool in tools})
        else:
            self.tools = tools
            self.available_tools = {tool.__name__: tool for tool in tools}

    def generate(self, use_format: bool = False) -> ChatResponse:
        return self.llm.generate(
            self.messages,
            tools=self.tools,
            structured_output=self.structured_output if use_format else None
        )


    def invoke(self, prompt: str, *, images: list[bytes] = None) -> str:

        # Initial user message
        if images:
            if "vision" not in self.llm.capabilities:
                raise RuntimeError(f"Model {self.llm.model_name} does not support vision")
            assert isinstance(images, list), f"Images must be a list but got {type(images)}"
            assert all(isinstance(image, bytes) for image in images), "All images must be bytes"
            assert isinstance(prompt, str), f"Prompt must be a string but got {type(prompt)}"
            self.messages.append({"role": "user", "content": prompt, "images": images})
        else:
            assert isinstance(prompt, str), f"Prompt must be a string but got {type(prompt)}"
            self.messages.append({"role": "user", "content": prompt})
        response = self.generate()
        self.messages.append(response.message)

        # Tool calling loop
        n_steps = 0
        while (tool_call_list := response.message.tool_calls) and (n_steps < self.n_max_steps):
            if self.verbose: print(f"\n[{self.agent_name}] Step {1+n_steps} - Tool calling loop")
            n_steps += 1
            for tool_call in tool_call_list:
                if function_to_call := self.available_tools.get(tool_call.function.name):
                    if self.verbose:
                        print(f"Calling tool {tool_call.function.name} with arguments {tool_call.function.arguments}")
                    output = function_to_call(**tool_call.function.arguments)
                    if self.verbose:
                        print(f"Tool {tool_call.function.name} returned {output}")
                    self.messages.append({'role': 'tool', 'content': str(output), 'tool_name': tool_call.function.name})
                else:
                    self.messages.append({'role': 'tool', 'content': f"Function {tool_call.function.name} not found", 'tool_name': tool_call.function.name})

            response = self.generate()
            self.messages.append(response.message)
        
        if n_steps == self.n_max_steps:
            raise RuntimeError(f"Agent {self.agent_name} reached maximum number of steps {self.n_max_steps}")
        
        if self.structured_output:
            response = self.generate(use_format=True)
            self.messages.append(response.message)
            return self.structured_output.model_validate_json(response.message.content)

        return response.message.content
    


if __name__ == "__main__":

    llm = LLM("qwen3:4b", use_thinking=True)

    from pydantic import Field

    class PersonCard(BaseModel):
        worker_name: str = Field(description="The name of the worker")
        worker_id: int = Field(description="The id of the worker")
        hours_worked: float = Field(description="The hours worked by the worker")
        
    
    def get_name_by_id(id: int) -> str:
        return "John Doe"
    
    def get_hours_worked_by_name(name: str) -> float:
        return 123.45
    

    agent = Agent(
        "agent1",
        llm,
        tools=[get_name_by_id, get_hours_worked_by_name],
        system_prompt=REACT_AGENT_PROMPT,
        verbose=True,
        structured_output=PersonCard,
    )

    output = agent.invoke("How many hours has person with id 35 worked?")
    print("OUTPUT:",output)
    print(type(output))
    from pprint import pprint
    pprint(agent.messages)