import random
from llm import LLM
from agents import Agent
from pydantic import BaseModel, Field

def main():

    # Pydantic class for structured output
    class Weather(BaseModel):
        temperature_fahrenheit: float = Field(description="Temperature in Fahrenheit")
        weather_condition: str = Field(description="Description of the weather")
        appropriate_clothing: str = Field(description="Appropriate clothing for the weather")

    # Tools
    def celcius_to_fahrenheit(celcius: float) -> float:
        """Convert Celsius to Fahrenheit."""
        return (celcius * 9/5) + 32

    def weather_condition(city_name: str) -> str:
        """Get the weather condition for a given city."""
        return random.choice(["Sunny", "Rainy", "Cloudy", "Windy", "Snowy"])
    

    # Sampling parameters
    sampling_params = {
        "temperature": 0.5,
        "top_p": 0.9,
        "top_k": 100,
    }

    # Initialize the LLM
    llm = LLM(
        model_name="qwen3:4b", # Model name as given by running `ollama list` in bash
        use_thinking=True, # Enable thinking/reasoning mode for supported models
        options=sampling_params, # Custom sampling parameters
    )

    # Initialize the Agent
    agent = Agent(
        agent_name="Weather Agent", # Agent name
        llm=llm, # The LLM instance
        tools=[celcius_to_fahrenheit, weather_condition], # List of tools
        system_prompt="You are a helpful assistant.", # System prompt
        structured_output=Weather, # Structured output
        n_max_steps=5, # Limit the number of steps
    )

    # Invoke the agent
    output = agent.invoke("It is 35 degrees celsius in New York. What is the weather condition?")

    print(output)
    # >>> temperature_fahrenheit=95.0 weather_condition='Windy' appropriate_clothing='Light jacket or windbreaker'
    

if __name__ == "__main__":
    main()