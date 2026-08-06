import swisseph as swe
from datetime import datetime, timezone, date, timedelta
from zoneinfo import ZoneInfo
from decimal import Decimal
import math
import roman
import sys
from aspects import calculate_aspects
from heat_map import generate_date_heat_map
from utils import get_RA_from_decimal
from utils import get_declination
from utils import get_d_m
from utils import get_d_a
from utils import get_angle_sexag
from utils import get_cuadrant
from utils import get_PMP
from utils import get_placidus_mund_pos
from utils import get_placidus_ratio
from utils import calcular_arco_placidus
from utils import normalize_angle
from utils import get_placidus_pole
from utils import arc_to_date


def get_phi(d_m, s_arc, natal_geo_latitude,cuadrant):
    phi = math.degrees(math.atan(d_m / s_arc * math.tan(math.radians(natal_geo_latitude))))
    return phi



def calculate_MC_direction(ra, ARMC, naibod_key, start_date):
    conj = ra - ARMC
    ye = abs(conj / naibod_key)
    days = 365 * (ye % 1)
    total_days = (365 * int(ye)) + days
    mature_date = start_date + timedelta(days=total_days)
    return conj, ye, days, mature_date

print("Astrorectify v0.1 Primary Direcciones calcularion")

try:
    if len(sys.argv) != 3:
        hdsystem = sys.argv[1].split(":")[1]
        promitor = sys.argv[2].split(":")[1].split(",")
        significator = sys.argv[3].split(":")[1].split(",")
    else:
        raise KeyError
except KeyError:
    print("\nUsage:\n------------\n\npython3 prim_dir.py System:param1 Promitor:param2 Significator:param3")
    print("Param1: Primary Directions sysmtem possible values")
    print("\n- Topocentric\n- Placidus-SA\n- Placidus-UP\n- Regiomentano")
    print("\nParam2: possible values * all, ASC, MC, Sun, Moon, Mercury, Venus, Mars, Jupiter, Saturn, Uranus, Neptune, Pluto")
    print("\nParam3: possible values * all, ASC, MC, Sun, Moon, Mercury, Venus, Mars, Jupiter, Saturn, Uranus, Neptune, Pluto")
    print("\n------------")
    sys.exit()

#MC_directions = []
speculum = {}
aspects = {}
aspects_MC = {}  # aspectos de cuerpos solo para dirigir el MC

#native data
natal_geo_latitude = -32.95
natal_geo_longitude = -60.6667
date = datetime(1976, 12, 26, 17, 40, 00, tzinfo=timezone.utc)

# system parameters #######
naibod_key = 0.9856472  # naibod key
oblicuity = 23.44       # ecliptic declination 
max_age = 360           # max arc distance

# domification system #
if hdsystem=="Topocentric":
    hsys = b"T"
elif hdsystem=="Placidus-SA":
    hsys = b"P"
elif hdsystem=="Placidus-UP":
    hsys = b"P"
elif hdsystem=="Regiomentano":
    hsys = b"R"
###########################

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
print(f"\n\n --- Parámetros: ")
print(f"Domificación (System: {hsys.decode()}) --- {hdsystem}")
print(f"Clave: Naibod {naibod_key }---")
print(f"Oblicuidad: {oblicuity}")
print(f"Arco maximo: {max_age}")
print(f"\n---Datos del nativo")
print(f"Latitud {natal_geo_latitude} Longitud {natal_geo_longitude}")
print(f"Fecha y hora universal: {date}")

cusps, ascmc = swe.houses(jd_ut, natal_geo_latitude, natal_geo_longitude, hsys)
angles = [ascmc[0], ascmc[1], ascmc[2]]
print(f"Ascendant: {angles[0]}")
print(f"Midheaven: {angles[1]}")
print(f"ARMC: {angles[2]}")
ARMC = angles[2]
ASC = angles[0]
MC = angles[1]
ASC_OA = ARMC + 90
if ASC_OA > 360:
    ASC_OA = ASC_OA - 360
