# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.

from datetime import date, timedelta
import math
import logging  


logging.basicConfig(level=logging.INFO)
orbe_tolerance : float = 1.0



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
    logging.debug(f'{grade} {mins} {secs} raw RAMC: {RAMC}')
    if (RAMC<0):
        if grade >=270:
            RAMC = RAMC + 360
        elif grade >=180:
            RAMC = RAMC + 270
    else:
        if grade >=180:
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
    logging.debug(f'orbe tolerance: {orbe_tolerance}')
    matches = []
    a_90 = abs(90 - diff)
    a_180 = abs(180 - diff)
    a_120 = abs(120 - diff)
    a_150 = abs(150 - diff)
    a_60 = abs(60 - diff)
    a_0 = abs(diff)
    a_30 = abs(30 - diff)
    a_45 = abs(45 - diff)
    a_135 = abs(135 - diff)
    a_72 = abs(72 - diff)
    a_144 = abs(144 - diff)

    if a_90<orbe_tolerance:
        matches.append(90-diff)
        logging.info("----------------------------------- ")
        logging.info(f'cuadratura 90°: {a_90}')
    if a_0<orbe_tolerance:
        matches.append(diff)
        logging.info("----------------------------------- ")
        logging.info(f'conjucion 0°: {a_0}')
    if a_180<orbe_tolerance:
        matches.append(180-diff)
        logging.info("----------------------------------- ")
        logging.info(f'oposicion 180°: {a_180}')
    if a_60<orbe_tolerance:
        matches.append(60-diff)
        logging.info("----------------------------------- ")
        logging.info(f'sextial 60°: {a_60}')
    if a_120<orbe_tolerance:
        matches.append(120-diff)
        logging.info("----------------------------------- ")
        logging.info(f'cuadratura 120°: {a_120}')
    if a_150<orbe_tolerance:
        matches.append(150-diff)
        logging.info("----------------------------------- ")
        logging.info(f'quincuncio 150°: {a_150}')
    if a_30<orbe_tolerance:
        matches.append(30-diff)
        logging.info("----------------------------------- ")
        logging.info(f'semisextil 30°: {a_30}')
    if a_45<orbe_tolerance:
        matches.append(45-diff)
        logging.info("----------------------------------- ")
        logging.info(f'semicuadratural 45°: {a_45}')
    if a_135<orbe_tolerance:
        matches.append(135-diff)
        logging.info("----------------------------------- ")
        logging.info(f'sesquicuadratura 135°: {a_135}')
    if a_72<orbe_tolerance:
        matches.append(72-diff)
        logging.info("----------------------------------- ")
        logging.info(f'quintil 72°: {a_72}')
    if a_144<orbe_tolerance:
        matches.append(144-diff)
        logging.info("----------------------------------- ")
        logging.info(f'biquintil 144°: {a_144}')
    
    return matches


def get_angle_sexag(adhj_eclep_longitude_dir):
    g = int(adhj_eclep_longitude_dir)
    m = int((adhj_eclep_longitude_dir % 1) * 60)
    s = int((((adhj_eclep_longitude_dir % 1) * 60) % 1) * 60)
    logging.debug(f'sexagecimal angle: {g} {m} {s}')
    return g,m,s

