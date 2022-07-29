from shnorr import *

m1 = "qsl"
m2 = "lc"
d,Q = key()
print("private key =",d)
(r1,s1),k = shnorr_sign(m1,d)
(r2,s2) =shnorr_sign1(m2,d,k)
df = (s1-s2)*pow(r2-r1,n-2,n) % n
print("calculated = ",df)
if df == d:
    print("successfully attack!")

print(shnorr_verify(m1,r1,s1,Q))
print(shnorr_verify(m2,r2,s2,Q))