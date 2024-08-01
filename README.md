# magic-lamp
[![PyPI - Version](https://img.shields.io/pypi/v/magic-lamp)](https://pypi.org/project/magic-lamp/)

Easily integrate LLM calls into Python code. By default, uses a local LLM.

## Quickstart

```bash
pip install magic-lamp
```

Define a function with a description and a set of examples.

```python
import magic_lamp

format_name = magic_lamp.Function(
    'Format this surname in a way that it would be written out.',
    examples=[
        ("PERALTA", "Peralta"),
        ("OCONNELL", "O'Connel"),
        ("MCDONALD", "McDonald")
    ],
)

print(format_name("MCDOWELL"))
```

## Configuring the LLM

By default, `magic-lamp` downloads and runs a local LLM from Hugging Face. For more complex tasks, OpenAI models will perform better.

### Using OpenAI

`OPENAI_API_KEY` must be set in the environment. Pass in the name of a `gpt-*` model to the function constructor.

```python
import magic_lamp

format_number = magic_lamp.Function(
    'Write this number out in words.',
    examples=[
        ("1", "one"),
        ("35", "thirty-five"),
        ("15690", "fifteen thousand, six hundred ninety"),
    ],
    model="gpt-4o-mini"
)

print(format_number("328745226793"))
```

## Links
- https://github.com/jackmpcollins/magentic - A similar concept but using decorators.
- https://github.com/abetlen/llama-cpp-python - Used by this library to run the local LLM.
- https://ai.meta.com/blog/meta-llama-3-1/ - Llama 3.1 8b is the default model.
- https://huggingface.co/bullerwins/Meta-Llama-3.1-8B-Instruct-GGUF - Uses these GGUFs by default.
