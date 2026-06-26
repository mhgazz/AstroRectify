import unittest
import math
from utils import get_RA_from_decimal
from utils import get_declination
from utils import get_d_m

class TestUtils(unittest.TestCase):
    
    def test_example(self):
        # Replace with actual function calls from utils.py
        # self.assertEqual(utils.some_function(), expected_value)
        pass

    def test_get_d_m(self):
        self.assertAlmostEqual(get_d_m(49.69 ,299.82,119.83,1),119.83-49.69,places=5)

    def test_get_RA_from_decimal(self):
        # Test case 1: A simple positive angle
        # For dec_angle = 0, RA should be 0
        self.assertAlmostEqual(get_RA_from_decimal(0), 0.0, places=5)

        # Test case 2: A positive angle where tan_long is positive
        # Example: dec_angle = 45 degrees
        # radian_angle = math.radians(45)
        # tan_long = math.tan(radian_angle) = 1
        # cos_dec = math.cos(math.radians(23.44))
        # ra_rad = math.atan(1 * cos_dec)
        # RA = math.degrees(ra_rad)
        # Expected value can be calculated manually or using a calculator
        dec_angle_1 = 320.1
        obliquity = 23.44
        expected_ra = 322.50710592723874
        self.assertAlmostEqual(get_RA_from_decimal(dec_angle_1), expected_ra, places=5)

        # Test case 3: A negative angle
        dec_angle_2 = 111.84
        expected_ra_2 = 113.6
        actual = get_RA_from_decimal(dec_angle_2)
        self.assertAlmostEqual(actual, expected_ra_2, places=5)

        # Test case 4: Angle around 90 degrees (where tan goes to infinity)
        # The function handles this implicitly through math.atan, but it's good to test
        # For 90 degrees, tan is undefined, but for values close to 90, it's very large.
        # Let's pick a value slightly less than 90
        dec_angle_3 = 89.9
        radian_angle_3 = math.radians(dec_angle_3)
        tan_long_3 = math.tan(radian_angle_3)
        expected_ra_rad_3 = math.atan(tan_long_3 * cos_dec)
        expected_ra_3 = math.degrees(expected_ra_rad_3)
        self.assertAlmostEqual(get_RA_from_decimal(dec_angle_3), expected_ra_3, places=5)

        # Test case 5: Angle around 180 degrees
        dec_angle_4 = 180.0
        self.assertAlmostEqual(get_RA_from_decimal(dec_angle_4), 0.0, places=5) # tan(180) = 0

        # Test case 6: Angle around 270 degrees
        dec_angle_5 = 269.9
        radian_angle_5 = math.radians(dec_angle_5)
        tan_long_5 = math.tan(radian_angle_5)
        expected_ra_rad_5 = math.atan(tan_long_5 * cos_dec)
        expected_ra_5 = math.degrees(expected_ra_rad_5)
        # The original function has conditional logic for RA < 0 and RA > 180/270.
        # Let's trace for dec_angle_5 = 269.9
        # tan(269.9) is a large positive number
        # ra_rad will be positive, RA will be positive.
        # The condition `if (RA<0)` will be false.
        # The condition `if RA >180` will be true.
        # So, RA = 180 + RA.
        # Let's calculate the expected value considering this logic.
        calculated_ra_5 = get_RA_from_decimal(dec_angle_5)
        self.assertAlmostEqual(calculated_ra_5, 180 + expected_ra_5, places=5)


if __name__ == '__main__':
    unittest.main()