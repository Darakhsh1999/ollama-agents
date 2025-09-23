import tool_groups
from llm import LLM
import default_prompts
from agents import Agent
from typing import Callable

class ReActAgent(Agent):
    def __init__(self, llm: LLM, tools: list[Callable] = None, *args, **kwargs):
        super().__init__(
            agent_name="react_agent",
            llm=llm,
            system_prompt=default_prompts.REACT_AGENT_PROMPT,
            tools=tools,
            *args,
            **kwargs,
        )

class MathAgent(Agent):
    def __init__(self, llm: LLM, *args, **kwargs):
        super().__init__(
            agent_name="math_agent",
            llm=llm,
            tools=tool_groups.MATH_TOOLS,
            system_prompt=default_prompts.MATH_AGENT_PROMPT,
            *args,
            **kwargs,
        )

class WritingAgent(Agent):
    def __init__(self, llm: LLM, *args, **kwargs):
        super().__init__(
            agent_name="writing_agent",
            llm=llm,
            tools=tool_groups.FILE_TOOLS,
            system_prompt=default_prompts.WRITING_AGENT_PROMPT,
            *args,
            **kwargs,
        )
    
class CodingAgent(Agent):
    def __init__(self, llm: LLM, *args, **kwargs):
        super().__init__(
            agent_name="coding_agent",
            llm=llm,
            tools=tool_groups.CODING_TOOLS,
            system_prompt=default_prompts.CODING_AGENT_PROMPT,
            *args,
            **kwargs,
        )
    


if __name__ == "__main__":

    llm = LLM("qwen3:4b", use_thinking=False)

    coding_agent = CodingAgent(llm, verbose=True)

    print(coding_agent.invoke("Calculate the levenshtein distance between the strings 'hello' and 'hola'."))


    