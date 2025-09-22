import ollama
from default_prompts import ASSISTANT_PROMPT
from ollama import Options, ChatResponse

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
        context_length: int = 4096,
        temperature: float = 0.7,
        top_p: float = 0.9,
        top_k: int = 40,
        max_tokens: int = -1,
        ):

        # Check model availability
        available_model_names = [x.model for x in ollama.list().models]
        if not any([(model.startswith(model_name)) for model in available_model_names]):
            raise ValueError(f"Model {model_name} not found. Use 'ollama pull <model_name>' to pull the model.")


        self.model_name = model_name
        self.messages: list[dict[str, str]] = []
        self.client = ollama.Client()
        self.capabilities = ollama.show(model_name).capabilities
        self.tools = []
        

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

        # System prompt
        if system_prompt:
            self.messages.append({"role": "system", "content": system_prompt})
        elif default_system_prompt:
            self.messages.append({"role": "system", "content": ASSISTANT_PROMPT})

        # Tools
        if tools:
            self.bind_tools(tools)
        else:
            self.tools = []
            self.available_tools = {}
        
    def invoke(self) -> ChatResponse:
        """ Invoke the model """
        response = self.client.chat(
            model=self.model_name,
            messages=self.messages,
            options=self.options,
            tools=self.tools,
        )
        return response


    def generate(self, prompt: str) -> str:
        """ Generate a response from the model """

        # Initial user message
        self.messages.append({"role": "user", "content": prompt})
        response = self.invoke()
        self.messages.append(response.message)

        # Tool calling loop
        while tool_call_list := response.message.tool_calls:
            for tool_call in tool_call_list:
                if function_to_call := self.available_tools.get(tool_call.function.name):
                    print(f"Calling tool {tool_call.function.name}")
                    output = function_to_call(**tool_call.function.arguments)
                    self.messages.append({'role': 'tool', 'content': str(output), 'tool_name': tool_call.function.name})
                else:
                    self.messages.append({'role': 'tool', 'content': f"Function {tool_call.function.name} not found", 'tool_name': tool_call.function.name})

            response = self.invoke()
            self.messages.append(response.message)

        return response.message.content


    def bind_tools(self, tools: list):

        assert isinstance(tools, list), f"Tools must be a list but got {type(tools)}"
        assert all(callable(tool) for tool in tools), "All tools must be callable"
        if self.tools:
            self.tools += tools
            self.available_tools.update({tool.__name__: tool for tool in tools})
        else:
            self.tools = tools
            self.available_tools = {tool.__name__: tool for tool in tools}





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


    # Tool calling
    def get_weather(city: str) -> str:
        return f"The weather in {city} is currently sunny."
    llm = LLM("llama3.2", default_system_prompt=True, tools=[get_weather])
    print(llm.generate("What is the weather in Stockholm at this moment?"))