import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src/rectifier')))
import Rectifier
from utils import *
from datetime import date, timedelta
import math
import logging

logging.basicConfig(level=logging.INFO)

def test_get_angle_sexag():
    eclp_long = 113.4361111111111
    g,m,s = get_angle_sexag(eclp_long)
    logging.info(f'sexagecimal angle: {g} {m} {s}')

    assert g == 113
    assert m == 26
    assert s == 10