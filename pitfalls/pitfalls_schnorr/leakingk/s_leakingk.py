from shnorr import *

m = "qsl"
d,Q = key()
print("private key =",d)
(r,s),k = shnorr_sign(m,d)
df = ((k-s)*pow(r,n-2,n)) % n
print("calculated = ",df)
if df == d:
    print("successfully attack!")

print(shnorr_verify(m,r,s,Q))

