# -*- coding: utf-8 -*-
"""
Direcciones primarias: MC a planetas
Método: Placidus de semi-arco

Dependencia:
    pip install pyswisseph

Nota:
    Por defecto, el MC se trata como ángulo, con semi-arco angular de 90°.
    Si se quiere tratar el grado del MC natal como punto con declinación propia,
    usar mc_como_punto=True.
"""

import math

try:
    import swisseph as swe
except ImportError:
    swe = None


TOL = 1e-9


# ----------------------------------------------------------------------
# Configuración de planetas
# ----------------------------------------------------------------------

if swe is not None:
    PLANETAS = {
        "Sol": swe.SUN,
        "Luna": swe.MOON,
        "Mercurio": swe.MERCURY,
        "Venus": swe.VENUS,
        "Marte": swe.MARS,
        "Júpiter": swe.JUPITER,
        "Saturno": swe.SATURN,
        "Urano": swe.URANUS,
        "Neptuno": swe.NEPTUNE,
        "Plutón": swe.PLUTO,
        "Nodo Verdadero": swe.TRUE_NODE,
    }

    # Por defecto usamos Moshier, que viene incorporado y no requiere
    # descargar archivos de efemérides. Para mayor precisión, se puede
    # cambiar a swe.FLG_SWIEPH si se tienen los archivos de Swiss Ephemeris.
    DEFAULT_EPH_FLAG = getattr(swe, "FLG_MOSEPH", 0) | getattr(swe, "FLG_SPEED", 0)

else:
    PLANETAS = {}
    DEFAULT_EPH_FLAG = 0


# ----------------------------------------------------------------------
# Utilidades angulares
# ----------------------------------------------------------------------

def norm360(x: float) -> float:
    """Normaliza un ángulo a [0, 360)."""
    return x % 360.0


def norm180(x: float) -> float:
    """Normaliza un ángulo a [-180, 180)."""
    return (x + 180.0) % 360.0 - 180.0


def dms(x: float, normalize: bool = True) -> str:
    """
    Convierte grados decimales a grados°minutos'segundos".
    """
    if normalize:
        x = norm360(x)

    signo = "-" if x < 0 else ""
    x = abs(x)

    d = int(x)
    mf = (x - d) * 60.0
    m = int(mf)
    s = (mf - m) * 60.0

    if s >= 59.995:
        s = 0.0
        m += 1
        if m == 60:
            m = 0
            d += 1

    return f"{signo}{d:03d}°{m:02d}'{s:05.2f}\""


# ----------------------------------------------------------------------
# Tiempo y coordenadas básicas
# ----------------------------------------------------------------------

def jd_utc(year: int, month: int, day: int, hour_utc: float, calendario: str = "gregoriano") -> float:
    """
    Obtiene el Julian Day correspondiente a una fecha/hora en UTC.

    hour_utc puede ser decimal:
        12.5 = 12:30 UTC
    """
    if swe is None:
        raise ImportError(
            "No está instalado pyswisseph.\n"
            "Instálalo con: pip install pyswisseph"
        )

    if calendario.lower().startswith("g"):
        cal = getattr(swe, "GREG_CAL", 1)
    else:
        cal = getattr(swe, "JUL_CAL", 0)

    return swe.julday(year, month, day, float(hour_utc), cal)


def obtener_oblicuidad(jd: float) -> float:
    """
    Obtiene la oblicuidad de la eclíptica para la fecha.
    Intenta usar Swiss Ephemeris; si falla, usa una fórmula aproximada.
    """
    if swe is not None:
        try:
            # SE_ECL_NUT suele devolver oblicuidad verdadera en x[0]
            x = swe.calc_ut(jd, getattr(swe, "ECL_NUT", -1), 0)
            if x and len(x) > 0:
                return float(x[0])
        except Exception:
            pass

    # Oblicuidad media aproximada, suficiente para muchos casos.
    T = (jd - 2451545.0) / 36525.0
    eps = (
        23.0 + 26.0 / 60.0 + 21.448 / 3600.0
        - (46.8150 * T + 0.00059 * T * T - 0.001813 * T ** 3) / 3600.0
    )
    return eps


def obtener_ramc(jd: float, lon_geo: float) -> float:
    """
    Calcula la RAMC / Tiempo Sidéreo Local en grados.

    lon_geo: longitud geográfica en grados.
             Este positiva, Oeste negativa.
    """
    if swe is None:
        raise ImportError("pyswisseph no está instalado.")

    gst_horas = swe.sidtime(jd)  # Tiempo sidéreo de Greenwich en horas
    return norm360(gst_horas * 15.0 + lon_geo)


