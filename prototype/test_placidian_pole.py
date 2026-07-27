from utils import get_placidus_pole

d_m      = 4.79
s_arc    = 105.4
cuadrant = 3
decl     = -21.82
a_d      = 15.4

phi = get_placidus_pole(d_m,s_arc,cuadrant,decl,a_d)
print(f"phi {phi}")