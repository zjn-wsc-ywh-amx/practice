import ecdsa
import mykeys
from hashlib import sha1


n = 115792089237316195423570985008687907852837564279074904382605163141518161494337  # 由使用的曲线NIST192p决定
m = b"message"
M = "message"


def attack(M,m,n):
    sk = mykeys.SigningKey.generate(curve=ecdsa.SECP256k1)
    vk = sk.get_verifying_key()
    sig, *K = sk.sign(m)
    r, s, k ,h= K[0]
    e = sha1()
    e.update(M.encode("utf-8"))
    e = e.hexdigest()
    r_ = pow(r, n - 2, n)
    d = ((int(s) * int(k) - int(e, 16)) * int(r_)) % int(n)
    print("Calculated the private key ={}".format(d))
    print(vk.verify(sig, m)[0])



attack(M,m,n)

