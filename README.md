# magic-lamp
[![PyPI - Version](https://img.shields.io/pypi/v/magic-lamp)](https://pypi.org/project/magic-lamp/)

Easily integrate LLM calls into Python code.

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

By default, `magic-lamp` downloads and runs a local LLM. For more complex tasks, use OpenAI.

## Configuring the LLM

### Using OpenAI

`OPENAI_API_KEY` must be set in the environment. Pass in the name of a `gpt-*` model to the function constructor.

```python
import magic_lamp

format_number = magic_lamp.Function(
    'Write this number out in words.',
    examples=[
        ("1", "one"),
        ("35", "thirty-five"),
        ("15,690", "fifteen thousand, six hundred ninety"),
    ],
    model="gpt-4o-mini"
)

print(format_number("328,745,226,793"))
```

## Alternatives
- https://github.com/jackmpcollins/magentic
- https://github.com/abetlen/llama-cpp-python