RAIC = ARMC - 180
if RAIC < 0:
    RAIC = 360 - RAIC
print(f"RAIC: {RAIC}")

""" ####
Speculum array:
 1- RA
 2- Declination
 3- Ecliptic long
 4- None
 5- Cuadrante,
 6- Diferencia ascencional bajo polo
 7- Asc oblicua
 8- Descencion oblicua
 9- Polo
10- Semiarco
11- Distancia al meridiano
12- Diferencia ascencional
13- Placidus mundanal position PMP
"""

# speculum de casa y angulos
h_ind:int=0
for h in cusps[0:13]:
    h_ind = h_ind + 1
    eclp_cusp = h
    house = roman.toRoman(h_ind)
    ao = 0
    d_a_up = 0
    ra_cusp = math.degrees(math.atan(math.tan(math.radians(eclp_cusp)) * math.cos(math.radians(oblicuity))))
    #print(h_ind-1,h,ra_cusp)
    if h_ind>=1 and h_ind<4:
        ao = ARMC + 90 + ( (h_ind-1) * 30)
        ra_cusp = ra_cusp + 0
    elif h_ind>=4 and h_ind<7:
        ao = ARMC - (30 * (10-h_ind))
        ra_cusp = 180 + ra_cusp
    elif h_ind>=7 and h_ind<10:
        ra_cusp = ra_cusp + 180
        ao = ARMC - (30 * (10-h_ind))
    elif h_ind>=10 and h_ind<12:
        ao = ARMC + 0 + ( (h_ind-10) * 30)
        ra_cusp = 360 + ra_cusp

    if ao>360:
        ao = ao - 360

    d_a_up = ra_cusp - ao
    do = None
    cuadrant=None
    phi = 0
    decl = get_declination(ra_cusp)
    cuadrant = get_cuadrant(eclp_cusp,cusps)
    if h_ind==1:
        house="ASC"
        cuadrant=1
        phi = natal_geo_latitude
    if h_ind==10:
        house="MC"
        cuadrant=4

    d_a, s_arc = get_d_a(natal_geo_latitude, decl, cuadrant)
    d_m = get_d_m(ra_cusp,ARMC,RAIC,cuadrant)

    pmp = 0
    if hsys.decode()=='R':
        pmp = get_PMP(d_a, natal_geo_latitude, decl, cuadrant, ARMC, RAIC, ra_cusp)
    elif hsys.decode()=='P':
        pmp = get_placidus_mund_pos(d_m,s_arc,cuadrant,ARMC)

    speculum[house] = (ra_cusp, decl, eclp_cusp, None, cuadrant, d_a_up, ao, do,phi,s_arc,d_m,d_a,pmp)

    # aspectos de las cuspides
    if h_ind in (10,11,12,1,2,3):
        if hsys.decode()=='P':
            aspects[house]  = calculate_aspects(pmp)
        elif hsys.decode()=='T':
            aspects[house]  = calculate_aspects(eclp_cusp)
        # aspectos para MC independiente del sistema
        aspects_MC[house]  = calculate_aspects(ra_cusp)




