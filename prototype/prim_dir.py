import swisseph as swe
from datetime import datetime, timezone, date, timedelta
from zoneinfo import ZoneInfo
from decimal import Decimal
import math
import roman
from aspects import calculate_aspects
from heat_map import generate_date_heat_map
from utils import get_RA_from_decimal
from utils import get_declination
from utils import get_d_m
from utils import get_d_a
from utils import get_angle_sexag

def get_phi(d_m, s_arc, natal_geo_latitude,cuadrant):
    phi = math.degrees(math.atan(d_m / s_arc * math.tan(math.radians(natal_geo_latitude))))
    return phi

def arc_to_date(arc:float,naibod_key:float,init_date):
    naibod_indx = naibod_key / 365.242197
    #ye = arc / naibod_key
    #dy = ye % 1
    #days = 365 * dy
    #total_days = (365 * int(ye)) + days
    total_days = int(arc / 0.00269861)
    mature_days = init_date + timedelta(days=total_days)
    mature_dt = mature_days.strftime("%Y/%m/%d")
    return mature_dt,total_days

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
aspects = {}

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

# calculo de casa
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
    if h_ind>=1 and h_ind<4:
        ao = ARMC + 90 + ( (h_ind-1) * 30)
        ra_cusp = ra_cusp + 0
    elif h_ind>=4 and h_ind<7:
        ao = ARMC - (30 * (10-h_ind))
        ra_cusp = 180 + ra_cusp
    elif h_ind>=7 and h_ind<10:
        ra_cusp = ra_cusp + 180
        ao = ARMC - (30 * (10-h_ind))
    elif h_ind>=10 and h_ind<13:
        ao = ARMC + 0 + ( (h_ind-10) * 30)
        ra_cusp = 360 + ra_cusp

    if ao>360:
        ao = ao - 360

    d_a_up = ra_cusp - ao
    do = None

    #print(f"{house:<12}   α  {ra_cusp:>3.4f}    λ {eclp_cusp:>3.4f}   AO={ao:>3.4f}")
    speculum[house] = (ra_cusp, None, eclp_cusp, None, None, d_a_up, ao, do,0,0,0,0)

RAIC = speculum["IV"][0]
#generar speculum y aspectos de planetas
for name, id_val in PLANET_IDS.items():
   # returns coordinates, flags, and error messages
    iflag = swe.FLG_SWIEPH | swe.FLG_SPEED | swe.FLG_EQUATORIAL
    coords, flag, _ = swe.calc_ut(jd_tt, id_val, iflag)
    ra = coords[0]
    dec = coords[1]
    coords, flag, _ = swe.calc_ut(jd_tt, id_val)
    eclip_long = coords[0]
    eclip_lat = coords[1]
    cuadrant = get_cuadrant(eclip_long, cusps)

    #speculum
    """
    d_a = math.degrees(math.asin(math.tan(math.radians(dec)) * math.tan(math.radians(natal_geo_latitude))))
    if cuadrant>2:
        s_arc = 90 + d_a
    else:
        s_arc = 90 - d_a
    """
    d_a, s_arc = get_d_a(natal_geo_latitude, dec, cuadrant)
    d_m = get_d_m(ra,ARMC,RAIC,cuadrant)
    #phi = math.degrees( math.atan( d_m/s_arc * math.tan(math.radians(natal_geo_latitude))) )
    phi = get_phi(d_m,s_arc,natal_geo_latitude,cuadrant)
    d_a_up = math.degrees( math.asin(math.tan(math.radians(phi)) * math.tan(math.radians(dec))) )
    AO = 0
    DO = 0
    if cuadrant == 1 or cuadrant ==4:
        AO = ra - d_a_up
    else:
        DO = ra + d_a_up

    # speculum conteniendo
    # 1. Ascencion Recta 2. declinacion 3 y 4. longitud y latitud ecliptica
    # 5. cuadrante
    # 6. diferencia ascencional bajo el polo, 
    # 7. ascencion 8. descencion oblicua

    speculum[name] = (ra, dec, eclip_long, eclip_lat, cuadrant, d_a_up, AO, DO, phi, s_arc, d_m, d_a)
    aspects[name]  = calculate_aspects(eclip_long)

    # direcciones del MC
    conj = ra - ARMC
    ye = abs(conj/naibod_key)
    days = 365 * (ye%1)
    total = (365 * int(ye)) + days
    mature = (date + timedelta(days=total)).strftime("%Y/%m/%d")
    conj, ye, days, mature_dt = calculate_MC_direction(ra, ARMC, naibod_key, date)
    mature = mature_dt.strftime("%Y/%m/%d")
    MC_directions.append(f"{ra:>3.2f}" + " " + f"{conj:>4.2f}" + " " + str(int(ye)) + " years " + str(int(days)) + " days" + " " + str(mature))




