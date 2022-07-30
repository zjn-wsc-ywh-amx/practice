import random
from pysmx.SM3 import hash_msg
from crypto.Util.number import *

p = 0xFFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF00000000FFFFFFFFFFFFFFFF
a = 0xFFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF00000000FFFFFFFFFFFFFFFC
b = 0x28E9FA9E9D9F5E344D5A9E4BCF6509A7F39789F515AB8F92DDBCBD414D940E93
n = 0xFFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFF7203DF6B21C6052B53BBF40939D54123
G = (0x32C4AE2C1F1981195F9904466A39C9948FE30BBFF2660BE1715A4589334C74C7, 0xBC3736A2F4F6779C59BDCEE36B692153D0A9877CC62A474002DF32E52139F0A0)
ID = [0x31, 0x32, 0x33, 0x34, 0x35, 0x36, 0x37, 0x38, 0x31,0x32, 0x33, 0x34, 0x35, 0x36, 0x37, 0x38]

def key():
    d = random.getrandbits(256) % n
    Q = point_mult(G,d)
    return (d,Q)

def precom(ID,a,b,G,Q):
    byte = b""
    for i in ID:
        byte+=bytes(str(i).encode())
    byte += bytes(str(a).encode())
    byte += bytes(str(b).encode())
    byte += bytes(str(G[0]).encode())
    byte += bytes(str(G[1]).encode())
    byte += bytes(str(Q[0]).encode())
    byte += bytes(str(Q[1]).encode())
    long = bytes_to_long(byte)
    l = str(long)
    za = hash_msg(l)
    return za


def point_add(p1,p2):
    if(p1 == None or p2 == None):
        if p1 == None:
            return p2
        else:
            return p1
    if(p1[0] == p2[0] and p1[1]!= p2[1]):
        return None
    if(p1 == p2):
        lamb = ((3*(p1[0]**2)+a)*inverse(2*p1[1],p)) % p
    else:
        lamb = ((p2[1]-p1[1])*inverse(p2[0]-p1[0],p))% p
    x = (lamb**2-p2[0]-p1[0]) %p
    y = (lamb*(p1[0]-x)-p1[1]) %p
    return(x,y)


def point_mult(Q,m):
    m = bin(m)[2:]
    G = Q
    for i in range(1, len(m)):
        Q = point_add(Q, Q)
        if m[i] == '1':
            Q= point_add(Q, G)
    return Q



def sm2_sign(za,M,G,d,n):
    M = str(M)
    m = M + str(za)
    e = hash_msg(str(m))
    e = int(e,16)


    k = random.getrandbits(256) % n
    P1= point_mult(G,k)
    #print(P1)
    x1 = int(P1[0])
    r = (e+x1) % n

    if(r==0 or r+k ==n):
        return None
    c = (k-r*d+n)
    s = (inverse(d+1, n) * c) % n
    if s==0:
        return None
    return (r,s),k



def sm2_verify(za,r,s, m,Q,n,k,d):
    m = str(m)
    print(za)
    m = m + str(za)
    e = hash_msg(str(m))
    e = int(e, 16)

    t = (r + s) % n

    if t == 0:
        return None

    P1 = point_mult(G,s)
    P2 = point_mult(Q,t)
    G1 = point_add(P1,P2)
    #print(G1)


    x = G1[0]
    return (r == ((e + x) % n))



