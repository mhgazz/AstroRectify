import math

def convert_angle_decimal(grade:int,mins:int,secs:int):
    """ convert angle in decimal degrees """
    decimal = grade + mins/60 + secs/3600
    return decimal

def get_RA_from_degree(grade:int,mins:int,secs:int):
    """ provide Right Ascention with standard declination value 23.44"""
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

def get_RA_from_decimal(dec_angle:float):
    """ provide Right Ascention with standard obliquity value 23.44"""
    obliquity: float = 23.44
    radian_angle = math.radians(dec_angle)
    tan_long = math.tan(radian_angle)
    cos_dec = math.cos(math.radians(obliquity))
    ra_rad = math.atan(tan_long*cos_dec)
    RA = math.degrees(ra_rad)
    if (RA<0):
        if dec_angle >270:
            RA = RA + 360
        elif dec_angle >180:
            RA = RA + 270
        else:
            RA = 180 + RA
    else:
        if dec_angle >180:
            RA = 180 + RA
    return RA

def get_declination(dec_angle:float):
    """ calculo de declinacion sin latitud ecliptica usando declinacion ecliptica"""
    obliquity: float = 23.44
    radian_angle = math.radians(dec_angle)
    sin_long = math.sin(radian_angle)
    sin_dec = math.sin(math.radians(obliquity))
    deg_dec = math.degrees(math.asin(sin_long * sin_dec))
    return deg_dec

def get_d_m(ra_angle: float, RAMC: float, RAIC: float, quadrant: int) -> float:
    """
    Calcula la distancia meridiana (dm) de un planeta.

    Args:
        ra_angle (float): El ángulo de ascensión recta del planeta.
        RAMC (float): Ascensión Recta del Medio Cielo.
        RAIC (float): Ascensión Recta del Fondo del Cielo.
        quadrant (int): El cuadrante en el que se encuentra el planeta (1 a 4).

    Returns:
        float: La distancia meridiana (dm).

    Raises:
        ValueError: Si el cuadrante no es un valor entre 1 y 4.
    """
    dm: float
    if quadrant == 1:
        dm = +1*(RAIC - ra_angle)
    elif quadrant == 2:
        dm = +1*(ra_angle - RAIC)
    elif quadrant == 3:
        dm = +1*(RAMC - ra_angle)
    elif quadrant == 4:
        dm = +1*(ra_angle - RAMC)
    else:
        raise ValueError("El cuadrante debe ser un valor entre 1 y 4.")
    return dm

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


def get_d_a(natal_geo_latitude: float, dec: float, cuadrant:float):
    """
    obtener diferencia ascencional
    parametros:
        natal_geo_latitude: latitud
        dec:                declinacion
        cuadrant:           cuadrante
    return:
        d_a:    diferencia ascencional
        s_arc:  semiarco
    """

    d_a = math.degrees(math.asin(math.tan(math.radians(dec)) * math.tan(math.radians(natal_geo_latitude))))
    if cuadrant>2:
        s_arc = 90 + d_a
    else:
        s_arc = 90 - d_a
    return d_a,s_arc

def get_angle_sexag(adhj_eclep_longitude_dir):
    g = int(adhj_eclep_longitude_dir)
    m = int((adhj_eclep_longitude_dir % 1) * 60)
    s = int((((adhj_eclep_longitude_dir % 1) * 60) % 1) * 60)
    return g,m,s

def get_placidus_mund_pos(md_s,sa_s,cuadrant,RAMC):
    """obtener posicion mundana Placidus"""
    pmp = 0
    if cuadrant==1:
        pmp = 90 - (90 * md_s / sa_s)
    elif cuadrant==2:
        pmp = 90 + (90 * md_s / sa_s)
    elif cuadrant==3:
        pmp = 270 - (90 * md_s / sa_s)
    else:
        pmp = 270 + (90 * md_s / sa_s)
    return pmp

def get_PMP(DA:float,PHI:float,decl:float,quadrt:int,RAMC:float,RAIC:float,RA_o:float):
    """obtener placidus posicion mundana Placidus"""
    pmp = 0
    R = 0
    if quadrt == 1:
        R = (RA_o - RAIC) / (90 - DA)
        pmp = RAIC - (90 * R)
    elif quadrt == 2:
        R = (RAIC - RA_o) / (90 - DA)
        pmp = RAIC + (90 * R)
    elif quadrt == 3:
        R = (RAMC - RA_o) / (90 + DA)
        pmp = RAMC - (90 * R)
    elif quadrt == 4:
        R = (RA_o - RAMC) / (90 + DA)
        pmp = RAMC + (90 * R)
    return pmp