def longitud_mc(ramc: float, eps: float) -> float:
    """
    Calcula la longitud eclíptica del Medio Cielo a partir de la RAMC
    y la oblicuidad de la eclíptica.
    """
    r = math.radians(ramc)
    e = math.radians(eps)

    lam = math.degrees(
        math.atan2(
            math.sin(r),
            math.cos(r) * math.cos(e)
        )
    )
    return norm360(lam)


# ----------------------------------------------------------------------
# Transformación eclíptica -> ecuatorial
# ----------------------------------------------------------------------

def ecl_to_equ(lon: float, lat: float, eps: float) -> tuple[float, float]:
    """
    Convierte longitud/latitud eclípticas a Ascensión Recta y Declinación.

    Entrada:
        lon: longitud eclíptica en grados
        lat: latitud eclíptica en grados
        eps: oblicuidad de la eclíptica en grados

    Salida:
        (ra, dec) en grados
    """
    lon = math.radians(norm360(lon))
    lat = math.radians(lat)
    eps = math.radians(eps)

    # Vectores en coordenadas eclípticas
    x = math.cos(lat) * math.cos(lon)
    y = math.cos(lat) * math.sin(lon) * math.cos(eps) - math.sin(lat) * math.sin(eps)
    z = math.cos(lat) * math.sin(lon) * math.sin(eps) + math.sin(lat) * math.cos(eps)

    ra = math.degrees(math.atan2(y, x))
    dec = math.degrees(math.asin(max(-1.0, min(1.0, z))))

    return norm360(ra), dec


# ----------------------------------------------------------------------
# Semi-arcs y posición mundana Placidus
# ----------------------------------------------------------------------

def semiarcos(dec: float, lat_geo: float) -> tuple[float, float]:
    """
    Calcula los semi-arcs diurno y nocturno de un cuerpo
    según su declinación y la latitud geográfica.

    Devuelve:
        (semi_arco_diurno, semi_arco_nocturno) en grados.

    En latitudes polares, Placidus puede volverse degenerado.
    """
    if abs(lat_geo) >= 90.0 - 1e-12:
        # Caso degenerado; se evita división por cero.
        return 180.0, 0.0

    phi = math.radians(lat_geo)
    delta = math.radians(dec)

    arg = -math.tan(phi) * math.tan(delta)

    if arg <= -1.0:
        # Circumpolar siempre sobre el horizonte
        d = 180.0
        n = 0.0
    elif arg >= 1.0:
        # Circumpolar siempre bajo el horizonte
        d = 0.0
        n = 180.0
    else:
        d = math.degrees(math.acos(arg))
        n = 180.0 - d

    return d, n


def posicion_mundana_placidus(ra: float, dec: float, ramc: float, lat_geo: float) -> dict:
    """
    Calcula la posición mundana de un punto según Placidus.

    Devuelve:
        diccionario con:
            h: hora angular en grados [0, 360)
            above: True si está sobre el horizonte
            cuadrante:
                'sobre_horizonte_oeste'  -> MC a Descendente
                'sobre_horizonte_este'   -> Ascendente a MC
                'bajo_horizonte_oeste'   -> Descendente a IC
                'bajo_horizonte_este'    -> IC a Ascendente
            md: distancia meridiana usada
            semi_arco: semi-arco correspondiente
            fraccion: md / semi_arco

    Nota sobre la fracción:
        En cuadrantes superiores:
            se mide desde el MC.
        En cuadrantes inferiores:
            se mide desde el IC.
    """
    h = norm360(ramc - ra)

    d_sa, n_sa = semiarcos(dec, lat_geo)

    phi = math.radians(lat_geo)
    delta = math.radians(dec)
    h_rad = math.radians(h)

    sin_alt = (
        math.sin(phi) * math.sin(delta)
        + math.cos(phi) * math.cos(delta) * math.cos(h_rad)
    )

    above = sin_alt >= -1e-10

    if above:
        sa = d_sa
        if sa < TOL:
            sa = TOL

        if h <= d_sa + TOL:
            cuadrante = "sobre_horizonte_oeste"
            md = min(max(h, 0.0), d_sa)
        else:
            cuadrante = "sobre_horizonte_este"
            md = min(max(360.0 - h, 0.0), d_sa)

    else:
        sa = n_sa
        if sa < TOL:
            sa = TOL

        if h >= 180.0 - TOL:
            cuadrante = "bajo_horizonte_este"
            md = min(max(h - 180.0, 0.0), n_sa)
        else:
            cuadrante = "bajo_horizonte_oeste"
            md = min(max(180.0 - h, 0.0), n_sa)

    fraccion = md / sa if sa > TOL else 0.0
    fraccion = min(1.0, max(0.0, fraccion))

    return {
        "h": h,
        "above": above,
        "cuadrante": cuadrante,
        "md": md,
        "semi_arco": sa,
        "fraccion": fraccion,
    }


