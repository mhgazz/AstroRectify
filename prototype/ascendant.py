import math



"""
Valores tomados de las tablas de casas topocentrias en Astro.com
https://www.astro.com/swisseph/sweph_ht_e.htm
Lat 32s
Sid.Time: 19h56m 
ARMC: 299°00'

Topocentrico
MC        XI     XII    Asc    II    III
26Cp57'23 29Aq21 29Pc05 24Ar46 23Ta20 24Gm21

Placidus
MC        XI     XII    Asc    II    III
26Cp57'23 29Aq22 29Pc05 24Ar46 23Ta18 24Gm18
"""
AOs=[29.602,29.6772,2.13694]
L_gs= [32.95,32.95,3.45]
E=23.44
ARMCs=[299.602222,299.6772,272.13694]
x = len(AOs)

for i in range(x):
    print("----" + str(i) + "----")
    ao   = AOs[i]
    ARMC = ARMCs[i]
    L_g  = L_gs[i]
    cos_E  = math.cos(math.radians(E))
    sen_E  = math.sin(math.radians(E))
    tag_E  = math.tan(math.radians(E))
    cos_AO = math.cos(math.radians(ao))
    tag_AO = math.tan(math.radians(ao))
    sin_AO = math.sin(math.radians(ao))
    tan_Lg = math.tan(math.radians(L_g))
    sen_ARMC = math.sin(math.radians(ARMC))
    cos_ARMC = math.cos(math.radians(ARMC))

    L=((cos_AO + (tan_Lg * tag_E)) / sin_AO) * cos_E
    L_asc = math.atan(L)
    deg_L_asc = math.degrees(L_asc)
    print(L_asc)
    print(deg_L_asc)


    L_asc = math.atan(+1 * ((tan_Lg + sen_E) + (sen_ARMC * cos_E))/cos_ARMC)
    deg_L_asc = math.degrees(L_asc)
    print(L_asc)
    print(deg_L_asc)


#tmp  = -1 * (math.tan(math.radians(L)) * tag_E) + (math.sin(math.radians(ARMC))*cos_E)
#tmp2 = 1/(math.atan(math.cos(math.radians(ARMC))))