if __name__ == '__main__':

    MC_adjust=[]
    #colocar MC en long ecliptica absoluta
    RAMC_radix = get_RAMC(297,36,8)
    geograph_long = 4.046262
    HS_GMT = 6.30777 
    GMT_Hour = -3

    logging.info('RAMC radix:' + str(RAMC_radix))

    #fechas a utilizar para rectificar
    native_dates = {}
    delta_days = dateptrdiffs(1976, 12, 26, 2026, 4, 21)
    direction_arc = get_direction_arc(delta_days)
    event_title="Procedimiento de infiltración en la cadera"
    native_dates[event_title]=direction_arc
    logging.debug(f'days {delta_days} direction arc: {direction_arc}')
    
    delta_days = dateptrdiffs(1976, 12, 26, 2003, 9, 8)
    direction_arc = get_direction_arc(delta_days)
    event_title="Primer empleo profesional"
    native_dates[event_title]=direction_arc
    logging.debug(f'days {delta_days} direction arc: {direction_arc}')
    
    delta_days = dateptrdiffs(1976, 12, 26, 2005, 8, 20)
    direction_arc = get_direction_arc(delta_days)
    event_title="Primer casamiento"
    native_dates[event_title]=direction_arc
    logging.debug(f'days {delta_days} direction arc: {direction_arc}')
    
    delta_days = dateptrdiffs(1976, 12, 26, 2016, 10, 8)
    direction_arc = get_direction_arc(delta_days)
    event_title="Primera cita con Luza"
    native_dates[event_title]=direction_arc
    logging.debug(f'days {delta_days} direction arc: {direction_arc}')
    
    delta_days = dateptrdiffs(1976, 12, 26, 2005, 11, 20)
    direction_arc = get_direction_arc(delta_days)
    event_title="Jail"
    native_dates[event_title]=direction_arc
    logging.debug(f'days {delta_days} direction arc: {direction_arc}')

    delta_days = dateptrdiffs(1976, 12, 26, 2018, 6, 16)
    direction_arc = get_direction_arc(delta_days)
    event_title="Casamiento con Luza"
    native_dates[event_title]=direction_arc
    logging.debug(f'days {delta_days} direction arc: {direction_arc}')

    delta_days = dateptrdiffs(1976, 12, 26, 2023, 9, 22)
    direction_arc = get_direction_arc(delta_days)
    event_title="Casamiento civil con Luza"
    native_dates[event_title]=direction_arc
    logging.debug(f'days {delta_days} direction arc: {direction_arc}')

    delta_days = dateptrdiffs(1976, 12, 26, 2022, 12, 7)
    direction_arc = get_direction_arc(delta_days)
    event_title="Accidente lumbar con perdida de movilidad"
    native_dates[event_title]=direction_arc
    logging.debug(f'days {delta_days} direction arc: {direction_arc}')

    delta_days = dateptrdiffs(1976, 12, 26, 2009, 2, 27)
    direction_arc = get_direction_arc(delta_days)
    event_title="Primera separacion"
    native_dates[event_title]=direction_arc
    logging.debug(f'days {delta_days} direction arc: {direction_arc}')

    delta_days = dateptrdiffs(1976, 12, 26, 2016, 12, 1)
    direction_arc = get_direction_arc(delta_days)
    event_title="Ingreso a IBM de Colombia"
    native_dates[event_title]=direction_arc
    logging.debug(f'days {delta_days} direction arc: {direction_arc}')


    """
    long ecliptica absoluta: posición desde 0 Aries
    """
    sun = (30*9) + 5 + 5/60 + 56/3600
    moon = (30*11) + 17 + 9/60 + 43/3600
    mercury = (30*9) + 23 + 7/60 + 48/3600
    venus = (30*10) + 20 + 1/60 + 49/3600
    mars =  (30*5) + 12 + 3/60 + 48/3600
    jupiter = (30*1) + 21 + 50/60 + 15/3600
    saturn = (30*3) + 16 +  7/60 + 2/3600
    uranus = (30*7) + 10 + 40/60 + 8/3600
    neptune = (30*8) + 14 + 28/60
    pluto = (30*6) + 14 + 3/60/ + 57/3600
    mean_node = (30*7) + 0 + 9/60 + 51/3600
    AC = 25 + 11/60 + 1/3600
    II = (30*1) + 23 + 39/60 + 59/3600
    III = (30*2) + 24 + 46/60 + 52/3600
    IC = (30*3) + 27 + 39/60 + 1/3600
    V = (30*5) + 0 + 9/60 + 8/3600
    VI = (30*5) + 29 + 44/60 + 59/3600

    objects = {"sun":sun,
               "moon":moon,
               "mercury":mercury,
               "venus":venus,
               "mars":mars,
               "jupiter":jupiter,
               "saturn":saturn,
               "uranus":uranus,
               "neptune":neptune,
               "pluto":pluto,
               "mean_node":mean_node,
               "AC":AC,
               "II":II,
               "III":III,
               "IC":IC,
               "V":V,
               "VI":VI
               }

    for cur_event in native_dates:
        cur_arc = native_dates[cur_event]
        logging.info(f'\n\n--- rectificando para arco {cur_arc} {cur_event} ----')

        # direccionar el arco sobre el MC
        direct = RAMC_radix + cur_arc
        converse = RAMC_radix - cur_arc
        logging.info(f'direct: {direct}')
        logging.info(f'converse: {converse}')

        for cur_object in objects.keys():
            object_ecliptic_long = objects.get(cur_object)
            logging.debug(f'processing {cur_object} {str(object_ecliptic_long)}')

            eclep_longitude_direct = get_ecliptic_longitude(direct)
            eclep_longitude_converse = get_ecliptic_longitude(converse)
            logging.debug(f'direct Ecliptic longitude: {eclep_longitude_direct}')
            logging.debug(f'converse Ecliptic longitude: {eclep_longitude_converse}')

            direct_diff = eclep_longitude_direct - object_ecliptic_long
            converse_diff = eclep_longitude_converse - object_ecliptic_long

            logging.debug(f'direct diff: {direct_diff}')
            logging.debug(f'converse diff: {converse_diff}')

            logging.debug(f'identificando aspectos con {cur_object} radical')
            aspects = identify_aspect(direct_diff)
            if len(aspects)>0:
                logging.info(f'MC ecliptica {eclep_longitude_direct}')
                logging.info(f'{cur_object} {object_ecliptic_long} 🎯 aspects: {aspects[0]} orbe')
                adhj_eclep_longitude_dir = eclep_longitude_direct + aspects[0]
                g,m,s = get_angle_sexag(adhj_eclep_longitude_dir)
                temp_ramc = get_RAMC(g, m, s)
                logging.info(f'MC RA directo ajustada {temp_ramc}')
                adj_ramc =  temp_ramc - cur_arc
                logging.info(f'--> RA directa ajustada: {adj_ramc} 🆗')
                MC_adjust.append(adj_ramc)

            aspects = identify_aspect(converse_diff)
            if len(aspects) > 0:
                logging.info(f'MC ecliptica {eclep_longitude_converse}')
                logging.info(f'{cur_object} {object_ecliptic_long} 🎯 aspects: {aspects[0]} orbe')
                adhj_eclep_longitude_converse = eclep_longitude_converse + aspects[0]
                g,m,s = get_angle_sexag(adhj_eclep_longitude_converse)
                temp_ramc = get_RAMC(g, m, s)
                logging.info(f'--> RA conversa ajustada: {temp_ramc}')
                adj_ramc =  temp_ramc + cur_arc
                logging.info(f'--> MC radix ajustado: {adj_ramc} 🆗')
                MC_adjust.append(adj_ramc)

    #results computing
    logging.info("\n\n\nresultados finales:")
    logging.info("--------------------------------")
    x = 0
    t = 0
    for cur_ARMC in MC_adjust:
        x = x + 1
        t = t + cur_ARMC
        logging.info(f'MC radix ajustado: {cur_ARMC}')
    new_ARMC = t/x
    if x > 0:
        logging.info("--------------------------")
        logging.info(f'nueva ARMC {new_ARMC}')
        new_eceliptic_long = get_ecliptic_longitude(new_ARMC)
        logging.info(f'ARMC radical original {RAMC_radix}')
        logging.info(f'nueva longitud ecliptica {new_eceliptic_long}')
        HL = ((new_ARMC/15 + geograph_long - HS_GMT)*.99727) + GMT_Hour
        h,m,s = get_angle_sexag(HL)
        logging.info(f'nueva hora local {h} {m} {s}')

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
