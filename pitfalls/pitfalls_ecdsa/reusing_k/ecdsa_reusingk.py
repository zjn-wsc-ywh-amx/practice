import ecdsa
from hashlib import sha1
from ecdsa.util import bit_length
import mykeys2

sk1 = mykeys2.SigningKey.generate(curve=ecdsa.SECP256k1)
vk1 = sk1.get_verifying_key()

m1 = b"message"
m2 = b"agsjgusjkr"
M1 = "message"
M2 = "agsjgusjkr"
n = 115792089237316195423570985008687907852837564279074904382605163141518161494337#由使用的曲线NIST192p决定
k1 = 17974378272343640558356421156198842709697181676928762395882995871818944028373
sig1,*R1 = sk1.sign(m1,k1)
r1,*s1 = R1[0]

sig2,*R2 = sk1.sign(m2,k1)
r2,*s2 = R2[0]

print("k1=",k1)

e1 = sha1()  #创建sha1加密对象
e1.update(M1.encode("utf-8"))   #转码（字节流）
e1 = e1.hexdigest()

e2 = sha1()
e2.update(M2.encode("utf-8"))
e2 = e2.hexdigest()


L = bit_length(n)

e1 = bin(int(e1,16))
e2 = bin(int(e2,16))

z1 = int(e1[2:L],2)
z2 = int(e2[2:L],2)
#print(vk1.verify(sig1, m1))
#print(z1)

#print(pow(s1[0]-s2[0],n-2,n))
k = ((z1-z2)*(pow((s1[0]-s2[0]),n-2,n))) % n
print("calculate k:",k)

if k== k1:
    print("successfully calculate k")


r_1 = pow(r1, n - 2, n)
d1 = ((s1[0] * k - int(e1,2)) * int(r_1)) % int(n)
print("Calculated the private key ={}".format(d1))

