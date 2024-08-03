import magic_lamp
import unittest


class TestMagicLamp(unittest.TestCase):
    def test_return_str(self):
        format_name = magic_lamp.Function(
            "Format this surname in a way that it would be written out.",
            examples=[
                ("PERALTA", "Peralta"),
                ("OCONNELL", "O'Connell"),
                ("MCDONALD", "McDonald"),
            ],
        )

        self.assertEqual(format_name("MCDOWELL"), "McDowell")
        self.assertEqual(format_name("ONEILL"), "O'Neill")

    def test_president(self):
        next_president = magic_lamp.Function(
            "Return the name of the president that followed the given president.",
            examples=[
                ("George Washington", "John Adams"),
                ("William Henry Harrison", "John Tyler"),
            ],
        )

        self.assertEqual(next_president("Calvin Coolidge"), "Herbert Hoover")
    
    def test_return_boolean(self):
        is_positive = magic_lamp.Function(
            "Return True if this movie review is positive, else return False.",
            examples=[
                ("An exceptionally smart, brooding picture with some terrific performances.", True),
                ("Ugly, annoying and inconsistent.", False),
            ],
        )

        self.assertEqual(is_positive("The final moments of Infinity War are haunting and impactful and mysterious."), True)
    
    def test_return_set(self):
        get_atoms = magic_lamp.Function(
            "Break this molecule down into it's consituent atoms. Return as a set.",
            examples=[
                ("water", {"hydrogen", "oxygen"}),
                ("glucose", {"carbon", "hydrogen", "oxygen"}),
            ],
        )

        self.assertEqual(get_atoms("ammonia"), {"nitrogen", "hydrogen"})

    @unittest.skip("Needs chain of thought to make it better.")
    def test_return_number(self):
        count_s = magic_lamp.Function(
            "Count the number of instances of the letter 's' in the word.",
            examples=[("mississippi", 4), ("hello", 0), ("sugar", 1)],
        )

        self.assertEqual(count_s("supercalifragilisticexpialidocious"), 3)

    def test_models_cache(self):
        """Ensure that loaded models are being cached and not re-loaded for every function."""

        functions = []
        for i in range(20):
            functions.append(
                magic_lamp.Function(
                    "Write this number out in words.",
                    examples=[
                        (1, "one"),
                        (35, "thirty-five"),
                        (15690, "fifteen thousand, six hundred ninety"),
                    ],
                )
            )

        self.assertEqual(
            functions[0](328745226793),
            "three hundred twenty-eight billion, seven hundred forty-five million, two hundred twenty-six thousand, seven hundred ninety-three",
        )


if __name__ == "__main__":
    unittest.main()
