import os
import json

from urllib import request
from typing import List, Tuple, Union


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


class Function:
    def __init__(
        self,
        description: str,
        examples: List[Tuple[str, str]] = [],
        model: Union[str, LLMModel] = LLamaCppModel(),
    ):
        system_prompt = f"""Perform the following task: {description}
Return only the output and nothing else."""

        self.messages = [
            {"role": "system", "content": system_prompt},
        ]

        for example in examples:
            self.messages.append({"role": "user", "content": example[0]})
            self.messages.append({"role": "assistant", "content": example[1]})

        if isinstance(model, str):
            self.model = get_backend(model)
        else:
            self.model = model

    def __call__(self, arg: str) -> str:
        return self.model.chat_completion(
            self.messages
            + [
                {"role": "user", "content": arg},
            ],
        )