print("\n\n")
print(f"--- Direcciones de MC ---")
OBJECT_NAMES = list(PLANET_IDS.keys())
for name, obj_ra in zip(OBJECT_NAMES, MC_directions):
    position_string = f"{name:<8} {obj_ra}"
    print(position_string)

print(f"\n\n--- Speculum (System: {hsys.decode()}) ---")
print("Cuerpo          α       λ       δ      AO.    DO.   DAup     φ    S.A.   D.M.   D.A.   Cuadrante")
for line in speculum:
    ra = speculum[line][0]
    dec = speculum[line][1]
    eclip_long = speculum[line][2]
    eclip_lat = speculum[line][3]
    cuadrant = speculum[line][4]
    d_a_up = speculum[line][5]
    AO = speculum[line][6]
    DO = speculum[line][7]
    phi = speculum[line][8]
    s_arc = speculum[line][9]
    d_m = speculum[line][10]
    d_a = speculum[line][11]
    if DO is None:
        DO = 0
    if AO is None:
        AO = 0
    if dec is None:
        dec = 0
    print(f"{line:<12}   {ra:>6.2f} {eclip_long:>6.2f} {dec:>6.2f} {AO:>6.2f} {DO:>6.2f} {d_a_up:>6.2f} {phi:>6.2f} {s_arc:>6.2f} {d_m:>6.2f} {d_a:>6.2f}    {cuadrant}")



#print("\n\n")
#print(f"--- Direcciones de objetos ---")
directions = {}
ids = {"Sun":1,"Moon":2}
for name in ids: #PLANET_IDS.items():
    signf_ra     = speculum[name][0]
    signf_ao     = speculum[name][6]
    signf_do     = speculum[name][7]
    signf_aupu   = speculum[name][5]
    signf_cudrt  = speculum[name][4]
    signf_phi   = speculum[name][8]

    #print(f"\n\nDirecciones de {name} ----------------------")

    dir_concec=0
    for body,body_aspects in aspects.items():
        body_ra     = speculum[body][0]
        body_adup   = speculum[body][5]
        body_cudrt  = speculum[body][4]
        #print(f"\n{body}    {str(body_aspects)}")
        for cur_aspect,cur_eclep_long in body_aspects.items():
            arc = 0
            cur_ra = get_RA_from_decimal(cur_eclep_long)
            new_dec = get_declination(cur_eclep_long)

            #cambio ---
            #cur_cuadrant = get_cuadrant(cur_eclep_long,cusps)
            #if cur_cuadrant!=body_cudrt:
            #    d_a, s_arc = get_d_a(natal_geo_latitude, new_dec, cur_cuadrant)
            #    d_m = get_d_m(cur_ra, ARMC, RAIC, cur_cuadrant)
            #    signf_phi = math.degrees(math.atan(d_m / s_arc * math.tan(math.radians(natal_geo_latitude))))
            #new_d_a_up = math.degrees(math.asin(math.tan(math.radians(new_phi)) * math.tan(math.radians(new_dec))))
            #----cambio
            new_d_a_up = math.degrees( math.asin(math.tan(math.radians(signf_phi)) * math.tan(math.radians(new_dec))) )
            #--- cambio

            arc = 0
            ao_do_P = 0
            if signf_cudrt==1 or signf_cudrt==4:
                ao_do_P = cur_ra - new_d_a_up
                arc =  ao_do_P - signf_ao
            else:
                ao_do_P = cur_ra + new_d_a_up
                arc = ao_do_P - signf_do
            arc = abs(arc)
            if arc > 360:
                arc = arc - 360

            E_W = "/"
            if arc<=70:
                mature_dt,days_arc=arc_to_date(arc, naibod_key, date)
                #print(f" {body} {cur_aspect} arc {arc} dias {days_arc} fecha {mature_dt} {E_W}")
                #print(f" \tsignificador {name} α {signf_ra} AO:{signf_ao} DO:{signf_do}")
                #print(f" \t    promisor {body} {cur_aspect} --> α {cur_ra} DAup {new_d_a_up} AO/DO {ao_do_P}")
                ao_do = 0
                if signf_ao is not None and signf_ao!=0:
                    signf_cuadrant = get_cuadrant(signf_ao,cusps)
                    ao_do = signf_ao
                else:
                    signf_cuadrant = get_cuadrant(signf_do,cusps)
                    ao_do = signf_do
                ao_do_P_cuadrant=get_cuadrant(ao_do_P,cusps)
                directions[mature_dt+" "+str(dir_concec)] = (cur_aspect, arc,days_arc,name,body,signf_ra,ao_do,cur_ra,new_d_a_up,ao_do_P_cuadrant,signf_cuadrant,ao_do_P)
                dir_concec+=1

