import myecdsa4
import curves
import random
import olll

#创建曲线
gen = curves.NIST256p.generator
order = gen.order()
secret = random.randrange(1,order)

#制作签名
pub_key = myecdsa4.Public_key(gen, gen * secret)
priv_key = myecdsa4.Private_key(pub_key, secret)
nonce1 = random.randrange(1, 2**127)
nonce2 = random.randrange(1, 2**127)
msg1 = random.randrange(1, order)
msg2 = random.randrange(1, order)
sig1,t1 = priv_key.sign(msg1, nonce1)
sig2,t2 = priv_key.sign(msg2, nonce2)

#构造矩阵
r1 = t1[1]
s1_inv = pow(t1[2],order-2, order)
r2 = t2[1]
s2_inv = pow(t2[2],order-2, order)
matrix = [[order, 0, 0, 0], [0, order, 0, 0],
[r1*s1_inv, r2*s2_inv, (2**128) / order, 0],
[msg1*s1_inv, msg2*s2_inv, 0, 2**128]]

#格基约化计算
new_matrix = olll.reduction(matrix, 0.75)
r1_inv = pow(sig1.r, order-2,order)
s1 = t1[2]
for row in new_matrix:
    potential_nonce_1 = row[0]
    potential_priv_key = r1_inv * ((potential_nonce_1 * s1) - msg1)

    #检查是否攻击成功
    if myecdsa4.Public_key(gen, gen * potential_priv_key) == pub_key:
        print( "found private key!")