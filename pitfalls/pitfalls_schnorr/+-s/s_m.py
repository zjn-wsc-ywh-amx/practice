from shnorr import *

m = "qsl"
d,Q = key()
print("private key =",d)
(r,s),k = shnorr_sign(m,d)


print(shnorr_verify(m,r,-s,Q))