sorted_directions = sorted(directions.items())
#print(directions)
sorted_dates=[]
for tt in sorted_directions:
    sorted_dates.append(tt[0])
#results = generate_date_heat_map(sorted_dates,10)
print("Fecha      | Intensidad (Heat)")
print("-" * 28)
#for key, intensity in results:
#α       λ       δ
print("Fecha      Arco        Prm      Aspect             Sig       Prm α   PrmAO/DO   Crd   Sig α   DAφ    SigAO/Do Cdr")
for upla in sorted_directions:
    key=upla[0]
    date_string = str(key).split(" ")[0]
    concec = str(key).split(" ")[1]
    #str_date = date.strftime("%Y/%m/%d")
    #datetime_obj = date.strptime(date_string, "%Y-%m-%d")
    #print(f"{date} | {'*' * intensity} ({intensity})  {directions[key][0]} {directions[key][1]} {directions[key][2]} {directions[key][3]} --> {directions[key][4]}")
    g, m, s = get_angle_sexag(float(directions[key][1]))
    arc_sexag = str(g) + "º" + str(m) + "," + str(s) + "'"
    print(f"{date_string} {arc_sexag:10}  {directions[key][3]:8} {directions[key][0]:18} {directions[key][4]:8}  {round(float(directions[key][5]),3):<6.3f} {round(float(directions[key][6]),3):<6.3f}    {directions[key][10]:1}     {round(float(directions[key][7]),3):<6.3f} {round(float(directions[key][8]),2):<6.3f} {round(float(directions[key][11]),2):<6.3f}  {directions[key][9]:1}")
    #print(f"{date_string},{arc_sexag:10},{directions[key][3]:8},{directions[key][0]:18},{directions[key][4]:8},{round(float(directions[key][5]), 3):<6.3f},{round(float(directions[key][6]), 3):<6.3f},{directions[key][10]:1},{round(float(directions[key][7]), 3):<6.3f},{round(float(directions[key][8]), 2):<6.3f},{round(float(directions[key][11]), 2):<6.3f},{directions[key][9]:1}")
    #{ra:>6.2f}

