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
    if includes is not None:
        r.set_includes(includes)

    r.set_geograph_long("W",76,31,0)
    r.set_HS_GMT(18.348055)
    r.set_GMT_Hour(-5)
    r.set_radix_bithdate(1975,6,28)
    r.set_radix_MC(270,8,13)
    #r.set_orbe_tolerance(0.15)

    r.add_event("Comienzo empleo profesional",2001,3,1)
    r.add_event("Renuncia",2023,6,27)
    r.add_event("Matrimonio",1995,6,16)
    r.add_event("Matrimonio",2018,6,16)
    r.add_event("Matrimonio",2011,11,11)
    r.add_event("Divorcio",2013,1,18)
    r.add_event("Comienzo de relación romántica",2016,10,8)
    r.add_event("Jail",2016,10,8)
    r.add_event("Casamiento civil con Mariano",2023,9,22)
    r.add_event("Mundanza al campo",2022,5,13)
    r.add_event("Nacimiento de hijo",1997,6,22)
    r.add_event("Nacimiento de hijo",1999,3,17)
    r.add_event("Graduación biorreprogramación",2016,11,13)
    r.add_event("Graduación MTC neijing",2023,11,12)
    r.add_event("Graduación colegio secundario",1992,11,12)
    r.add_event("Enfermedad",2021,8,10)

    r.add_object(natal_chart_object(natal_chart_object.sun,6,50,25,natal_chart_object.cancer))
    r.add_object(natal_chart_object(natal_chart_object.moon,9,35,16,natal_chart_object.piscis))
    r.add_object(natal_chart_object(natal_chart_object.mercury,16,42,24,natal_chart_object.gemini))
    r.add_object(natal_chart_object(natal_chart_object.venus,21,46,31,natal_chart_object.leo))
    r.add_object(natal_chart_object(natal_chart_object.mars,28,35,59,natal_chart_object.aries))
    r.add_object(natal_chart_object(natal_chart_object.jupiter,21,21,36,natal_chart_object.aries))
    r.add_object(natal_chart_object(natal_chart_object.saturn,20,23,6,natal_chart_object.cancer))
    r.add_object(natal_chart_object(natal_chart_object.uranus,28,23,9,natal_chart_object.libra))
    r.add_object(natal_chart_object(natal_chart_object.neptune,9,42,36,natal_chart_object.sagittarius))
    r.add_object(natal_chart_object(natal_chart_object.pluto,6,31,16,natal_chart_object.libra))
    r.add_object(natal_chart_object(natal_chart_object.mean_node,0,16,21,natal_chart_object.sagittarius))
    r.add_object(natal_chart_object(natal_chart_object.AC,2,23,29,natal_chart_object.aries))
    r.add_object(natal_chart_object(natal_chart_object.II,4,47,26,natal_chart_object.taurus))
    r.add_object(natal_chart_object(natal_chart_object.III,4,32,48,natal_chart_object.gemini))
    r.add_object(natal_chart_object(natal_chart_object.IC,1,57,39,natal_chart_object.cancer))
    r.add_object(natal_chart_object(natal_chart_object.XI,29,32,58,natal_chart_object.capricorn))
    r.add_object(natal_chart_object(natal_chart_object.XII,29,33,13,natal_chart_object.aquarius))

    new_HL = r.calculate()
    logging.info(f'nueva hora local {new_HL}')
    print(f'nueva hora local {new_HL}')
    #assert new_HL == "14hs 40ms 21scs"


if __name__ == "__main__":
    if len(sys.argv) < 2:
        test_rectifier(None)
    else:
        includes = sys.argv[1]
        test_rectifier(includes)