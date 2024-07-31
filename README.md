# justask

Easily integrate LLM calls into Python code.

```python
import justask

format_name = justask.Function(
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
