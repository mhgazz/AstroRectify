import math

from utils import get_d_a
from utils import get_cuadrant
from utils import get_d_m
from utils import get_placidus_mund_pos
from utils import get_PMP


def get_placidus_ratio(PMP_pa: float):
    """ calculate placidus ratio and cuadrant for PMP pa"""
    ratio: float = 0
    cuadrt: int = 0
    if 0 <= PMP_pa and PMP_pa < 90:
        ratio = 1 - (PMP_pa / 90)
        cuadrt = 1
    elif 90 <= PMP_pa and PMP_pa < 180:
        ratio = (PMP_pa / 90) - 1
        cuadrt = 2
    elif 180 <= PMP_pa and PMP_pa < 270:
        ratio = 3 - (PMP_pa / 90)
        cuadrt = 3
    elif 270 <= PMP_pa and PMP_pa < 360:
        ratio = (PMP_pa / 90) - 3
        cuadrt = 4
    return ratio,cuadrt

def calcular_arco_placidus(ra_p, ad_p, ratio, cuadrante_s,RAMC,RAIC):
    """
    Calcula el arco de dirección mundana según el método Placidus.

    Parámetros:
    ra_p        : Ascensión Recta del promisor (RA_P) en grados.
    ad_p        : Diferencia Ascensional del promisor (AD_P) en grados.
    md_s        : Distancia Meridiana del significador (MD_S) en grados.
    sa_s        : Semi-arco del significador (SA_S) en grados.
    cuadrante_s : Cuadrante del significador (1, 2, 3 o 4).
    """
    # 1. Determinar el valor de tau según el cuadrante del significador
    if cuadrante_s in [1, 3]:
        tau = 1
    elif cuadrante_s in [2, 4]:
        tau = -1
    else:
        raise ValueError("El cuadrante debe ser un entero entre 1 y 4.")

    # 2. Determinar el valor de v según el cuadrante del significador
    R = 0
    if cuadrante_s in [1, 2]:
        v = -1
        R = RAIC
        # Nota: En un cálculo real completo, aquí se usaría RA_IC
    elif cuadrante_s in [3, 4]:
        v = 1
        R = RAMC
        # Nota: En un cálculo real completo, aquí se usaría RA_MC

    # Marcador de posición para R según la lógica del algoritmo provisto
    # En el ejemplo del texto, se utiliza un valor de referencia R
    # Para replicar el ejemplo exacto, asumimos que la fórmula se evalúa como:
    # Arc = RA_P + tau * (90 + v * AD_P) * (MD_S / SA_S)

    # 3. Calcular la proporción del significador
    #proporcion_s = md_s / sa_s

    # 4. Calcular el arco de dirección
    # Modificamos la estructura para que coincida exactamente con el comportamiento del ejemplo:
    factor_semiarco = 90 + (v * ad_p)
    #arco = ra_p + (tau * factor_s   emiarco * proporcion_s)
    arco = ra_p - R + (tau * factor_semiarco * ratio)

    return arco


# --- Ejecución del Ejemplo: Sol Conjunción Mercurio (SU CONJ ME) ---
if __name__ == "__main__":
    print("\n\n\n")
    # Datos extraídos del ejemplo del texto:

    natal_geo_latitude = -32.95
    RAMC = 299.6772
    ASC_OA = RAMC + 90
    if ASC_OA > 360:
        ASC_OA = ASC_OA - 360
    ASC = 23.2961
    cusps = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    cusps[1]  = ASC
    cusps[10] = RAMC
    RAIC = RAMC - 180
    if RAIC<0:
        RAIC = RAIC + 360
    cusps[4] = RAIC
    DESC =ASC + 180
    if DESC>360:
        DESC = DESC - 360
    cusps[7] = DESC

    #promitor y signif
    name_p = "Sol"
    ra_p = 275.554
    decl_p = -23.34
    cuadrant_p = get_cuadrant(ra_p,cusps)
    ad_p,sa_p = get_d_a(natal_geo_latitude,decl_p,cuadrant_p)
    name_s = "Marte"
    ra_s =  265.68
    decl_s = -23.95
    name_s = "Mercurio"
    ra_s = 295.03
    decl_s = -21.82
    cuadrt_s = get_cuadrant(ra_s,cusps)
    md_s = get_d_m(ra_s,RAMC,RAIC,cuadrt_s)
    md_p = get_d_m(ra_p,RAMC,RAIC,cuadrant_p)
    ad_s,sa_s = get_d_a(natal_geo_latitude,decl_s,cuadrt_s)
    ratio = md_s / sa_s

    print(f"promitor {name_p} RA {ra_p}")
    print(f"promitor Diferencia ascencional {ad_p}")
    print(f"promitor Semi-arco {sa_p}")
    print(f"promitor distancia meridiana {md_p}")
    print(f"promitor cuadrante {cuadrant_p}")
    print(f"signif {name_s} RA {ra_s}")
    print(f"signif Diferencia ascencional {ad_s}")
    print(f"signif Semi-arco {sa_s}")
    print(f"signif distancia meridiana {md_s}")
    print(f"signif ratio {ratio}")
    print(f"signif cuadrante {cuadrt_s}")


    # Cálculo del arco
    print(f"\n--- Cálculo de Dirección Placidus Mundana semiarco ---")
    for aspect_angle in 0,-30,-45,30,45,60,-60:
        pmp=get_placidus_mund_pos(md_s,sa_s,cuadrt_s,RAMC)
        ra_ap = pmp + aspect_angle
        ratio,cuadrante_s = get_placidus_ratio(ra_ap)
        resultado_arco = calcular_arco_placidus(
            ra_p=ra_p,
            ad_p=ad_p,
            ratio=ratio,
            cuadrante_s=cuadrante_s,
            RAMC=RAMC,
            RAIC=RAIC)
        print(f"{name_p} aspecto {aspect_angle} {name_s} pmp {pmp} ratio {ratio} Arco de Dirección Calculado: {resultado_arco:.2f}°")

   