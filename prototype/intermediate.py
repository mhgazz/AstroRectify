import math

"""
Topocentrico
MC        XI     XII    Asc    II    III
26Cp57'23 29Aq21 29Pc05 24Ar46 23Ta20 24Gm21
Placidus
MC        XI     XII    Asc    II    III
26Cp57'23 29Aq22 29Pc05 24Ar46 23Ta18 24Gm18
"""

def get_ecliptic_longitude(ar:float):
    """ convert a AR value to ecliptic longitude"""
    E: float = 23.43
    tang_ar = math.tan(math.radians(ar))
    dec_cos = math.cos(math.radians(E))
    tmp = tang_ar/dec_cos
    temp2 = math.atan(tmp)
    ecliptic_longitude = math.degrees(temp2)
    if ar >270:
        ecliptic_longitude = ecliptic_longitude + 360
    elif ar >=180:
        ecliptic_longitude = ecliptic_longitude + 180
    elif ar >=90:
        ecliptic_longitude = 180 + ecliptic_longitude
    return ecliptic_longitude

def get_declination(long_ecep:float,E:float,latitude:float):
    sen_E = math.sin(math.radians(E))
    cos_E = math.cos(math.radians(E))
    sen_Lat = math.sin(math.radians(latitude))
    cos_Lat = math.cos(math.radians(latitude))
    sen_L = math.sin(math.radians(long_ecep))
    dec = math.degrees(math.asin(sen_E * sen_L))
    #δ=arcsin(sinβ * cosε + cosβ * sinε * sinλ)
    #dec = math.degrees (math.asin( (sen_Lat * cos_E) + (cos_Lat * sen_E * sen_L) ))
    #print("long_ecep " + str(long_ecep))
    #print("dec " + str(dec))
    return dec


def main():
    #RAMC = 276.25138
    RAMC = 12.238
    #RAMC = 113.483
    #polo_ASC = 53.4
    #polo_ASC = 42.3
    polo_ASC = 51.5
    E = 23.445
    latitude = polo_ASC
    # δ = arcsin(sinβ * cosε + cosβ * sinε * sinλ)

    polo_XI_III = math.degrees(math.atan(1/3 * math.tan(math.radians(polo_ASC))))
    print ("polo XI_III  " + str(polo_XI_III)) 
    polo_XII_II = math.degrees(math.atan(2/3 * math.tan(math.radians(polo_ASC))))
    print ("polo XII_II " + str(polo_XII_II)) 
    polo_ASC = math.degrees(math.atan(1 * math.tan(math.radians(polo_ASC))))
    print ("polo ASC " + str(polo_ASC)) 


    OAs = [RAMC+30,RAMC+60,RAMC+90,RAMC+120,RAMC+150]
    polos = [polo_XI_III,polo_XII_II,polo_ASC,polo_XII_II,polo_XI_III]
    
    for i in range(len(OAs)):
        geodetic_latitude = polos[i]
        oa = OAs[i]
        
        #long_ecep = math.degrees(math.atan(math.tan(math.radians(oa))/math.cos(math.radians(E))))
        long_ecep = get_ecliptic_longitude(oa)
        obliquity = E
        etanz = math.tan(math.radians(obliquity)) * math.tan(math.radians(geodetic_latitude))
        
        if oa>=360:
            oa=oa-360
        ra = oa # (=>1st appoximation)
        it=0
        print(" ")
        print("--------" + str(i+1) + "--------")
        print("polo :" + str(geodetic_latitude))
        print ("ascencion recta inicial " + str(oa) )
        while True:
            ra1 = ra
            ad = math.asin ( etanz * math.sin( math.radians(ra1 ) ))
            ra = oa + math.degrees ( ad / 3 )
            #print(ra1-ra)
            if abs( ra1 - ra ) < 1e-7:
                break
            it=it+1

        # alexander marr's formula
        sen_e=  math.sin(math.radians(obliquity))
        print("sen_e " + str(sen_e))
        cos_e=  math.cos(math.radians(obliquity))
        print("cos_e " + str(cos_e))
        phi=    math.tan(math.radians(geodetic_latitude))
        print("phi " + str(phi))
        sen_oa= math.sin(math.radians(oa))
        print("sen_oa " + str(sen_oa))
        cos_oa= math.cos(math.radians(oa))
        print("cos_oa " + str(cos_oa))
        par = ((sen_e * phi) - (cos_e * cos_oa)) / sen_oa
        print("par " + str(par))
        cusp=   math.degrees(math.atan(par))
        print("cusp " + str(cusp))
        if oa >=180:
            cusp=cusp+270
        else:
            cusp=cusp+90
            
        #ecliptic = math.degrees(math.atan(math.tan(math.radians(ra))/math.cos(math.radians(E))))
        ecliptic = get_ecliptic_longitude(ra)
        print ("declinacion " + str(obliquity))
        print ("ascencion recta final " + str(ra) )
        print ("ecliptica       " + str(ecliptic ))
        print ("iteraciones     " + str(it ))
        print ("alex marr's: " + str(cusp))

if __name__ == "__main__":
    main()
