import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src/rectifier')))
import Rectifier
from utils import *
from datetime import date, timedelta
import math
import logging


def test_rectifier():
    r = Rectifier.Rectifier()
    r.set_geograph_long("W",60,38,22)
    r.set_HS_GMT(6.30777)
    r.set_GMT_Hour(-3)
    r.set_radix_bithdate(1976,12,26)
    r.set_radix_MC(297,36,8)
    r.add_event("Procedimiento de infiltración en la cadera",2026,4,21)
    r.add_event("Primer empleo profesional",2003,9,8)
    r.add_event("Primer casamiento",2005,8,20)
    r.add_event("Primera cita con Luza",2016,10,8)
    r.add_event("Jail",2005,11,20)
    r.add_event("Casamiento con Luza",2018,6,16)
    r.add_event("Casamiento civil con Luza",2023,9,22)
    r.add_event("Accidente lumbar con perdida de movilidad",2022,12,7)
    r.add_event("Primera separacion",2009,2,27)
    r.add_event("Ingreso a IBM de Colombia",2016,12,1)
    r.add_object(natal_chart_object(natal_chart_object.sun,5,5,56,natal_chart_object.capricorn))
    r.add_object(natal_chart_object(natal_chart_object.moon,17,9,43,natal_chart_object.piscis))
    r.add_object(natal_chart_object(natal_chart_object.mercury,23,7,48,natal_chart_object.capricorn))
    r.add_object(natal_chart_object(natal_chart_object.venus,20,1,49,natal_chart_object.aquarius))
    r.add_object(natal_chart_object(natal_chart_object.mars,12,3,48,natal_chart_object.sagittarius))
    r.add_object(natal_chart_object(natal_chart_object.jupiter,21,50,15,natal_chart_object.taurus))
    r.add_object(natal_chart_object(natal_chart_object.saturn,16,7,2,natal_chart_object.leo))
    r.add_object(natal_chart_object(natal_chart_object.uranus,10,40,8,natal_chart_object.scorpio))
    r.add_object(natal_chart_object(natal_chart_object.neptune,14,28,0,natal_chart_object.sagittarius))
    r.add_object(natal_chart_object(natal_chart_object.pluto,14,3,57,natal_chart_object.libra))
    r.add_object(natal_chart_object(natal_chart_object.mean_node,0,9,51,natal_chart_object.scorpio))
    r.add_object(natal_chart_object(natal_chart_object.AC,25,11,1,natal_chart_object.aries))
    r.add_object(natal_chart_object(natal_chart_object.II,23,39,59,natal_chart_object.taurus))
    r.add_object(natal_chart_object(natal_chart_object.III,24,46,52,natal_chart_object.gemini))
    r.add_object(natal_chart_object(natal_chart_object.IC,27,39,1,natal_chart_object.cancer))
    r.add_object(natal_chart_object(natal_chart_object.V,0,9,8,natal_chart_object.virgo))
    r.add_object(natal_chart_object(natal_chart_object.VI,29,44,59,natal_chart_object.virgo))

    new_HL = r.calculate()
    logging.info(f'nueva hora local {new_HL}')
    print(f'nueva hora local {new_HL}')
    assert new_HL == "14hs 40ms 19scs"