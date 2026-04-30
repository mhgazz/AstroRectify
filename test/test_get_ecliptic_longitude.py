import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src/rectifier')))
import Rectifier
from utils import *
from datetime import date, timedelta
import math
import logging

logging.basicConfig(level=logging.INFO)

def test_get_ecliptic_longitude_2():

    RAMC_radix = get_RAMC(113,26,10)
    logging.info(f'RAMC del radix {RAMC_radix}')
    eclp_long = get_ecliptic_longitude(RAMC_radix)
    logging.info(f'eclipting longide {eclp_long}')
    g,m,s = get_angle_sexag(eclp_long)
    logging.info(f'sexagecimal angle: {g} {m} {s}')

    assert g == 113
    assert m == 26
    assert s == 10
    
def test_get_ecliptic_longitude_4():
    RAMC_radix = get_RAMC(297,36,8)
    logging.info(f'RAMC del radix {RAMC_radix}')
    eclp_long = get_ecliptic_longitude(RAMC_radix)
    logging.info(f'eclipting longide {eclp_long}')
    g,m,s = get_angle_sexag(eclp_long)
    logging.info(f'sexagecimal angle: {g} {m} {s}')

    assert g == 297
    assert m == 36
    assert s == 8

def test_get_ecliptic_longitude_1():
    RAMC_radix = get_RAMC(76,36,8)
    logging.info(f'RAMC del radix {RAMC_radix}')
    eclp_long = get_ecliptic_longitude(RAMC_radix)
    logging.info(f'eclipting longide {eclp_long}')
    g,m,s = get_angle_sexag(eclp_long)
    logging.info(f'sexagecimal angle: {g} {m} {s}')

    assert g == 76
    assert m == 36
    assert s == 8

def test_get_ecliptic_longitude_3():
    RAMC_radix = get_RAMC(198,3,28)
    logging.info(f'RAMC del radix {RAMC_radix}')
    eclp_long = get_ecliptic_longitude(RAMC_radix)
    logging.info(f'eclipting longide {eclp_long}')
    g,m,s = get_angle_sexag(eclp_long)
    logging.info(f'sexagecimal angle: {g} {m} {s}')

    assert g == 198
    assert m == 3
    assert s == 28


if __name__ == "__main__":
    test_get_ecliptic_longitude()

    
    #cur_arc = 12.93713634
    # direccionar el arco sobre el MC
    #direct = RAMC_radix + cur_arc
    #converse = RAMC_radix - cur_arc
    #logging.info(f'direct RA: {direct}')
    #logging.info(f'converse RA: {converse}')
    #eclep_longitude_direct = get_ecliptic_longitude(direct)
    #eclep_longitude_converse = get_ecliptic_longitude(converse)
    #logging.info(f'direct Ecliptic longitude: {eclep_longitude_direct}')
    #logging.info(f'converse Ecliptic longitude: {eclep_longitude_converse}')