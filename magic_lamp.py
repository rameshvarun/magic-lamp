import os
import json
import ast

from urllib import request
from typing import List, Tuple, Union, Any, Literal

def is_literal(value: Any) -> bool:
    """
    Check if 'value' object can be serialized and deserialized
    using a combination of 'repr' and 'ast.literal_eval'.
    """
    try:
        return value == ast.literal_eval(repr(value))
    except:
        return False


class LLMModel:
    def chat_completion(self, messages) -> str:
        raise NotImplementedError("chat_completion not implemented.")


class LLamaCppModel(LLMModel):
    def __init__(
        self,
        repo_id="bullerwins/Meta-Llama-3.1-8B-Instruct-GGUF",
        filename="Meta-Llama-3.1-8B-Instruct-Q4_K_M.gguf",
    ):
        from llama_cpp import Llama

        self.llm = Llama.from_pretrained(
            repo_id=repo_id, filename=filename, verbose=False
        )

    def chat_completion(self, messages) -> str:
        result = self.llm.create_chat_completion(messages=messages)
        return result["choices"][0]["message"]["content"].strip()


class OpenAIModel(LLMModel):
    def __init__(self, model: str):
        if "OPENAI_API_KEY" not in os.environ:
            raise Exception("OPENAI_API_KEY not found in environment.")

        self.model = model
        self.api_key = os.environ["OPENAI_API_KEY"]

    def chat_completion(self, messages) -> str:
        payload = {
            "model": self.model,
            "messages": messages,
        }

        req = request.Request(
            "https://api.openai.com/v1/chat/completions", method="POST"
        )
        req.add_header("Content-Type", "application/json")
        req.add_header("Authorization", f"Bearer {self.api_key}")

        with request.urlopen(req, data=json.dumps(payload).encode()) as f:
            response = json.loads(f.read())

        return response["choices"][0]["message"]["content"].strip()


class OllamaModel(LLMModel):
    def __init__(self, model: str):
        self.model = model

        req = request.Request("http://localhost:11434/api/pull", method="POST")
        req.add_header("Content-Type", "application/json")

        payload = {"name": self.model, "stream": False}
        with request.urlopen(req, data=json.dumps(payload).encode()) as f:
            json.loads(f.read())

    def chat_completion(self, messages) -> str:
        payload = {
            "model": self.model,
            "messages": messages,
            "stream": False,
        }

        req = request.Request("http://localhost:11434/api/chat", method="POST")
        req.add_header("Content-Type", "application/json")

        with request.urlopen(req, data=json.dumps(payload).encode()) as f:
            response = json.loads(f.read())

        return response["message"]["content"].strip()


def get_backend(model_name: str) -> LLMModel:
    """Automatically construct a backend using the model name."""
    if model_name.startswith("gpt-"):
        return OpenAIModel(model_name)
    else:
        raise Exception(
            f"Couldn't automatically create backend for model name: {model_name}"
        )


OutputType = Literal["string", "ast-literal"]

_default_model = None

def get_default_model() -> LLMModel:
    global _default_model

    if _default_model == None:
        _default_model = LLamaCppModel()

    return _default_model


class Function:
    def __init__(
        self,
        description: str,
        examples: List[Tuple[str, str]] = [],
        model: Union[str, LLMModel] = None,
    ):
        if model == None:
            self.model = get_default_model()
        elif isinstance(model, str):
            self.model = get_backend(model)
        else:
            self.model = model

        self.output_type = self._get_output_type(examples)

        system_prompt = f"Perform the following task: {description}"

        if self.output_type == "string":
            system_prompt += """
Return only the output and nothing else. Do not wrap in quotation marks."""
        elif self.output_type == "ast-literal":
            system_prompt += """
Return your result as a Python literal. Characters in strings must be properly escaped.

Examples of Python Literals:
45.03 # This is a number.
False # This is a boolean.
'that\\'s' # This is an escaped string.
"\\"hello world\\"" # This is an escaped string.
['a', 1, 2, 3] # This is a list of elements
{'x', 'y', 'z'} # This is a set of elements.
('a', 3) # This is a tuple."""
        else:
            raise Exception(f"Unknown output type: {self.output_type}")

        self.messages = [
            {"role": "system", "content": system_prompt},
        ]

        for example in examples:
            self.messages.append(
                {"role": "user", "content": self._format_input(example[0])}
            )
            self.messages.append(
                {"role": "assistant", "content": self._format_output(example[1])}
            )


    def _format_output(self, output: Any) -> str:
        if self.output_type == "string":
            return output
        elif self.output_type == "ast-literal":
            return repr(output)
        else:
            raise Exception(f"Unknown output type: {self.output_type}")

    def _format_input(self, input_val) -> str:
        if isinstance(input_val, str):
            return input_val
        else:
            return repr(input_val)

    def _get_output_type(self, examples: List[Tuple[Any, Any]]) -> OutputType:
        """
        Depending on the type of the outputs (as deduced from the examples),
        different prompting strategies will be used.
        """

        outputs = [e[1] for e in examples]

        if len(outputs) == 0:
            # If no examples were provided, the output type is 'string'.
            return "string"
        elif all(isinstance(o, str) for o in outputs):
            return "string"
        elif all(is_literal(o) for o in outputs):
            return "ast-literal"
        else:
            raise Exception("Outputs must be Python literals.")

    def _parse_output(self, output: str) -> Any:
        if self.output_type == "string":
            return output
        elif self.output_type == "ast-literal":
            try:
                return ast.literal_eval(output)
            except (SyntaxError, ValueError):
                raise Exception(f"Failed to parse LLM output: {output}")
        else:
            raise Exception(f"Unknown output type: {self.output_type}")

    def __call__(self, *args: str) -> str:
        if len(args) == 1:
            content = self._format_input(args[0])
        else:
            content = self._format_input(args)

        messages = self.messages + [
            {"role": "user", "content": content},
        ]
        completion = self.model.chat_completion(messages)
        return self._parse_output(completion)