"""                                                                                                        #signf_ra,ao_do,cur_ra,new_d_a_up,ao_do_P
(cur_aspect,
 arc,days_arc,
 name,
 body,
 signf_ra,
 ao_do,
 cur_ra,
 new_d_a_up,
 ao_do_P,
 signf_cuadrant)



mars_aupu = speculum["Mars"][5]
mars_ao   = speculum["Mars"][6]
mars_do   = speculum["Mars"][6]
mars_ra   = speculum["Mars"][0]

sun_ra   = speculum["Sun"][0]
marcury_ra   = speculum["Mercury"][0]
mercury_aupu = speculum["Mercury"][5]
venus_ra   = speculum["Venus"][0]
neptune_ra   = speculum["Neptune"][0]
ASC_ao = speculum["I"][6]
ASC_aupu = speculum["I"][5]
moon_ra = speculum["Moon"][0]
jupiter_ra = speculum["Jupiter"][0]

dirarc_sun = sun_ra - mars_do + mars_aupu
dirarc_marcury = marcury_ra - mars_do + mars_aupu
dirarc_mercury_smsextil = abs(marcury_ra + 30 - mars_do + mars_aupu)
convarc_mercury_smsextil = abs(marcury_ra - 30 - mars_do + mars_aupu)
dirarc_venus = venus_ra - mars_do + mars_aupu
convarc_neptune = mars_do - neptune_ra - mars_aupu
convarc_asc_moon = abs(360 - (moon_ra - ASC_ao - ASC_aupu))
convarc_asc_moon_semsextil = abs(360 - (moon_ra + 30 - ASC_ao - ASC_aupu))
dirarc_asc_moon_sextil = abs(moon_ra + 60 - 360 - ASC_ao - ASC_aupu)
dirarc_asc_moon_sqr = abs(moon_ra + 90 - 360 - ASC_ao - ASC_aupu)
dirarc_asc_jupiter = abs(jupiter_ra - ASC_ao - ASC_aupu)

jupiter_smsextil_dir = aspects["Jupiter"]["semisextil+"]
jupiter_smsextil_conv = aspects["Jupiter"]["semisextil-"]
dirarc_asc_jupiter_semsextil_a = abs(jupiter_smsextil_dir - ASC_ao - ASC_aupu)
convarc_asc_jupiter_semsextil_a = abs(jupiter_smsextil_conv - ASC_ao - ASC_aupu)

print("\n\nMarte----------")
print(f"     sol: conj {dirarc_sun} {arc_to_date(dirarc_sun,naibod_key,date)}")
print(f"mercurio: conj {dirarc_marcury} {arc_to_date(dirarc_marcury,naibod_key,date)}")
print(f"mercurio: smsextil dir {dirarc_mercury_smsextil} {arc_to_date(dirarc_mercury_smsextil,naibod_key,date)}")
print(f"mercurio: smsextil conv {convarc_mercury_smsextil} {arc_to_date(convarc_mercury_smsextil,naibod_key,date)}")
print(f"   venus: conj {dirarc_venus} {arc_to_date(dirarc_venus,naibod_key,date)}")
print(f" neptune: conj {convarc_neptune} {arc_to_date(convarc_neptune,naibod_key,date)}")

print(f" ASC -> CONJ moon conv: {convarc_asc_moon} {arc_to_date(convarc_asc_moon,naibod_key,date)}")
print(f" ASC -> SMSEX moon conv: {convarc_asc_moon_semsextil} {arc_to_date(convarc_asc_moon_semsextil,naibod_key,date)}")
print(f" ASC -> SEX moon dir: {dirarc_asc_moon_sextil} {arc_to_date(dirarc_asc_moon_sextil,naibod_key,date)}")
print(f" ASC -> SQR moon dir: {dirarc_asc_moon_sqr} {arc_to_date(dirarc_asc_moon_sqr,naibod_key,date)}")
print(f" ASC -> CONJ jupiter dir: {dirarc_asc_jupiter} {arc_to_date(dirarc_asc_jupiter,naibod_key,date)}")
print(f" ASC -> SMSEX jupiter dir: {dirarc_asc_jupiter_semsextil_a} {arc_to_date(dirarc_asc_jupiter_semsextil_a,naibod_key,date)}")
print(f" ASC -> SMSEX jupiter conv: {convarc_asc_jupiter_semsextil_a} {arc_to_date(convarc_asc_jupiter_semsextil_a,naibod_key,date)}")
"""