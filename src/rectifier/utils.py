from datetime import date, timedelta
import math
import logging  

logging.basicConfig(level=logging.DEBUG)
orbe_tolerance : float = 1.0

def convert_ARMC_to_HL(armc,long,HS_GMT,GMT_Hour):
    """convert ARMC to local hour"""
    # long: geographical longitude W o E (if E then negative)
    # HS_GMT sideral time 0AM of the day in ephemerides tables
    # GMT_Hour time zone GMT (negative if W)
    # in case result is negative add 24hs

    HL = ((armc/15 + long - HS_GMT)*.99727) + GMT_Hour
    if HL < 0:
        HL = HL + 24
    
    return HL


def get_angle_sexag(adhj_eclep_longitude_dir):
    g = int(adhj_eclep_longitude_dir)
    m = int((adhj_eclep_longitude_dir % 1) * 60)
    s = int((((adhj_eclep_longitude_dir % 1) * 60) % 1) * 60)
    logging.debug(f'sexagecimal angle: {g} {m} {s}')
    return g,m,s

def convert_angle_decimal(grade:int,mins:int,secs:int):
    """ convert angle in decimal degrees """
    decimal = grade + mins/60 + secs/3600
    return decimal
def get_direction_arc(days:int):
    """get direction arc using Naibod key 59º08'33' """
    naibod_key: float = 0.00269861
    return naibod_key*days

def get_ecliptic_longitude(ar:float):
    """ convert a AR value to ecliptic longitude"""
    declination: float = 23.44
    tang_ar = math.tan(math.radians(ar))
    dec_cos = math.cos(math.radians(declination))
    tmp = tang_ar/dec_cos
    temp2 = math.atan(tmp)
    ecliptic_longitude = math.degrees(temp2)
    logging.debug(f'longitud ecliptica raw {ecliptic_longitude}')
    if ar >270:
        ecliptic_longitude = ecliptic_longitude + 360
    elif ar >=180:
        ecliptic_longitude = ecliptic_longitude + 180
    elif ar >=90:
        ecliptic_longitude = 180 + ecliptic_longitude

    logging.debug(f'longitud ecliptica final {ecliptic_longitude}')
    return ecliptic_longitude

def identify_aspect(diff:float):
    
    matches = ()
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
        matches=(90-diff,90,"cuadratura",diff)
        logging.info("----------------------------------- ")
        logging.info(f'cuadratura 90°: {a_90}')
    if a_0<orbe_tolerance:
        matches = (diff,0,"conjucion",diff)
        logging.info("----------------------------------- ")
        logging.info(f'conjucion 0°: {a_0}')
    if a_180<orbe_tolerance:
        matches=(180-diff,180,"oposicion",diff)
        logging.info("----------------------------------- ")
        logging.info(f'oposicion 180°: {a_180}')
    if a_60<orbe_tolerance:
        matches=(60-diff,60,"sextil",diff)
        logging.info("----------------------------------- ")
        logging.info(f'sextil 60°: {a_60}')
    if a_120<orbe_tolerance:
        matches=(120-diff,120,"trigono",diff)
        logging.info("----------------------------------- ")
        logging.info(f'trigono 120°: {a_120}')
    if a_150<orbe_tolerance:
        matches=(150-diff,150,"quincuncio",diff)
        logging.info("----------------------------------- ")
        logging.info(f'quincuncio 150°: {a_150}')
    if a_30<orbe_tolerance:
        matches=(30-diff,30,"semisextil",diff)
        logging.info("----------------------------------- ")
        logging.info(f'semisextil 30°: {a_30}')
    if a_45<orbe_tolerance:
        matches=(45-diff,45,"semicuadratural",diff)
        logging.info("----------------------------------- ")
        logging.info(f'semicuadratural 45°: {a_45}')
    if a_135<orbe_tolerance:
        matches=(135-diff,135,"sesquicuadratura",diff)
        logging.info("----------------------------------- ")
        logging.info(f'sesquicuadratura 135°: {a_135}')
    if a_72<orbe_tolerance:
        matches=(72-diff,72,"quintil",diff)
        logging.info("----------------------------------- ")
        logging.info(f'quintil 72°: {a_72}')
    if a_144<orbe_tolerance:
        matches=(144-diff,144,"biquintil",diff)
        logging.info("----------------------------------- ")
        logging.info(f'biquintil 144°: {a_144}')    
    return matches

def get_angle_sexag(decimal_angle:float):
    g = int(decimal_angle)
    m = int((decimal_angle % 1) * 60)
    s = round((((decimal_angle % 1) * 60) % 1) * 60)
    logging.debug(f'sexagecimal angle: {g} {m} {s}')
    return g,m,s

def dateptrdiffs(ya, ma, da, yb, mb, db):
    """ get delta dates in days"""
    date_a=date(ya,ma,da)
    date_b=date(yb,mb,db)
    delta = date_b-date_a
    return int(delta.days)

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
        elif grade >=90:
            RAMC = RAMC + 180
    else:
        if grade >=180:
            RAMC = 180 + RAMC
    return RAMC

class natal_chart_object():
    """ Represents an astronomical object in a natal chart """
    mars = "mars"
    mercury = "mercury"
    jupiter = "jupiter"
    saturn = "saturn"
    uranus = "uranus"
    neptune = "neptune"
    pluto = "pluto"
    sun = "sun"
    moon = "moon"
    venus = "venus"
    mean_node = "mean_node"    
    AC = "AC"
    II = "II"
    III = "III"
    IC = "IC"
    V = "V"
    VI = "VI"
    aries="aries"
    taurus="taurus"
    gemini="gemini"
    cancer="cancer"
    leo="leo"
    virgo="virgo"
    libra="libra"
    scorpio="scorpio"
    sagittarius="sagittarius"
    capricorn="capricorn"
    aquarius="aquarius"
    piscis="piscis"

    def __init__(self, name: str, degrees: int, minutes: int, seconds: int, sign: str):
        self.name = name
        
        match sign:
            case "aries":
                multi = 0
            case "taurus":
                multi = 1
            case "gemini":
                multi = 2
            case "cancer":
                multi = 3
            case "leo":
                multi = 4
            case "virgo":
                multi = 5
            case "libra":
                multi = 6
            case "scorpio":
                multi = 7
            case "sagittarius":
                multi = 8
            case "capricorn":
                multi = 9
            case "aquarius":
                multi = 10
            case "piscis":
                multi = 11

        self.ecliptic_longitude = (multi * 30) + degrees + (minutes / 60) + (seconds / 3600)
        logging.debug(f'longitud ecliptica {name} {self.ecliptic_longitude}')
