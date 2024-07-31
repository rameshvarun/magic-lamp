import os

from openai import OpenAI
from typing import Any, List, Tuple


class Function:
    def __init__(
        self, description, examples: List[Tuple[str, str]] = [], model="gpt-4-turbo"
    ):
        self.system_prompt = f"""Perform the following task.
Task Description: {description}

EXAMPLES:"""

        for example in examples:
            self.system_prompt += f"""
{example[0]} -> {example[1]}"""

        self.model = model

    def __call__(self, arg: str) -> str:
        if "OPENAI_API_KEY" not in os.environ:
            raise Exception("OPENAI_API_KEY not found in environment.")

        client = OpenAI(
            api_key=os.environ["OPENAI_API_KEY"],
        )

        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": self.system_prompt,
                },
                {"role": "user", "content": arg},
            ],
            model=self.model,
        )

        return chat_completion.choices[0].message.content.strip()
