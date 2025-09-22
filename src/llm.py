import ollama
from default_prompts import ASSISTANT_PROMPT
from ollama import Options, ChatResponse

class LLM():

    def __init__(
        self,
        model_name: str,
        *,
        use_thinking: bool = False,
        options: Options = None,
        context_length: int = 4096,
        temperature: float = 0.7,
        top_p: float = 0.9,
        top_k: int = 40,
        max_tokens: int = -1,
        ):

        # Check model availability
        available_model_names = [x.model for x in ollama.list().models]
        if not any([(model.startswith(model_name)) for model in available_model_names]):
            raise ValueError(f"Model {model_name} not found. Use 'ollama pull <model_name>' to pull specific model.\nAvailable local models:\n- {"\n- ".join(available_model_names)}")

        # Ollama Client
        self.model_name = model_name
        self.client = ollama.Client()
        self.capabilities = ollama.show(model_name).capabilities

        # Reasoning
        if "thinking" in self.capabilities:
            self.use_thinking = use_thinking
        else:
            print(f"Warning: Model {model_name} does not support reasoning. Setting use_thinking to False")
            self.use_thinking = False

        # Model sampling parmeters
        if options:
            self.options = options
        else:
            self.options = Options(
                num_ctx=context_length,
                temperature=temperature,
                top_p=top_p,
                top_k=top_k,
                num_predict=max_tokens
        )

        
    def generate(self, messages: list[dict[str, str]], tools: list = None) -> ChatResponse:
        """ Invoke the model """
        return self.client.chat(
            model=self.model_name,
            messages=messages,
            options=self.options,
            tools=tools,
            think=self.use_thinking,
        )



if __name__ == "__main__":

    print("Running main")

    # # Multi conversation
    # llm = LLM("llama3.2", default_system_prompt=True)
    # print(llm.generate("Hello my name is Bob and I am 30 years old. My favourite color is blue."))
    # print(llm.generate("Recommended me a good jacket. What color should the jacket be?"))

    # # Options
    # options = Options(num_ctx=1024, temperature=0.9)
    # llm = LLM("llama3.2", default_system_prompt=True, options=options)
    # print(llm.generate("Give me a 3 sentence poem about boats and the color blue"))

    # # Custom options
    # llm = LLM("llama3.2", default_system_prompt=True, context_length=1024, temperature=0)
    # print(llm.generate("What is the capital of France, Sweden and Germany?"))


    # # Tool calling
    # def get_weather(city: str) -> str:
    #     return f"The weather in {city} is currently sunny."
    # llm = LLM("llama3.2", default_system_prompt=True, tools=[get_weather])
    # print(llm.generate("What is the weather in Stockholm at this moment?"))

    llm0 = LLM("ldiwoanoinlama3.2", use_thinking=True)
    llm1 = LLM("llama3.2", use_thinking=True)
    llm2 = LLM("qwen3:4b", use_thinking=True)
    llm2 = LLM("gemma3", use_thinking=True)