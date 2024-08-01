import magic_lamp

format_name = magic_lamp.Function(
    "Format this surname in a way that it would be written out.",
    examples=[
        ("PERALTA", "Peralta"),
        ("OCONNELL", "O'Connel"),
        ("MCDONALD", "McDonald"),
    ],
)

print(format_name("MCDOWELL"))