#generar speculum y aspectos de planetas
for name, id_val in PLANET_IDS.items():
   # returns coordinates, flags, and error messages
    iflag = swe.FLG_SWIEPH | swe.FLG_SPEED | swe.FLG_EQUATORIAL
    if hsys.decode()=="T":
        # geo coordenadas para calculo topocentrico
        swe.set_topo(natal_geo_latitude,natal_geo_longitude)
    coords, flag = swe.calc_ut(jd_tt, id_val, iflag)
    ra = coords[0]
    dec = coords[1]
    coords, flag = swe.calc_ut(jd_tt, id_val)
    eclip_long = coords[0]
    eclip_lat = coords[1]
    cuadrant = get_cuadrant(eclip_long, cusps)

    #speculum
    d_a, s_arc = get_d_a(natal_geo_latitude, dec, cuadrant)
    d_m = get_d_m(ra,ARMC,RAIC,cuadrant)
    phi = 0
    if hsys.decode()=="P" and hdsystem=="Placidus-UP":
        phi = get_placidus_pole(d_m,s_arc,cuadrant,dec,d_a)
    elif hsys.decode()=="T":
        phi = get_phi(d_m,s_arc,natal_geo_latitude,cuadrant)

    d_a_up = math.degrees( math.asin(math.tan(math.radians(phi)) * math.tan(math.radians(dec))) )
    
    pmp = 0
    if hsys.decode()=='R':
        pmp = get_PMP(d_a, natal_geo_latitude, dec, cuadrant, ARMC, RAIC, ra)
    elif hsys.decode()=='P':
        pmp = get_placidus_mund_pos(d_m,s_arc,cuadrant,ARMC)
    
    AO = 0
    DO = 0
    if cuadrant == 1 or cuadrant ==4:
        AO = ra - d_a_up
    else:
        DO = ra + d_a_up

    speculum[name] = (ra, dec, eclip_long, eclip_lat, cuadrant, d_a_up, AO, DO, phi, s_arc, d_m, d_a, pmp)

    # calculo de aspectos por cada cuerpo
    # sistema placidus con RA | sistema topocentrico con longitud ecliptica
    if hsys.decode()=='T':
        aspects[name]  = calculate_aspects(eclip_long)
    elif hsys.decode()=='P':
        aspects[name] = calculate_aspects(pmp)
    # aspecto de RA independiente de sistema para dirigir MC
    aspects_MC[name]  = calculate_aspects(eclip_long)



print(f"\n\n--- Speculum (System: {hsys.decode()}) ---")
print("Cuerpo          α       λ       δ      AO.    DO.   DAup     φ    S.A.   D.M.   D.A.  PMP  Qd")
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
    pmp = speculum[line][12]
    if DO is None:
        DO = 0
    if AO is None:
        AO = 0
    if dec is None:
        dec = 0
    print(f"{line:<12}   {ra:>6.2f} {eclip_long:>6.2f} {dec:>6.2f} {AO:>6.2f} {DO:>6.2f} {d_a_up:>6.2f} {phi:>6.2f} {s_arc:>6.2f} {d_m:>6.2f} {d_a:>6.2f} {pmp:>6.2f} {cuadrant}")



directions = {}
#sys.exit(0)
header="/"

