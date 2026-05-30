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
    r.set_geograph_long("W",75,32,0)
    hs_gmt = convert_angle_decimal(10,58,24)
    #print(f'hora de Greenwich sideral gmt {str(hs_gmt)}')
    r.set_HS_GMT(hs_gmt) #hora de la efemeride del dia 12am convertida a decimales
    r.set_GMT_Hour(-5)
    r.set_radix_bithdate(1977,3,7)
    r.set_radix_MC(168,1,53)
    r.set_orbe_tolerance(0.9)
    r.add_event("Comienzo de relación romántica",1992,2,14)
    r.add_event("Matrimonio",2000,5,6)
    r.add_event("Nacimiento de hija",2000,3,4)
    r.add_event("Mudanza a EEUU",2016,11,6)
    r.add_event("Matrimonio",2017,2,27)
    r.add_event("Relación romántica",2018,8,10)
    r.add_event("Rompimiento de relación romántica",2025,9,30)
    r.add_event("Mudanza de hija",2024,5,6)
    r.add_event("Nacimiento de hermano",1979,1,30)
    r.add_event("Nacimiento de hermano",1989,3,15)
    r.add_event("Nacimiento de hermana",2000,3,21)
    r.add_event("Primer dia de colegio",1982,2,1)
    """
    r.add_event("Graduación",2007,12,1) #????
    r.add_event("Promoción",2008,5,2) #????
    r.add_event("Divorcio",2014,2,1) #????
    r.add_event("Obtención de residencia",2018,5,1) #????
     #???
    """

    r.add_object(natal_chart_object(natal_chart_object.sun,16,31,20,natal_chart_object.piscis))
    r.add_object(natal_chart_object(natal_chart_object.moon,6,22,7,natal_chart_object.libra))
    r.add_object(natal_chart_object(natal_chart_object.mercury,8,33,44,natal_chart_object.piscis))
    r.add_object(natal_chart_object(natal_chart_object.venus,23,3,3,natal_chart_object.aries))
    r.add_object(natal_chart_object(natal_chart_object.mars,19,57,11,natal_chart_object.aquarius))
    r.add_object(natal_chart_object(natal_chart_object.jupiter,25,13,59,natal_chart_object.taurus))
    r.add_object(natal_chart_object(natal_chart_object.saturn,11,1,11,natal_chart_object.leo))
    r.add_object(natal_chart_object(natal_chart_object.uranus,11,36,2,natal_chart_object.scorpio))
    r.add_object(natal_chart_object(natal_chart_object.neptune,16,6,41,natal_chart_object.sagittarius))
    r.add_object(natal_chart_object(natal_chart_object.pluto,13,31,37,natal_chart_object.libra))
    r.add_object(natal_chart_object(natal_chart_object.mean_node,24,45,10,natal_chart_object.libra))
    r.add_object(natal_chart_object(natal_chart_object.AC,17,0,41,natal_chart_object.sagittarius))
    r.add_object(natal_chart_object(natal_chart_object.II,15,18,54,natal_chart_object.capricorn))
    r.add_object(natal_chart_object(natal_chart_object.III,15,4,12,natal_chart_object.aquarius))
    r.add_object(natal_chart_object(natal_chart_object.IC,16,59,24,natal_chart_object.piscis))
    r.add_object(natal_chart_object(natal_chart_object.XI,19,17,38,natal_chart_object.libra))
    r.add_object(natal_chart_object(natal_chart_object.XII,19,24,22,natal_chart_object.scorpio))

    new_HL = r.calculate()
    logging.info(f'nueva hora local {new_HL}')
    print(f'nueva hora local {new_HL}')
    #assert new_HL == "14hs 40ms 21scs"

if __name__ == "__main__":
    test_rectifier()