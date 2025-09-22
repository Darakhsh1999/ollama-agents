import ollama
from default_prompts import ASSISTANT_PROMPT
from ollama import Options

class LLM():

    def __init__(
        self,
        model_name: str,
        /,
        system_prompt: str = None,
        tools: list = None,
        *,
        default_system_prompt: bool = False,
        options: Options = None,
        temperature: float = 0.7,
        top_p: float = 0.9,
        top_k: int = 40,
        frequency_penalty: float = 0.5,
        presence_penalty: float = 0.5,
        repetition_penalty: float = 1.2,
        max_tokens: int = 1024,
        ):

        ollama.list() # List all available models
        if model_name not in ollama.list():
            raise ValueError(f"Model {model_name} not found. Use 'ollama pull <model_name>' to pull the model.")


        self.model_name = model_name
        self.messages: list[dict[str, str]] = []
        self.client = ollama.Client()
        self.capabilities = ollama.show(model_name).capabilities
        self.tools = tools

        # Model sampling parmeters
        if options:
            self.options = options
        else:
            self.options = Options(
            temperature=temperature,
            top_p=top_p,
            top_k=top_k,
            frequency_penalty=frequency_penalty,
            presence_penalty=presence_penalty,
            repetition_penalty=repetition_penalty,
            max_tokens=max_tokens,
        )

        # System prompt
        if system_prompt:
            self.messages.append({"role": "system", "content": system_prompt})
        elif default_system_prompt:
            self.messages.append({"role": "system", "content": ASSISTANT_PROMPT})

        # Tools
        if tools:
            assert isinstance(tools, list), f"Tools must be a list but got {type(tools)}"
            assert all(isinstance(tool, dict) for tool in tools), "All tools must be dictionaries"
            self.tools = tools


    def generate(self, prompt: str):
        self.messages.append({"role": "user", "content": prompt})

        # Invoke model
        response = self.client.chat(
            model=self.model_name,
            messages=self.messages,
            options=self.options,
        )

        self.messages.append({"role": "assistant", "content": response.message.content})

        return response.message.content


    def bind_tools(self, tools: list):
        assert isinstance(tools, list), f"Tools must be a list but got {type(tools)}"
        self.tools += tools





if __name__ == "__main__":

    llm = LLM("llama3.2", default_system_prompt=True)
    print(llm.generate("Hello my name is Bob and I am 30 years old. My favourite color is blue."))
    print(llm.generate("Recommended me a good jacket. What color should the jacket be?"))