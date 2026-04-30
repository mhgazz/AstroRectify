import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src/rectifier')))
import Rectifier
from utils import *
from datetime import date, timedelta
import math


def test():
    r = Rectifier.Rectifier()
    r.set_geograph_long("W",60,38,22)
    r.set_HS_GMT(20.35527)
    r.set_GMT_Hour(-3)
    r.set_radix_bithdate(1949,7,28)
    r.set_radix_MC(113,26,10)
    r.add_event("Fallecimiento de hermano",1962,9,12)
    r.add_event("Graduacion",1971,12,17)
    r.add_event("Casamiento",1976,1,3)
    r.add_event("Nacimiento de hijo",1976,12,26)
    r.add_event("Nacimiento de hija",1978,10,22)
    r.add_event("Nacimiento de hija",1980,4,22)
    r.add_object(natal_chart_object(natal_chart_object.sun,5,11,34,natal_chart_object.leo))
    r.add_object(natal_chart_object(natal_chart_object.moon,13,7,24,natal_chart_object.virgo))
    r.add_object(natal_chart_object(natal_chart_object.mercury,7,10,54,natal_chart_object.leo))
    r.add_object(natal_chart_object(natal_chart_object.venus,2,24,14,natal_chart_object.virgo))
    r.add_object(natal_chart_object(natal_chart_object.mars,3,37,27,natal_chart_object.cancer))
    r.add_object(natal_chart_object(natal_chart_object.jupiter,26,11,47,natal_chart_object.capricorn))
    r.add_object(natal_chart_object(natal_chart_object.saturn,5,11,23,natal_chart_object.virgo))
    r.add_object(natal_chart_object(natal_chart_object.uranus,2,48,48,natal_chart_object.cancer))
    r.add_object(natal_chart_object(natal_chart_object.neptune,12,42,57,natal_chart_object.libra))
    r.add_object(natal_chart_object(natal_chart_object.pluto,15,50,7,natal_chart_object.leo))
    r.add_object(natal_chart_object(natal_chart_object.mean_node,20,23,31,natal_chart_object.aries))
    r.add_object(natal_chart_object(natal_chart_object.AC,6,46,34,natal_chart_object.scorpio))
    r.add_object(natal_chart_object(natal_chart_object.II,6,58,0,natal_chart_object.sagittarius))
    r.add_object(natal_chart_object(natal_chart_object.III,0,40,0,natal_chart_object.capricorn))
    r.add_object(natal_chart_object(natal_chart_object.IC,23,26,10,natal_chart_object.capricorn))
    r.add_object(natal_chart_object(natal_chart_object.V,19,33,00,natal_chart_object.aquarius))
    r.add_object(natal_chart_object(natal_chart_object.VI,23,41,0,natal_chart_object.piscis))

    new_HL = r.calculate()
    print(f'nueva hora local {new_HL}')


if __name__ == '__main__':
    test()