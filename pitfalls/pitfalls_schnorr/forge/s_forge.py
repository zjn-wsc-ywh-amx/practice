from shnorr import *

m = "qsl"
d,Q = key()
print("private key =",d)
(r,s),k = shnorr_sign(m,d)
k1 = random.getrandbits(256)%n
R = point_mult(G,k1)


print(verify_without_m(R,k1,0,Q))