# calcular direcciones de planetas y ASC
dir_concec = 0
# promitor
ids = {"MC":1,"ASC":2}
for name in PLANET_IDS.keys() | ids.keys():
    if name not in promitor:
        continue
    signf_ra    = speculum[name][0]
    decl_p      = speculum[name][1]
    signf_ao    = speculum[name][6]
    signf_do    = speculum[name][7]
    signf_aupu  = speculum[name][5]
    signf_cudrt = speculum[name][4]
    signf_phi   = speculum[name][8]
    ad_p        = speculum[name][11]
    #print(f"\n\n --- promitor {name} RA {signf_ra} declination {decl_p} --------")

    if name == "MC":
        aspects_s = aspects_MC
    else:
        aspects_s = aspects

    #significator
    for body,body_aspects in aspects_s.items():
        if body not in significator:
            continue
        #print(body + " " + str(body_aspects))
        body_ra     = speculum[body][0]
        body_adup   = speculum[body][5]
        body_cudrt  = speculum[body][4]
        body_decl   = speculum[body][1]
        sa_s        = speculum[body][9]
        md_s        = speculum[body][10]

        #print(f"\n --- significador {body} aspectos en RA {str(body_aspects)}")
        for cur_aspect,cur_eclep_long in body_aspects.items():
            arc = 0
            diff = 0

            if body==name and cur_aspect=="conjuncion":
                continue


            if hsys.decode()=="T":
                # calculo topocentrico de arco de dirección sobre ecliptica

                if name=="MC":
                    # calculo de arco para MC como promitor y cuerpo como significador
                    cuadrante_s = body_cudrt
                    cur_ra = get_RA_from_decimal(cur_eclep_long)
                    if cur_aspect=="conjuncion":
                        cur_ra = body_ra
                    #cur_ra = 275.554
                    #ARMC = 299.6772
                    arc = cur_ra - ARMC
                    arc = abs(arc)
                    ao_do_P = cur_ra
                    new_d_a_up = 0 
                else:
                    # calculo para interplanetarias y ASC              
                    cur_ra = get_RA_from_decimal(cur_eclep_long)
                    ao_do_P = 0
                    new_d_a_up = 0
                    new_dec = get_declination(cur_eclep_long)
                    new_d_a_up = math.degrees( math.asin(math.tan(math.radians(signf_phi)) * math.tan(math.radians(new_dec))) )
                    arc = 0
                    ao_do_P = 0
                    if signf_cudrt==1 or signf_cudrt==4:
                        ao_do_P = cur_ra - new_d_a_up
                        arc =  ao_do_P - signf_ao
                    else:
                        ao_do_P = cur_ra + new_d_a_up
                        arc = ao_do_P - signf_do

            elif hsys.decode()=="P" and hdsystem=="Placidus-UP":
                # calculo topocentrico de arco de dirección sobre ecliptica
                if name=="MC":
                    cur_ra = ARMC
                else:
                    cur_ra = get_RA_from_decimal(cur_eclep_long)
                ao_do_P = 0
                new_d_a_up = 0
                new_dec = get_declination(cur_eclep_long)
                new_d_a_up = math.degrees( math.asin(math.tan(math.radians(signf_phi)) * math.tan(math.radians(new_dec))) )
                arc = 0
                ao_do_P = 0
                cuadrante_s = signf_cudrt
                if signf_cudrt==1 or signf_cudrt==4:
                    ao_do_P = cur_ra - new_d_a_up
                    arc =  ao_do_P - signf_ao
                else:
                    ao_do_P = cur_ra + new_d_a_up
                    arc = ao_do_P - signf_do

            elif hsys.decode()=="P" and hdsystem=="Placidus-SA":
                # calculo metodo Placidus por semiarco mundano de arco de dirección
                cur_ra = body_ra
                cuadrante_s = body_cudrt
                ra_p = signf_ra
                pmp = cur_eclep_long
                pmp = normalize_angle(pmp)
                if name=="MC":
                    if cur_aspect=="conjuncion":
                        cur_ra = body_ra
                    else:
                        cur_ra = get_RA_from_decimal(cur_eclep_long)
                    #cur_ra = 275.554
                    #ARMC = 299.6772
                    arc = cur_ra - ARMC
                    arc = abs(arc)
                else:                
                    ratio,cuadrante_s = get_placidus_ratio(pmp)
                    arc,diff = calcular_arco_placidus(
                        ra_p=ra_p,
                        ad_p=ad_p,
                        ratio=ratio,
                        cuadrante_s=cuadrante_s,
                        RAMC=ARMC,
                        RAIC=RAIC)

            if hsys.decode()=="R":
                # calculo metodo Regiomentano generico arco de dirección
                # TODO revisar con libro de Makrasky e implementar
                cur_ra = body_ra
                ra_ap = cur_eclep_long
                decl_s = body_decl
                ao_do_P = cur_ra
                ra_p = signf_ra
                new_d_a_up = 0
                cuadrt_s = get_cuadrant(cur_ra, cusps)
                ad_s, sa_s = get_d_a(natal_geo_latitude, decl_s, cuadrt_s)
                pmp_pa = get_PMP(ad_s, natal_geo_latitude, decl_s, cuadrt_s, ARMC, RAIC, ra_ap)
                #print(f"-- {body} aspect {cur_aspect} RA ap {ra_ap} PMP ap {pmp_pa} cuadrante signf ap {cuadrt_s}")
                # resultado_arco = calcular_arco_placidus(ra_p=ra_p,ad_p=ad_p,ratio=ratio,cuadrante_s=cuadrante_s,RAMC=RAMC,RAIC=RAIC)
                tan_decl = math.tan(math.radians(decl_p))
                tan_phi = math.tan(math.radians(natal_geo_latitude))
                cos_ca = math.cos(math.radians(ASC_OA - pmp_pa))
                a_diff = tan_decl * tan_phi * cos_ca
                #print(f"tan_decl {tan_decl} tan_phi {tan_phi} cos_ca {cos_ca} total {a_diff}")
                diff = math.degrees(math.asin(a_diff))
                arc = ra_p - diff - pmp_pa
                #print(f"ASC AO {ASC_OA} Promittor RA {ra_p} arco {arc:.2f}")

            if arc<0:
                cur_aspect = cur_aspect + " C"
            arc = abs(arc)
            if arc > 360:
                arc = arc - 360

            E_W = "/"
            if arc<=max_age:
                mature_dt,days_arc=arc_to_date(arc, naibod_key, date)
                ao_do = 0

                if hsys.decode() == "T":
                    if signf_ao is not None and signf_ao!=0:
                        signf_cuadrant = get_cuadrant(signf_ao,cusps)
                        ao_do = signf_ao
                    else:
                        signf_cuadrant = get_cuadrant(signf_do,cusps)
                        ao_do = signf_do
                    ao_do_P_cuadrant=get_cuadrant(ao_do_P,cusps)
                    directions[mature_dt+" "+str(dir_concec)] = (cur_aspect, arc,days_arc,name,body,signf_ra,ao_do,cur_ra,new_d_a_up,ao_do_P_cuadrant,signf_cuadrant,ao_do_P)
                    header = "Fecha      Arco        Prm      Aspect             Sig       Prm α   PrmAO/DO   Crd    Sig α   DAφ    SigAO/Do Cdr"
                elif hsys.decode() == "P":
                    directions[mature_dt+" "+str(dir_concec)] = (cur_aspect,arc,days_arc,name,body,signf_ra,ao_do,cur_ra,diff,cuadrante_s,signf_cudrt,pmp)
                    header = "Fecha      Arco        Prm      Aspect             Sig       Prm α   PrmAO/DO  Crd_p  Sig α   Dif     PMPap   Cdr_s"
                elif hsys.decode() == "R":
                    pass
                else:
                    pass
                dir_concec+=1

