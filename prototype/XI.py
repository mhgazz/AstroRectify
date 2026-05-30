import math


def get_ecliptic_longitude(ar:float):
    """ convert a AR value to ecliptic longitude"""
    declination: float = 23.44
    tang_ar = math.tan(math.radians(ar))
    dec_cos = math.cos(math.radians(declination))
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

"""
Topocentrico
MC        XI     XII    Asc    II    III
26Cp57'23 29Aq21 29Pc05 24Ar46 23Ta20 24Gm21
Placidus
MC        XI     XII    Asc    II    III
26Cp57'23 29Aq22 29Pc05 24Ar46 23Ta18 24Gm18
"""

def main():
    RAMC = 299.5
    polo_ASC = 32.95
    E = 23.4333
    polo_XI_III = math.degrees(math.atan(1/3 * math.tan(math.radians(polo_ASC))))
    print ("polo XI_III  " + str(polo_XI_III)) 
    polo_XII_II = math.degrees(math.atan(2/3 * math.tan(math.radians(polo_ASC))))
    print ("polo XII_II  " + str(polo_XII_II)) 
    oa = RAMC + 30
    if oa > 360:
        oa = oa - 360
    P  = polo_XI_III

    #etanz = tan (obliquity) * tan (geodetic latitude)

    sen_E = math.sin(math.radians(E))
    sen_L = math.sin(math.radians(oa))
    obliquity = math.degrees(math.asin(sen_E * sen_L))
    etanz =  math.tan(math.radians(obliquity)) * math.tan(math.radians(P)) 

    #a = math.tan(math.radians(oa)) * math.cos(math.radians(E))
    #b = math.cos(math.radians(P)) - ( math.sin(math.radians(P)) * math.tan(math.radians(-60) * math.sin(math.radians(E))))
    #    c = math.degrees( math.atan(a/b))
    #print ("c " + str(c) )
    
    ra = oa #(=>1st appoximation)
    while True:
        ra1 = ra
        #ad = arcsin ( etanz * Sin ( ra1 ) )
        ad = math.degrees(math.asin( etanz * math.sin( math.radians(ra1 ) )))
        #ad = math.asin( math.tan(math.radians(P)) * math.tan(math.radians(obliquity)) )
        ra = oa + ( ad / 3 )
        print(ra1,ra,ra1 - ra)
        if abs( ra1 - ra ) < 1e-011:
            break
    # cusp = simple conversion of right ascension ra to ecliptic
    ecliptic = get_ecliptic_longitude(ra)
    print("ecliptica " + str(ecliptic ))

if __name__ == "__main__":
    main()


    