def hora_requerida(
    cuadrante: str,
    fraccion: float,
    sa_superior: float,
    sa_inferior: float
) -> float | None:
    """
    Convierte la fracción mundana del planeta promisor
    en el arco/base equivalente para el significador.

    Para MC como ángulo:
        sa_superior = 90
        sa_inferior = 90

    Para MC como punto:
        sa_superior = semi-arco diurno del grado MC
        sa_inferior = semi-arco nocturno del grado MC
    """
    f = min(1.0, max(0.0, fraccion))

    if cuadrante == "sobre_horizonte_oeste":
        # MC -> Descendente
        if sa_superior <= TOL:
            return None
        return norm360(f * sa_superior)

    if cuadrante == "sobre_horizonte_este":
        # Ascendente -> MC
        # Visto desde MC en movimiento directo, queda cerca de 360°
        if sa_superior <= TOL:
            return None
        return norm360(-f * sa_superior)

    if cuadrante == "bajo_horizonte_oeste":
        # Descendente -> IC
        # Aquí f viene medida desde IC hacia Descendente.
        if sa_inferior <= TOL:
            return None
        return norm360(180.0 - f * sa_inferior)

    if cuadrante == "bajo_horizonte_este":
        # IC -> Ascendente
        if sa_inferior <= TOL:
            return None
        return norm360(180.0 + f * sa_inferior)

    return None


# ----------------------------------------------------------------------
# Función principal
# ----------------------------------------------------------------------

def calcular_direcciones_mc(
    year: int,
    month: int,
    day: int,
    hour_utc: float,
    lat_geo: float,
    lon_geo: float,
    *,
    calendario: str = "gregoriano",
    eph_flag: int | None = None,
    mc_como_punto: bool = False
) -> dict:
    """
    Calcula direcciones primarias del MC a planetas por Placidus semi-arco.

    Parámetros:
        year, month, day: fecha calendario.
        hour_utc: hora en UTC decimal.
        lat_geo: latitud geográfica en grados. Norte positiva, Sur negativa.
        lon_geo: longitud geográfica en grados. Este positiva, Oeste negativa.
        calendario: "gregoriano" o "juliano".
        eph_flag: flag de efemérides Swiss Ephemeris.
        mc_como_punto:
            False => MC como ángulo, semi-arco angular de 90°.
            True  => MC natal como punto con declinación propia.

    Devuelve:
        dict con datos generales y lista de direcciones.
    """
    if swe is None:
        raise ImportError(
            "No está instalado pyswisseph.\n"
            "Instálalo con: pip install pyswisseph"
        )

    if eph_flag is None:
        eph_flag = DEFAULT_EPH_FLAG

    jd = jd_utc(year, month, day, hour_utc, calendario)
    eps = obtener_oblicuidad(jd)
    ramc = obtener_ramc(jd, lon_geo)

    mc_lon = longitud_mc(ramc, eps)
    mc_ra, mc_dec = ecl_to_equ(mc_lon, 0.0, eps)

    if mc_como_punto:
        # El grado del MC natal se trata como punto significador
        sa_sup, sa_inf = semiarcos(mc_dec, lat_geo)
        h0 = norm360(ramc - mc_ra)
    else:
        # MC como ángulo: cada cuadrante angular mide 90°
        sa_sup = 90.0
        sa_inf = 90.0
        h0 = 0.0

    direcciones = []

    for nombre, body in PLANETAS.items():
        try:
            x = swe.calc_ut(jd, body, eph_flag)
        except Exception as E:
            # Reintento sin velocidad si fallara
            print(E)
    
            try:
                flag_sin_speed = eph_flag & ~getattr(swe, "FLG_SPEED", 0)
                x = swe.calc_ut(jd, body, flag_sin_speed)
            except Exception as E:
                print(E)

        p_lon = x[0][0]
        p_lat = x[1]
        p_ra, p_dec = ecl_to_equ(p_lon, p_lat, eps)

        pos = posicion_mundana_placidus(p_ra, p_dec, ramc, lat_geo)

        h_req = hora_requerida(
            pos["cuadrante"],
            pos["fraccion"],
            sa_sup,
            sa_inf
        )

        if h_req is None:
            continue

        directo = norm360(h_req - h0)
        converso = norm360(h0 - h_req)

        # Corrección por redondeo
        if directo > 360.0 - 1e-7:
            directo = 0.0
        if converso > 360.0 - 1e-7:
            converso = 0.0

        if directo <= converso:
            tipo_principal = "directo"
            arco_principal = directo
        else:
            tipo_principal = "converso"
            arco_principal = converso

        direcciones.append({
            "planeta": nombre,
            "longitud": p_lon,
            "latitud": p_lat,
            "ra": p_ra,
            "dec": p_dec,
            "cuadrante": pos["cuadrante"],
            "distancia_meridiana": pos["md"],
            "semi_arco_promittor": pos["semi_arco"],
            "fraccion": pos["fraccion"],
            "arco_directo": directo,
            "arco_converso": converso,
            "tipo_principal": tipo_principal,
            "arco_principal": arco_principal,
            "anos_ptolomeo": arco_principal,  # clave 1° = 1 año
        })

    direcciones.sort(key=lambda d: d["arco_principal"])

    return {
        "jd": jd,
        "ramc": ramc,
        "oblicuidad": eps,
        "mc_longitud": mc_lon,
        "mc_ra": mc_ra,
        "mc_dec": mc_dec,
        "mc_como_punto": mc_como_punto,
        "semi_arco_mc_superior": sa_sup,
        "semi_arco_mc_inferior": sa_inf,
        "direcciones": direcciones,
    }


