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


if __name__ == "__main__":
    unittest.main()
