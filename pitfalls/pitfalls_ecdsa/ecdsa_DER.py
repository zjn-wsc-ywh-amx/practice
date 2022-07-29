import ecdsa.der
import mykeys
#import myecdsa
import binascii


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
r_ = ecdsa.der.encode_integer(r)
s_ = ecdsa.der.encode_integer(s)




b = '00'
b_ = binascii.unhexlify(b)
#print(b_)
#print("sig=",sig)
sig1 = b_ + sig
#print(sig1)


#print(vk.verify(sig1, m)[0])