# ----------------------------------------------------------------------
# Salida formateada
# ----------------------------------------------------------------------

def imprimir_resultado(res: dict) -> None:
    print("=" * 95)
    print("Direcciones primarias: MC a planetas")
    print("Método: Placidus de semi-arco")
    print("=" * 95)

    print(f"JD:       {res['jd']:.6f}")
    print(f"RAMC:     {dms(res['ramc'])}")
    print(f"MC:       {dms(res['mc_longitud'])}")

    modo = (
        "MC como punto (semi-arco real del grado MC)"
        if res["mc_como_punto"]
        else "MC como ángulo (semi-arco angular de 90°)"
    )
    print(f"Modo:     {modo}")

    print()

    encabezado = (
        f"{'Planeta':<15} "
        f"{'Longitud':>14} "
        f"{'Directo':>14} "
        f"{'Converso':>14} "
        f"{'Principal':>14} "
        f"{'Años Ptol.':>12}"
    )
    print(encabezado)
    print("-" * len(encabezado))

    if not res["direcciones"]:
        print("No se calcularon direcciones.")
        return

    for d in res["direcciones"]:
        linea = (
            f"{d['planeta']:<15} "
            f"{dms(d['longitud']):>14} "
            f"{dms(d['arco_directo']):>14} "
            f"{dms(d['arco_converso']):>14} "
            f"{dms(d['arco_principal']):>14} "
            f"{d['arco_principal']:12.4f}"
        )
        print(linea)

    print()
    print("Nota: 'Años Ptol.' usa la clave tradicional 1° = 1 año.")


# ----------------------------------------------------------------------
# Ejemplo
# ----------------------------------------------------------------------

if __name__ == "__main__":
    # try:
    #     # Ejemplo: 5 de agosto de 2026, 12:00 UTC
    #     # Madrid: lat 40.4168 N, lon 3.7038 W
    #     resultado = calcular_direcciones_mc(
    #         year=1976,
    #         month=12,
    #         day=26,
    #         hour_utc=17.40,
    #         lat_geo=-32.95,
    #         lon_geo=-60.6667,
    #         mc_como_punto=False  # MC como ángulo, método angular estándar
    #     )

    #     imprimir_resultado(resultado)

    # except Exception as e:
    #     print("Error:")
    #     print(e)

    # Ejemplo: 5 de agosto de 2026, 12:00 UTC
    # Madrid: lat 40.4168 N, lon 3.7038 W
    resultado = calcular_direcciones_mc(
        year=1976,
        month=12,
        day=26,
        hour_utc=17.40,
        lat_geo=-32.95,
        lon_geo=-60.6667,
        mc_como_punto=False  # MC como ángulo, método angular estándar
    )

    imprimir_resultado(resultado)