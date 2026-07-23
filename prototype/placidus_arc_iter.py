import math


def sgn(x):
    """Función de signo tal como la define el texto."""
    if x < 0:
        return -1
    return 1


def calcular_jd(Y, M, D, G):
    """Paso 1: Calcula el Día Juliano (JD) de nacimiento."""
    term1 = 367 * Y
    term2 = int(1.75 * (Y + int((M + 9) / 12)))
    term3 = int((275 * M) / 9) + D + (G / 24.0)
    term4 = 0.5 * sgn(100 * Y + M - 190002.5)

    jd = term1 - term2 + term3 - term4 + 1721014
    return jd


def calcular_dn(Y, M, D):
    """Calcula el número de día del año (DN) según la fórmula del texto."""
    term1 = int((275 * M) / 9) + D - 30
    term2 = int((M + 9) / 12) * (1 + int((Y + 2 - 4 * int(Y / 4)) / 3))
    return term1 - term2




def algoritmo_true_solar_arc(Y, M, D, G, RA_Su, A, PL):
    """
    Implementa el algoritmo completo de True Solar Arc en RA.

    Parámetros:
    Y, M, D, G: Año, Mes, Día y Hora GMT de nacimiento.
    RA_Su: Ascensión Recta del sol natal.
    A: Arco absoluto de dirección.
    PL: Longitud correspondiente a PR de la Fórmula A3 (requerida por el texto).
    """
    # 1. Calcular Día Juliano
    JD = calcular_jd(Y, M, D, G)
    print(f"[Paso 1] JD calculado: {JD:.3f}")

    # 2. Calcular PR y ajustar PL (Paso 2 y 3 del texto)
    PR = RA_Su + A
    if PR > 360:
        PL = PL % 360  # Ajuste si excede 360

    L = PL + 360 * (Y - 1900)
    print(f"[Paso 2-3] L calculado: {L:.4f}")

    # 4. Valor inicial de T
    T = (JD + A - 2415020) / 36525.0
    print(f"[Paso 4] T inicial: {T:.7f}")

    # 5 y 6. Proceso iterativo
    tolerancia = 1e-7
    max_iteraciones = 1000
    it = 0

    while it < max_iteraciones:
        T_viejo = T

        # Paso 5: Calcular Z (en grados para las funciones trigonométricas)
        Z_deg = 358.476 + 35999.05 * T
        Z_rad = math.radians(Z_deg)

        # Paso 6: Reciclar el valor de T
        numerador = L - 279.691 - 1.919 * math.sin(Z_rad) - 0.02 * math.sin(2 * Z_rad)
        denominador = 36000.769 - 0.0048 * math.sin(Z_rad)
        T = numerador / denominador

        # Comprobar convergencia
        if abs(T - T_viejo) < tolerancia:
            print(f"[Paso 5-6] Convergencia alcanzada en la iteración {it + 1}. T final: {T:.7f}")
            break
        it += 1
    else:
        print("[Alerta] No se alcanzó la convergencia exacta en el límite de iteraciones.")

    # 7. Calcular DY (Días transcurridos)
    DY = 36525 * T + 2415020 - JD
    if DY < 0:
        DY += 365.2422

    # Calcular DN (Día del año de nacimiento)
    DN = calcular_dn(Y, M, D)

    # Calcular fecha final en años y decimales (PY)
    PY = Y + (DN / 365.0 ) + DY

    print(f"[Paso 7] DY (Días desde nacimiento): {DY:.4f}")
    print(f"[Resultado] PY (Fecha final de operación): {PY:.4f}")

    return PY

def get_ecliptic_long(pr:float):
    longitud_pl = math.degrees(math.atan(math.tan(math.radians(pr))/math.cos(math.radians(23.44))))
    if pr>90 and pr<270:
        longitud_pl = longitud_pl + 180
    if pr>270 and pr<360:
        longitud_pl = longitud_pl + 360
    return longitud_pl


# --- EJEMPLO DE USO (Datos basados parcialmente en el ejemplo del texto) ---
if __name__ == "__main__":
    # Datos de nacimiento del ejemplo: 14 de Noviembre de 1948 a las 21h 14m 39s GMT
    año = 1948
    mes = 11
    dia = 14
    hora_gmt = 21 + 14 / 60.0 + 39 / 3600.0  # 21.24416

    # Valores hipotéticos para el arco de dirección (A) y Longitud (PL)
    # (Nota: Reemplaza estos valores con tus datos reales de cartas astronómicas)
    #arco_direccion = 16.1
    arco_direccion = 45.54
    ra_sol_natal = 230.1

    año = 1976
    mes = 12
    dia = 26
    hora_gmt = 17 + 39 / 60.0 + 42 / 3600.0

    arco_direccion = 12.279
    ra_sol_natal = 275.554

    pr = arco_direccion + ra_sol_natal
    longitud_pl = get_ecliptic_long(pr)
    print(f"parametros RA objeto {ra_sol_natal} arco {arco_direccion} longitud {longitud_pl}")

    print("--- Iniciando algoritmo astronómico ---")
    fecha_operacion = algoritmo_true_solar_arc(año, mes, dia, hora_gmt, ra_sol_natal, arco_direccion, longitud_pl)

    print(fecha_operacion)