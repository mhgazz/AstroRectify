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
    print(f"\n\n\n\n--- Cálculo de Dirección Regiomontanus generica ---")
    #PMP_s = get_placidus_mund_pos(md_s,sa_s,cuadrt_s,RAMC)
    for aspect_angle in -30,-45,30,45,60,-60:
        print("\n")
        ra_ap = ra_s + aspect_angle
        #ratio,cuadrante_s = get_placidus_ratio(ra)
        cuadrt_s = get_cuadrant(ra_ap,cusps)
        pmp_pa = get_PMP(ad_s,natal_geo_latitude,decl_s,cuadrt_s,RAMC,RAIC,ra_ap)
        print(f"RA sif {ra_s} aspect {aspect_angle} RAap {ra_ap} PMPap {pmp_pa} cuadrante signf {cuadrt_s}")
        #resultado_arco = calcular_arco_placidus(ra_p=ra_p,ad_p=ad_p,ratio=ratio,cuadrante_s=cuadrante_s,RAMC=RAMC,RAIC=RAIC)
        tan_decl = math.tan(math.radians(decl_p))
        tan_phi = math.tan(math.radians(natal_geo_latitude))
        cos_ca = math.cos(math.radians(ASC_OA - pmp_pa))
        a_diff = tan_decl * tan_phi * cos_ca
        print(f"tan_decl {tan_decl} tan_phi {tan_phi} cos_ca {cos_ca} total {a_diff}")
        diff = math.degrees(math.asin(a_diff))
        print(f"ASC AO {ASC_OA} Promittor RA {ra_p} diferencial {diff}")
        resultado_arco = ra_p - diff - pmp_pa
        print(f"{name_p} {aspect_angle} {name_s} Arco de Dirección Calculado: {resultado_arco:.2f}")
