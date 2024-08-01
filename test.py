import magic_lamp
import unittest


class TestMagicLamp(unittest.TestCase):
    def test_basic(self):
        format_name = magic_lamp.Function(
            "Format this surname in a way that it would be written out.",
            examples=[
                ("PERALTA", "Peralta"),
                ("OCONNELL", "O'Connel"),
                ("MCDONALD", "McDonald"),
            ],
        )

        self.assertEqual(format_name("MCDOWELL"), "McDowell")

    def test_stability(self):
        """Check if a model actually returns a consistent answer."""

        format_name = magic_lamp.Function(
            "Format this surname in a way that it would be written out.",
            examples=[
                ("PERALTA", "Peralta"),
                ("OCONNELL", "O'Connel"),
                ("MCDONALD", "McDonald"),
            ],
        )

        for i in range(100):
            self.assertEqual(format_name("MCDOWELL"), "McDowell")

    def test_models_cache(self):
        """Ensure that loaded models are being cached and not re-loaded for every function."""

        functions = []
        for i in range(20):
            functions.append(
                magic_lamp.Function(
                    "Write this number out in words.",
                    examples=[
                        ("1", "one"),
                        ("35", "thirty-five"),
                        ("15,690", "fifteen thousand, six hundred ninety"),
                    ],
                )
            )

        self.assertEqual(
            functions[0]("328,745,226,793"),
            "three hundred twenty-eight billion, seven hundred forty-five million, two hundred twenty-six thousand, seven hundred ninety-three",
        )


if __name__ == "__main__":
    unittest.main()
