import ecdsa
from hashlib import sha1
import mykeys
import mykeys3

sk1 = mykeys.SigningKey.generate(curve=ecdsa.SECP256k1)
vk1 = sk1.get_verifying_key()
sk2 = mykeys3.SigningKey.generate(curve=ecdsa.SECP256k1)
vk2 = sk2.get_verifying_key()
m1 = b"message"
m2 = b"agsjgusjkr"
M1 = "message"
M2 = "agsjgusjkr"
n = 115792089237316195423570985008687907852837564279074904382605163141518161494337#由使用的曲线NIST192p决定

sig1,*R1 = sk1.sign(m1)
r1,*s1 = R1[0]
k1=s1[1]
d=s1[2]
#print("k1=",k1)
sig2,*R2 = sk2.sign(m2,k1,d)
r2,*s2 = R2[0]


e1 = sha1()  #创建sha1加密对象
e1.update(M1.encode("utf-8"))   #转码（字节流）
e1 = int(e1.hexdigest(),16)

e2 = sha1()
e2.update(M2.encode("utf-8"))
e2 = int(e2.hexdigest(),16)


#print(s1[0],s2[0])

#print(s1[0],s2[0])
#print(pow(s1[0]-s2[0],n-2,n))
k = ((e1-e2)*(pow((s1[0]-s2[0]),n-2,n))) % n
#print("calculate:",k)

r_1 = pow(r1, n - 2, n)
d1 = ((s1[0] * int(k) - e1) * int(r_1)) % int(n)
print("Calculated the private key ={}".format(d1))
r_2 = pow(r2, n - 2, n)
d2 = ((s2[0] * int(k) - e2) * int(r_2)) % int(n)
print("Calculated the private key ={}".format(d2))

if d1==d2==d:
    print("successfully calculate!")
