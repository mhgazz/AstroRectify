# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.

from datetime import date, timedelta
import math


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press ⌘F8 to toggle the breakpoint.

def dateptrdiffs(ya, ma, da, yb, mb, db):
    """ get delta dates in days"""
    date_a=date(ya,ma,da)
    date_b=date(yb,mb,db)
    delta = date_b-date_a
    return int(delta.days)

def get_direction_arc(days:int):
    """get direction arc using Naibod key 59º08'33' """
    naibod_key: float = 0.00269861
    return naibod_key*days

def convert_angle_decimal(grade:int,mins:int,secs:int):
    """ convert angle in decimal degrees """
    decimal = grade + mins/60 + secs/3600
    return decimal

def get_RAMC(grade:int,mins:int,secs:int):
    """ provide Right Ascention for Mideum Coeli with standard declination value 23.44"""
    declination: float = 23.44
    dec_angle = convert_angle_decimal(grade,mins,secs)
    radian_angle = math.radians(dec_angle)
    tan_long = math.tan(radian_angle)
    cos_dec = math.cos(math.radians(declination))
    ramc_rad = math.atan(tan_long*cos_dec)
    RAMC = math.degrees(ramc_rad)
    if (RAMC<0):
        if grade >270:
            RAMC = RAMC + 360
        elif grade >180:
            RAMC = RAMC + 270
    else:
        if grade >180:
            RAMC = 180 + RAMC
    return RAMC

def get_ecliptic_longitude(ar:float):
    """ convert a AR value to ecliptic longitude"""
    declination: float = 23.44
    tang_ar = math.tan(math.radians(ar))
    dec_cos = math.cos(math.radians(declination))
    tmp = tang_ar/dec_cos
    ecliptic_longitude = math.degrees(math.atan(tmp))
    if ar >270:
        ecliptic_longitude = ecliptic_longitude + 360
    elif ar >180:
        ecliptic_longitude = ecliptic_longitude + 180
    return ecliptic_longitude


# Press the green button in the     gutter to run the script.
def identify_aspect(diff:float):

    matches = []
    a_90 = abs(90 - diff)
    a_180 = abs(180 - diff)
    a_120 = abs(120 - diff)
    a_150 = abs(150 - diff)
    a_60 = abs(60 - diff)
    a_0 = abs(diff)
    if a_90<.5:
        matches.append(90-diff)
    if a_0<0.5:
        matches.append(diff)
    if a_180<.5:
        matches.append(180-diff)
    if a_60<.5:
        matches.append(60-diff)
    if a_120<.5:
        matches.append(120-diff)
    if a_150<.5:
        matches.append(150-diff)
    return matches #.sort(reverse=True)


def get_angle_sexag(adhj_eclep_longitude_dir):
    g = int(adhj_eclep_longitude_dir)
    m = int((adhj_eclep_longitude_dir % 1) * 60)
    s = int((((adhj_eclep_longitude_dir % 1) * 60) % 1) * 60)
    print(f'gupta {g} {m} {s}')
    return g,m,s

if __name__ == '__main__':

    MC_adjust=[]
    #colocar MC en long ecliptica absoluta
    RAMC_radix = get_RAMC(297,36,8)
    print(f'RAMC radix: {RAMC_radix}')

    #fechas a utilizar para rectificar
    native_dates = []
    delta_days = dateptrdiffs(1976, 12, 26, 2026, 4, 21)
    direction_arc = get_direction_arc(delta_days)
    native_dates.append(direction_arc)
    print(f'days {delta_days} direction arc: {direction_arc}')
    delta_days = dateptrdiffs(1976, 12, 26, 2003, 9, 8)
    direction_arc = get_direction_arc(delta_days)
    native_dates.append(direction_arc)
    print(f'days {delta_days} direction arc: {direction_arc}')
    delta_days = dateptrdiffs(1976, 12, 26, 2005, 8, 20)
    direction_arc = get_direction_arc(delta_days)
    native_dates.append(direction_arc)
    print(f'days {delta_days} direction arc: {direction_arc}')

    """
    long ecliptica absoluta: posición desde 0 Aries
    """
    mercury = (30*9) + 23 + 7/60 + 48/3600
    venus = (30*10) + 20 + 1/60 + 49/3600
    mars =  (30*5) + 12 + 3/60 + 48/3600
    objects = {"mercury":mercury,
               "venus":venus,
               "mars":mars,}

    for cur_arc in native_dates:
        print("-----------------")
        print(f'--- rectificando para arco {cur_arc} ----')

        # direccionar el arco sobre el MC
        direct = RAMC_radix + cur_arc
        converse = RAMC_radix - cur_arc
        print(f'direct: {direct}')
        print(f'converse: {converse}')

        for cur_object in objects.keys():
            print ("-----------------------")
            object_ecliptic_long = objects.get(cur_object)
            print(f'processing {cur_object} {str(object_ecliptic_long)}')

            eclep_longitude_direct = get_ecliptic_longitude(direct)
            eclep_longitude_converse = get_ecliptic_longitude(converse)
            print(f'direct Ecliptic longitude: {eclep_longitude_direct}')
            print(f'converse Ecliptic longitude: {eclep_longitude_converse}')

            direct_diff = eclep_longitude_direct - object_ecliptic_long
            converse_diff = eclep_longitude_converse - object_ecliptic_long

            print(f'direct diff: {direct_diff}')
            print(f'converse diff: {converse_diff}')

            aspects = identify_aspect(direct_diff)
            if len(aspects)>0:
                print(f'--> 🎯 aspects: {aspects[0]} orbe')
                adhj_eclep_longitude_dir = eclep_longitude_direct + aspects[0]
                g,m,s = get_angle_sexag(adhj_eclep_longitude_dir)
                temp_ramc = get_RAMC(g, m, s)
                print(f'MC RA directo ajustada {temp_ramc}')
                adj_ramc =  temp_ramc - cur_arc
                print(f'--> RA directa ajustada: {adj_ramc} 🆗')
                MC_adjust.append(adj_ramc)

            aspects = identify_aspect(converse_diff)
            if len(aspects) > 0:
                print(f'--> 🎯 aspects: {aspects[0]} orbe')
                adhj_eclep_longitude_converse = eclep_longitude_converse + aspects[0]
                g,m,s = get_angle_sexag(adhj_eclep_longitude_converse)
                temp_ramc = get_RAMC(g, m, s)
                print(f'--> RA conversa ajustada: {temp_ramc}')
                adj_ramc =  temp_ramc + cur_arc
                print(f'--> MC radix ajustado: {adj_ramc} 🆗')
                MC_adjust.append(adj_ramc)

    for cur_ARMC in MC_adjust:
        print(f'')

    """
    mercury_diff = eclep_longitude_direct - mercury
    venus_diff = eclep_longitude_direct - venus
    mars_diff = eclep_longitude_direct - mars
    print(f'direct mercury diff: {mercury_diff}')
    print(f'direct venus diff: {venus_diff}')
    print(f'direct mars diff: {mars_diff}')
    

    mercury_diff = eclep_longitude_converse - mercury
    venus_diff = eclep_longitude_converse - venus
    mars_diff = eclep_longitude_converse - mars
    print(f'converse mercury diff: {mercury_diff}')
    print(f'converse venus diff: {venus_diff}')
    print(f'converse mars diff: {mars_diff}')

    aspects = identify_aspect(mars_diff)
    print(f'aspects: {aspects}')

    adhj_eclep_longitude_converse = eclep_longitude_converse + aspects[0]
    print(f'ecleptica conversa ajustada: {adhj_eclep_longitude_converse}')
    """
