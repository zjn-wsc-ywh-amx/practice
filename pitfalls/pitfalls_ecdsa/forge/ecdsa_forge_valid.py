import ecdsa
import mykeys
import myecdsa

sk = mykeys.SigningKey.generate(curve=ecdsa.SECP256k1)
vk = sk.get_verifying_key()
m = b"message"
M = "message"
n = 115792089237316195423570985008687907852837564279074904382605163141518161494337#由使用的曲线NIST192p决定

sig,*R1 = sk.sign(m)
r,*s1 = R1[0]
s = s1[0]
k1=s1[1]
d=s1[2]
# sig =


sig0 = myecdsa.Signature(r,-s)
sig1 = ecdsa.util.sigencode_string(sig0.r,sig0.s,n)

print(vk.verify(sig1, m)[0])
