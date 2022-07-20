import hashlib
import ecdsa
import random

import numpy as np

def gcd(a, b):
    while a != 0:
        a, b = b % a, a
    return b


# 定义一个函数，参数分别为a,n，返回值为b
def inverse(a, m):  # 这个扩展欧几里得算法求模逆

    if gcd(a, m) != 1:
        return None
    u1, u2, u3 = 1, 0, a
    v1, v2, v3 = 0, 1, m
    while v3 != 0:
        q = u3 // v3
        v1, v2, v3, u1, u2, u3 = (u1 - q * v1), (u2 - q * v2), (u3 - q * v3), v1, v2, v3
    return u1 % m

def sign(e, k, d, P, p):    # e: H(message)  k randomly chosen 0 < k < q
    Q = k*P
    s = np.mod(inverse(k, p)*(e + d*Q.x), p)
    return s, Q.x


def verify(e, s, r, G, P, p):
    Q1 = np.mod(e*inverse(s, p), p)*G
    Q2 = np.mod(r*inverse(s, p), p)*P
    R = Q1+Q2
    if R.x == r:
        return True, R.x
    return False, R.x


gen = ecdsa.NIST256p.generator


order = gen.order()
# 生成私钥d_A
d_A = random.randrange(1,order-1)
# 生成公私钥对象
print("d_A",d_A)
#生成公钥
public_key = ecdsa.ecdsa.Public_key(gen,gen * d_A)
private_key = ecdsa.ecdsa.Private_key(public_key,d_A)

message = "message"
m = int(hashlib.sha1(message.encode("utf8")).hexdigest(),16)


# 临时密钥
k = random.randrange(1,order-1)


# 签名
#signature = private_key.sign(m,k)
#r = signature.r
#s = signature.s
#print(r,s)


F = GF (0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F)  #生成一个给定阶数的全局唯一有限域
C = EllipticCurve ([F (0), F (7)])     #构造出椭圆曲线


G = C.lift_x(0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798)
N = GF (C.order())
P = P=-C.lift_x(0x11db93e1dcdb8a016b49840f8c53bc1eb68a382e97b1482ecad7b148a6909a5c) # block 9 coinbase payout key.

def forge(c, a=-1):  # Create a forged 'ECDSA'  (hashless) signature
  # set a to something other than -1 to be less obvious
  a = N(a)
  R = c*G + int(a)*P
  s = N(int(R.xy()[0]))/a
  m = N(c)*N(int(R.xy()[0]))/a
  print ('hash1 = %d'%m)
  print ('r1 = %d'%(int(R.xy()[0])))
  print ('s1 = %d'%s)
def verify():
    pass
for c in range(1,10):
  forge(c)