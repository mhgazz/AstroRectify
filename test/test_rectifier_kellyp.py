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
    r.set_geograph_long("W",75,35,0)
    r.set_HS_GMT(4.97) #hora de la efemeride del dia 12am convertida a decimales
    r.set_GMT_Hour(-5)
    r.set_radix_bithdate(1994,12,6)
    r.set_radix_MC(119,17,49)
    r.set_orbe_tolerance(0.1)
    r.add_event("Nacimiento de hijo",2023,2,10)
    r.add_event("Comienzo de relación romántica",2020,5,31)
    r.add_event("Comienzo de relación romántica",2011,10,29)
    r.add_event("Comienzo de relación romántica",2019,10,12)
    r.add_event("Rompimiento de relación de amistad",2025,6,8)
    r.add_event("Graduación",2011,11,30)
    r.add_event("Primer empleo profesional",2014,1,14)
    r.add_event("Fallecimiento de mascota",2025,7,14)
    r.add_event("Fallecimiento de tio asesinato intrafamiliar",1990,9,19)
    r.add_event("Fallecimiento de abuela",1992,6,19)
    r.add_event("Fallecimiento de hermano en gestión",1992,6,14)
    r.add_event("Fallecimiento de abuelo",1997,10,3)
    r.add_event("Fallecimiento de tia",2006,2,10)
    r.add_event("Mudanza de hogar",2019,9,9)
    r.add_event("Depresión",2020,1,15)
    r.add_event("Trip de LSD",2020,2,9)
    r.add_event("Iniciación a Shipiden en Reiki",2018,5,27)
    r.add_event("Ruptura de relación romántica",2020,1,3)
    r.add_event("Ruptura de relación romántica",2018,12,29)
    r.add_event("Renuncia",2021,12,31)
    r.add_event("Mudanza de casa con pareja",2021,5,29)
    r.add_event("Viaje",2021,12,19)
    r.add_event("Viaje",2022,2,23)
    r.add_event("Nacimiento de hermano",2003,1,11)
    r.add_event("Viaje a España",2024,12,5)

    r.add_object(natal_chart_object(natal_chart_object.sun,13,58,6,natal_chart_object.sagittarius))
    r.add_object(natal_chart_object(natal_chart_object.moon,0,5,5,natal_chart_object.aquarius))
    r.add_object(natal_chart_object(natal_chart_object.mercury,9,38,42,natal_chart_object.sagittarius))
    r.add_object(natal_chart_object(natal_chart_object.venus,5,25,17,natal_chart_object.scorpio))
    r.add_object(natal_chart_object(natal_chart_object.mars,28,23,58,natal_chart_object.leo))
    r.add_object(natal_chart_object(natal_chart_object.jupiter,29,19,13,natal_chart_object.scorpio))
    r.add_object(natal_chart_object(natal_chart_object.saturn,6,18,37,natal_chart_object.piscis))
    r.add_object(natal_chart_object(natal_chart_object.uranus,24,5,48,natal_chart_object.capricorn))
    r.add_object(natal_chart_object(natal_chart_object.neptune,21,40,27,natal_chart_object.capricorn))
    r.add_object(natal_chart_object(natal_chart_object.pluto,28,35,48,natal_chart_object.scorpio))
    r.add_object(natal_chart_object(natal_chart_object.mean_node,14,28,33,natal_chart_object.scorpio))
    r.add_object(natal_chart_object(natal_chart_object.AC,0,6,48,natal_chart_object.scorpio))
    r.add_object(natal_chart_object(natal_chart_object.II,29,56,45,natal_chart_object.scorpio))
    r.add_object(natal_chart_object(natal_chart_object.III,28,31,23,natal_chart_object.sagittarius))
    r.add_object(natal_chart_object(natal_chart_object.IC,27,14,23,natal_chart_object.capricorn))
    r.add_object(natal_chart_object(natal_chart_object.XI,27,33,46,natal_chart_object.leo))
    r.add_object(natal_chart_object(natal_chart_object.XII,29,15,26,natal_chart_object.virgo))

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