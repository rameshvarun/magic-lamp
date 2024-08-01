# magic-lamp
[![PyPI - Version](https://img.shields.io/pypi/v/magic-lamp)](https://pypi.org/project/magic-lamp/)

Easily integrate LLM calls into Python code.

```bash
pip install magic-lamp
```

## Example

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

By default, `magic-lamp` downloads and runs a local LLM.

## Alternatives
- https://github.com/jackmpcollins/magentic
