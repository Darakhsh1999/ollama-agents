import ollama

class LLM():

    def __init__(
        self,
        model_name: str,
        system_prompt: str = None,
        tools: list = None,
        ):

        self.model_name = model_name
        self.messages: list[dict[str, str]] = []
        self.client = ollama.Client()

        # System prompt
        if system_prompt:
            self.messages.append({"role": "system", "content": system_prompt})

        # Tools
        if tools:
            assert isinstance(tools, list), f"Tools must be a list but got {type(tools)}"
            assert all(isinstance(tool, dict) for tool in tools), "All tools must be dictionaries"
            self.tools = tools


    def generate(self, prompt: str):
        self.messages.append({"role": "user", "content": prompt})
        response = self.client.chat(
            model=self.model_name,
            messages=self.messages,
            tools=self.tools,
        )
        self.messages.append({"role": "assistant", "content": response.message.content})
        return response.message.content


    def bind_tools(self, tools: list):
        assert isinstance(tools, list), f"Tools must be a list but got {type(tools)}"
        self.tools += tools





if __name__ == "__main__":

    llm = LLM("llama3.2")
    print(llm.generate("Hello, how are you? Could you please tell me the weather in Berlin?"))