import sys
sys.path.append("../src")
from prebuilt_agents import WritingAgent
from agents import Agent
from llm import LLM
from base_tools import addition



if __name__ == "__main__":

    llm = LLM("qwen3:4b", use_thinking=True)

    writing_agent = WritingAgent(llm, verbose=True)
    import time

    print(writing_agent.invoke("Create a python file that implements a random forest regressor. Name it random_forest_regressor.py. Do not add comments"))
    print("paused")
    time.sleep(30)
    print(writing_agent.invoke("Edit the python file that you just created to limit the tree depth to max depth of 5. Also add some basic comments inside the code to explain what the code does."))
