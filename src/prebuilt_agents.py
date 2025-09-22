import tool_groups
from llm import LLM
import default_prompts
from agents import Agent

class MathAgent(Agent):
    def __init__(self, llm: LLM):
        super().__init__(
            agent_name="math_agent",
            llm=llm,
            tools=tool_groups.MATH_TOOLS,
            system_prompt=default_prompts.MATH_AGENT_PROMPT,
        )

class ReActAgent(Agent):
    def __init__(self, llm: LLM):
        super().__init__(
            agent_name="react_agent",
            llm=llm,
            tools=tool_groups.FILE_TOOLS,
            system_prompt=default_prompts.REACT_AGENT_PROMPT,
        )

class WritingAgent(Agent):
    def __init__(self, llm: LLM):
        super().__init__(
            agent_name="writing_agent",
            llm=llm,
            tools=tool_groups.FILE_TOOLS,
            system_prompt=default_prompts.WRITING_AGENT_PROMPT,
        )
    
class CodingAgent(Agent):
    def __init__(self, llm: LLM):
        super().__init__(
            agent_name="coding_agent",
            llm=llm,
            tools=tool_groups.FILE_TOOLS,
            system_prompt=default_prompts.CODING_AGENT_PROMPT,
        )
    