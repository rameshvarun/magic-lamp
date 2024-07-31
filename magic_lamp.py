import os
import json

from urllib import request
from typing import List, Tuple


class Function:
    def __init__(
        self,
        description: str,
        examples: List[Tuple[str, str]],
        model: str = "gpt-4o-mini",
    ):
        system_prompt = f"""Perform the following task: {description}
Return only the output and nothing else."""

        self.messages = [
            {"role": "system", "content": system_prompt},
        ]

        for example in examples:
            self.messages.append({"role": "user", "content": example[0]})
            self.messages.append({"role": "assistant", "content": example[1]})

        self.model = model

    def __call__(self, arg: str) -> str:
        if "OPENAI_API_KEY" not in os.environ:
            raise Exception("OPENAI_API_KEY not found in environment.")

        payload = {
            "model": self.model,
            "messages": self.messages
            + [
                {"role": "user", "content": arg},
            ],
        }

        req = request.Request(
            "https://api.openai.com/v1/chat/completions", method="POST"
        )
        req.add_header("Content-Type", "application/json")
        req.add_header("Authorization", f'Bearer {os.environ["OPENAI_API_KEY"]}')
        with request.urlopen(req, data=json.dumps(payload).encode()) as f:
            response = json.loads(f.read())

        return response['choices'][0]['message']['content'].strip()
