import swisseph as swe
from datetime import datetime, timezone, date, timedelta
from zoneinfo import ZoneInfo
from decimal import Decimal
import math
import roman

def arc_to_date(arc:float,naibod_key:float,init_date):
    naibod_indx = naibod_key / 365.24224
    #ye = arc / naibod_key
    #dy = ye % 1
    #days = 365 * dy
    #total_days = (365 * int(ye)) + days
    total_days = int(arc / naibod_indx)
    mature_days = init_date + timedelta(days=total_days)
    mature_dt = mature_days.strftime("%d/%m/%Y")
    return mature_dt

def calculate_MC_direction(ra, ARMC, naibod_key, start_date):
    conj = ra - ARMC
    ye = abs(conj / naibod_key)
    days = 365 * (ye % 1)
    total_days = (365 * int(ye)) + days
    mature_date = start_date + timedelta(days=total_days)
    return conj, ye, days, mature_date

def is_between(target, start, end):
    if start < end:
        return start <= target < end
    else:  # Spans across 0°
        return target >= start or target < end

def get_cuadrant(eclip_long, cusps):
    """
    Determines the quadrant of a planet based on house cusps.
    1: Asc to IC, 2: IC to Dsc, 3: Dsc to MC, 4: MC to Asc
    """
    # cusps[1]=Asc, [4]=IC, [7]=Dsc, [10]=MC
    asc = cusps[1]
    ic = cusps[4]
    dsc = cusps[7]
    mc = cusps[10]

    if is_between(eclip_long, asc, ic):
        return 1
    elif is_between(eclip_long, ic, dsc):
        return 2
    elif is_between(eclip_long, dsc, mc):
        return 3
    else:
        return 4
        (eclip_long,cusps)


MC_directions = []
speculum = {}

natal_geo_latitude = -32.95
natal_geo_longitude = -60.6394
#ng = -60.6394
hsys = b"T"
date = datetime(1976, 12, 26, 17, 39, 42, tzinfo=timezone.utc)
#date = datetime(1976, 12, 26, 17, 40, 00, tzinfo=timezone.utc)

naibod_key = 0.9856472
oblicuity = 23.44

jd_ut, jd_tt = swe.utc_to_jd(
    date.year, date.month, date.day, date.hour, date.minute, date.second
)


PLANET_IDS = {
    "Sun": swe.SUN,
    "Moon": swe.MOON,
    "Mercury": swe.MERCURY,
    "Venus": swe.VENUS,
    "Mars": swe.MARS,
    "Jupiter": swe.JUPITER,
    "Saturn": swe.SATURN,
    "Uranus": swe.URANUS,
    "Neptune": swe.NEPTUNE,
    "Pluto": swe.PLUTO,
}

print(f"\n\n--- Domificación (System: {hsys.decode()}) ---")
cusps, ascmc = swe.houses(jd_ut, natal_geo_latitude, natal_geo_longitude, hsys)
angles = [ascmc[0], ascmc[1], ascmc[2]]
print(f"Ascendant: {angles[0]}")
print(f"Midheaven: {angles[1]}")
print(f"ARMC: {angles[2]}")
ARMC = angles[2]
ASC = angles[0]
MC = angles[1]
print("\n")

h_ind:int=0
for h in cusps[1:13]:
    h_ind = h_ind + 1
    eclp_cusp = h
    house = roman.toRoman(h_ind)
    ao = 0
    d_a_up = 0
    ra_cusp = math.degrees(math.atan(math.tan(math.radians(eclp_cusp)) * math.cos(math.radians(oblicuity))))
    if h_ind>=1 and h_ind<=10:
        ao = ARMC + 90 + ( (h_ind-1) * 30)
        ra_cusp = ra_cusp + 0
    elif h_ind>=4 and h_ind<7:
        ao = ARMC - 180 + (30 * h_ind -3)
        ra_cusp = 180 + ra_cusp
    elif h_ind>=7 and h_ind<10:
        ra_cusp = ra_cusp + 180
    elif h_ind>=10 and h_ind<13:
        ao = ARMC + 0 + ( (h_ind-10) * 30)

    if ao>360:
        ao = ao - 360

    #print(f"{house:<12}   α  {ra_cusp:>3.4f}    λ {eclp_cusp:>3.4f}   AO={ao:>3.4f}")
    speculum[house] = (ra_cusp, None, eclp_cusp, None, None, d_a_up, ao, None)


