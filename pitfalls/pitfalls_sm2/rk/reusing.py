from sm2 import *

p = 0xFFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF00000000FFFFFFFFFFFFFFFF
a = 0xFFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF00000000FFFFFFFFFFFFFFFC
b = 0x28E9FA9E9D9F5E344D5A9E4BCF6509A7F39789F515AB8F92DDBCBD414D940E93
n = 0xFFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFF7203DF6B21C6052B53BBF40939D54123
G = (0x32C4AE2C1F1981195F9904466A39C9948FE30BBFF2660BE1715A4589334C74C7, 0xBC3736A2F4F6779C59BDCEE36B692153D0A9877CC62A474002DF32E52139F0A0)

M1 = 111
M2 = 222
d,Q = key()
(r,s),k = sm2_sign(M1,G,d,n)
(r2,s2),k2 = sm2_sign1(M2,G,d,n,k)
print(sm2_verify(r,s,M1,Q,n,k,d))
print(sm2_verify(r2,s2,M2,Q,n,k,d))

df = (s-s2)*inverse((s2-s+r2-r),n) %n
if df == d:
    print("siulfhgushuogyehijvhsidf!!!!!!!!!!!!!")