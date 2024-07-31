# magic-lamp
![PyPI - Version](https://img.shields.io/pypi/v/magic-lamp)

Easily integrate LLM calls into Python code. Requires environment variable `OPENAI_API_KEY` to be set.

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
    model="gpt-4o-mini"
)

print(format_name("MCDOWELL"))
```

## Alternatives
- https://github.com/jackmpcollins/magentic
