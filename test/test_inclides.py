import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src/rectifier')))
import Rectifier
from utils import *
from datetime import date, timedelta
import math
import logging


def test_rectifier(includes):
    r = Rectifier.Rectifier()
    print(includes)
    r.set_includes(includes)



if __name__ == "__main__":
    includes = sys.argv[1]
    test_rectifier(includes)