print(f"\n\n--- Speculum (System: {hsys.decode()}) ---")
print("Cuerpo         α      λ      AO.    DO.     DAup    phi   S.A.   D.M.   D.A.   Cuadrante")
for name, id_val in PLANET_IDS.items():
   # returns coordinates, flags, and error messages
    coords, flag, _ = swe.calc_ut(jd_tt, id_val, swe.FLG_EQUATORIAL)
    ra = coords[0]
    dec = coords[1]
    coords, flag, _ = swe.calc_ut(jd_tt, id_val)
    eclip_long = coords[0]
    eclip_lat = coords[1]
    cuadrant = get_cuadrant(eclip_long, cusps)

    #speculum
    d_a = math.degrees(math.asin(math.tan(math.radians(dec)) * math.tan(math.radians(natal_geo_latitude))))
    if cuadrant>2:
        s_arc = 90 + d_a
    else:
        s_arc = 90 - d_a
    
    if cuadrant==3 and cuadrant==1:
        d_m = ARMC - ra
    else:
        d_m = ra - ARMC
    
    phi = math.degrees( math.atan( d_m/s_arc * math.tan(math.radians(natal_geo_latitude))) )
    d_a_up = math.degrees( math.asin(math.tan(math.radians(phi)) * math.tan(math.radians(dec))) )
    AO = ra + d_a_up
    DO = ra - d_a_up
    #print(f"{name:<12}   {ra:>6.2f} {eclip_long:>6.2f} {AO:>6.2f} {DO:>6.2f} {d_a_up:>6.2f} {phi:>6.2f} {s_arc:>6.2f} {d_m:>6.2f} {d_a:>6.2f}    {str(cuadrant):<2}")

    #topocentric
    #TODO si la longitud ecliptica topocentrica es diferente debo usarla para calcular la dirección
    #swe_set_topo(geo_lon, geo_lat, altitude_above_sea)
    #swe.set_topo(natal_geo_longitude, natal_geo_latitude, 0)
    #swe.SEFLG_TOPOCTR = 1
    #iflag |= SEFLG_TOPOCTR;
    #iflgret = swe_calc(tjd, ipl, iflag, xp, serr);
    #coords, flag, _ = swe.calc_ut(jd_tt, id_val, swe.FLG_TOPOCTR)
    #coords, flag, _ = swe.calc_ut(jd_tt, id_val)
    #topo_eclip_long = coords[0]
    #topo_eclip_lat = coords[1]
    #topo_cuadrant = get_cuadrant(topo_eclip_long, cusps)
    #cos_oblicuity = math.cos(math.radians(oblicuity))
    #sen_oblicuity = math.sin(math.radians(oblicuity))
    #cos_topo_eclip_long = math.cos(math.radians(topo_eclip_long))
    #sen_topo_eclip_long = math.sin(math.radians(topo_eclip_long))
    #cos_topo_eclip_lat = math.cos(math.radians(eclip_lat))
    #cos_dec = math.cos(math.radians(dec))
    #ra_t = math.degrees( math.acos(cos_topo_eclip_long * cos_topo_eclip_lat / cos_dec))



    
    



    # speculum conteniendo
    # 1. Ascencion Recta 2. declinacion 3 y 4. longitud y latitud ecliptica
    # 5. cuadrante
    # 6. diferencia ascencional bajo el polo, 
    # 7. ascencion 8. descencion oblicua

    speculum[name] = (ra, dec, eclip_long, eclip_lat, cuadrant, d_a_up, AO, DO)

    # direcciones del MC
    conj = ra - ARMC
    ye = abs(conj/naibod_key)
    days = 365 * (ye%1)
    total = (365 * int(ye)) + days
    mature = (date + timedelta(days=total)).strftime("%Y/%m/%d")
    conj, ye, days, mature_dt = calculate_MC_direction(ra, ARMC, naibod_key, date)
    mature = mature_dt.strftime("%Y/%m/%d")
    MC_directions.append(f"{ra:>3.2f}" + " " + f"{conj:>4.2f}" + " " + str(int(ye)) + " years " + str(int(days)) + " days" + " " + str(mature))



"""
print("\n\n")
print(f"--- Direcciones de MC ---")
OBJECT_NAMES = list(PLANET_IDS.keys())
for name, obj_ra in zip(OBJECT_NAMES, MC_directions):
    position_string = f"{name:<8} {obj_ra}"
    print(position_string)
"""

for line in speculum:
    ra = speculum[line][0]
    dec = speculum[line][1]
    eclip_long = speculum[line][2]
    eclip_lat = speculum[line][3]
    cuadrant = speculum[line][4]
    d_a_up = speculum[line][5]
    AO = speculum[line][6]
    DO = speculum[line][7]
    phi=0
    s_arc=0
    d_m=0
    d_a=0
    if DO is None:
        DO = 0
    if AO is None:
        AO = 0


    print(f"{line:<12}   {ra:>6.2f} {eclip_long:>6.2f} {AO:>6.2f} {DO:>6.2f} {d_a_up:>6.2f} {phi:>6.2f} {s_arc:>6.2f} {d_m:>6.2f} {d_a:>6.2f}    {cuadrant}")



print("\n\n")
print(f"--- Direcciones de objetos ---")
mars_aupu = speculum["Mars"][5]
mars_ao   = speculum["Mars"][6]
mars_do   = speculum["Mars"][6]
sun_ra   = speculum["Sun"][0]
marcury_ra   = speculum["Mercury"][0]
mercury_aupu = speculum["Mercury"][5]
venus_ra   = speculum["Venus"][0]
neptune_ra   = speculum["Neptune"][0]

dirarc_sun = sun_ra - mars_do + mars_aupu
dirarc_marcury = marcury_ra - mars_do + mars_aupu
dirarc_venus = venus_ra - mars_do + mars_aupu
convarc_neptune = mars_do - neptune_ra - mars_aupu

print(f"     sol: {dirarc_sun} {arc_to_date(dirarc_sun,naibod_key,date)}")
print(f"mercurio: {dirarc_marcury} {arc_to_date(dirarc_marcury,naibod_key,date)}")
print(f"   venus: {dirarc_venus} {arc_to_date(dirarc_venus,naibod_key,date)}")
print(f" neptune: {convarc_neptune} {arc_to_date(convarc_neptune,naibod_key,date)}")


