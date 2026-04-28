from datetime import date, timedelta
import math
import logging  

logging.basicConfig(level=logging.INFO)

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
    ecliptic_longitude = math.degrees(math.atan(tmp))
    if ar >270:
        ecliptic_longitude = ecliptic_longitude + 360
    elif ar >180:
        ecliptic_longitude = ecliptic_longitude + 180
    return ecliptic_longitude

def identify_aspect(diff:float):
    logging.debug(f'orbe tolerance: {orbe_tolerance}')
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

def get_angle_sexag(adhj_eclep_longitude_dir):
    g = int(adhj_eclep_longitude_dir)
    m = int((adhj_eclep_longitude_dir % 1) * 60)
    s = int((((adhj_eclep_longitude_dir % 1) * 60) % 1) * 60)
    logging.debug(f'sexagecimal angle: {g} {m} {s}')
    return g,m,s

class natal_chart_object():
    """ Represents an astronomical object in a natal chart """
    self.mars = "mars"
    self.mercury = "mercury"
    self.jupiter = "jupiter"
    self.saturn = "saturn"
    self.uranus = "uranus"
    self.neptune = "neptune"
    self.pluto = "pluto"
    self.sun = "sun"
    self.moon = "moon"
    self.venus = "venus"
    self.mean_node = "mean_node"    
    self.AC = "AC"
    self.II = "II"
    self.III = "III"
    self.IC = "IC"
    self.V = "V"
    self.VI = "VI"
    self.aries="aries"
    self.taurus="taurus"
    self.gemini="gemini"
    self.cancer="cancer"
    self.leo="leo"
    self.virgo="virgo"
    self.libra="libra"
    self.scorpio="scorpio"
    self.sagittarius="sagittarius"
    self.capricorn="capricorn"
    self.aquarius="aquarius"
    self.piscis="piscis"

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

        self.ecliptic_longitude = (multi * 3) + degrees + (minutes / 60) + (seconds / 3600)
        logging.debug(f'longitud ecliptica {name} {self.ecliptic_longitude}')
