import unittest
from aspects import calculate_aspects

class TestAspects(unittest.TestCase):

    def test_calculate_aspects_basic(self):
        ra = 275.55
        aspects = calculate_aspects(ra)
        print(aspects)

        # Expected aspects for RA = 275.55 based on the implemented function:
        # Cuadratura (+/- 90):
        #   275.55 + 90 = 365.55 -> 5.55
        #   275.55 - 90 = 185.55
        # Trigono (+/- 120):
        #   275.55 + 120 = 395.55 -> 35.55
        #   275.55 - 120 = 155.55
        # Sextil (+/- 60):
        #   275.55 + 60 = 335.55
        #   275.55 - 60 = 215.55
        # Semicuadratura (+/- 45):
        #   275.55 + 45 = 320.55
        #   275.55 - 45 = 230.55
        # Semisextil (+/- 30):
        #   275.55 + 30 = 305.55
        #   275.55 - 30 = 245.55
        # Oposicion (+ 180):
        #   275.55 + 180 = 455.55 -> 95.55
        expected = {'cuadratura+': 5.55, 'cuadratura-': 185.55, 'trigono+': 35.55, 'trigono-': 155.55, 'sextil+': 335.55, 'sextil-': 215.55, 'semicuadratura+': 320.55, 'semicuadratura-': 230.55, 'semisextil+': 305.55, 'semisextil-': 245.55, 'oposicion': 95.55, 'quincuncio+': 65.55, 'quincuncio-': 125.55, 'sesquicuadratura+': 50.55, 'sesquicuadratura-': 140.55}

        # Using assertCountEqual because the order of elements in the list might not be guaranteed
        self.assertCountEqual(aspects, expected)

    def test_normalization(self):
        # Testing with RA = 350
        ra = 350.0
        aspects = calculate_aspects(ra)

        # Every value should be between 0 and 360
        for key,val in aspects.items():
            self.assertTrue(0 <= val < 360, f"Value {val} is not normalized")


if __name__ == '__main__':
    unittest.main()
