# magic-lamp
[![PyPI - Version](https://img.shields.io/pypi/v/magic-lamp)](https://pypi.org/project/magic-lamp/)

Create magic LLM-powered Python functions that return anything you ask for. Many caveats.

## Quickstart

```bash
pip install magic-lamp
```

Define a function with a description and a set of examples.

```python
import magic_lamp

get_atoms = magic_lamp.Function(
    "Break this molecule down into it's constituent atoms. Return as a set.",
    examples=[
        ("water", {"hydrogen", "oxygen"}),
        ("glucose", {"carbon", "hydrogen", "oxygen"}),
    ],
)

print(get_atoms("ammonia")) # => {"nitrogen", "hydrogen"}
```

Functions can return any Python literal (strings, numbers, dicts, tuples lists, etc). No API keys are required, since by default `magic-lamp` downloads and runs a local LLM.

## Configuring the LLM

By default, `magic-lamp` downloads and runs a local LLM from Hugging Face. For more complex tasks, OpenAI models will perform better.

### Using OpenAI

`OPENAI_API_KEY` must be set in the environment. Pass in the name of a `gpt-*` model to the function constructor.

```python
import magic_lamp

format_number = magic_lamp.Function(
    'Write this number out in words.',
    examples=[
        (1, "one"),
        (35, "thirty-five"),
        (15690, "fifteen thousand, six hundred ninety"),
    ],
    model="gpt-4o-mini"
)

print(format_number(328745226793))
```

## Links
- https://github.com/jackmpcollins/magentic - A similar concept but using decorators.
- https://github.com/PrefectHQ/marvin - Antoher similar concept.
- https://github.com/abetlen/llama-cpp-python - Used by this library to run the local LLM.
- https://ai.meta.com/blog/meta-llama-3-1/ - Llama 3.1 8b is the default model.
- https://huggingface.co/bullerwins/Meta-Llama-3.1-8B-Instruct-GGUF - Uses these GGUFs by default.
