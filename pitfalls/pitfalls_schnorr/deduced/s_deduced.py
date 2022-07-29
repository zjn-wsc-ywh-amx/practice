from shnorr import *


m1 = "qsl"
m2 = "lc"

d1,Q1 = key()
d2,Q2 = key()

print("private key1 =",d1)
print("private key2 =",d2)
(r1,s1),k = shnorr_sign(m1,d1)
(r2,s2) =shnorr_sign1(m2,d2,k)


df = (s1-s2+r1*d1)*pow(r2,n-2,n) % n
print("calculated = ",df)
if df == d2:
    print("successfully attack!")

print(shnorr_verify(m1,r1,s1,Q1))
print(shnorr_verify(m2,r2,s2,Q2))