sorted_directions = sorted(directions.items())
#print(directions)
sorted_dates=[]
for tt in sorted_directions:
    sorted_dates.append(tt[0])
#results = generate_date_heat_map(sorted_dates,10)
print("\n\nDirecciones primarias")
print("-" * 28)

# header
print(header)
dates_for_map = []
for upla in sorted_directions:
    key=upla[0]
    dates_for_map.append(key)
    date_string = str(key).split(" ")[0]
    concec = str(key).split(" ")[1]
    cur_arc = directions[key][1]
    g, m, s = get_angle_sexag(float(cur_arc))
    arc_sexag = str(g) + "º" + str(m) + "," + str(s) + "'"
    print(f"{date_string} {arc_sexag:10}  {directions[key][3]:8} {directions[key][0]:18} {directions[key][4]:8}  {str(round(float(directions[key][5]),3)):6}  {str(round(float(directions[key][6]),3)):6}    {directions[key][10]:1}      {round(float(directions[key][7]),3):6.3f} {round(float(directions[key][8]),2):6.3f} {round(float(directions[key][11]),2):6.3f}  {directions[key][9]:1}")

hm = generate_date_heat_map(dates_for_map,5)
print("\n\nFecha      | Intensidad (Heat)")
print("-" * 30)
for date, intensity in hm:
    if intensity>2:
        print(f"{date} | {'*' * intensity} ({intensity})")

