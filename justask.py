import os

from openai import OpenAI
from typing import List, Tuple


class Function:
    def __init__(
        self,
        description: str,
        examples: List[Tuple[str, str]],
        model: str = "gpt-4-turbo",
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

        client = OpenAI(
            api_key=os.environ["OPENAI_API_KEY"],
        )

        chat_completion = client.chat.completions.create(
            messages=self.messages
            + [
                {"role": "user", "content": arg},
            ],
            model=self.model,
        )

        return chat_completion.choices[0].message.content.strip()
