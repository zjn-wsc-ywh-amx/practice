import random
import hashlib

p = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F
n = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141
G = (0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798, 0x483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8)

def point_add(p1,p2):
    if(p1 == None or p2 == None):
        if p1 == None:
            return p2
        else:
            return p1
    if(p1[0] == p2[0] and p1[1]!= p2[1]):
        return None
    if(p1 == p2):
        lamb = (3*(p1[0]**2)*pow(2*p1[1],p-2,p)) % p
    else:
        lamb = ((p2[1]-p1[1])*pow((p2[0]-p1[0])+p,p-2,p))% p
    x = (lamb**2-p2[0]-p1[0]) %p
    y = (lamb*(p1[0]-x)-p1[1]) %p
    return(x,y)


def point_mult(Q,m):
    R = None
    m = abs(m)
    while m != 0:
        if m & 1:
            R = point_add(R, Q)
        m = m >> 1
        if (m != 0):
            Q = point_add(Q,Q)
    return R

def hashcon(M,C):
    hash=hashlib.sha256()
    hash.update(M.encode())
    hash.update(str(C).encode())
    return int(hash.hexdigest(),16)

def key():
    d = random.getrandbits(256) % n
    Q = point_mult(G,d)
    return (d,Q)

def shnorr_sign(m,d):
    k = random.getrandbits(256)%n
    R = point_mult(G,k)
    r = hashcon(m,R)
    s = (k - r * d) % n
    return (r,s),k

def shnorr_sign1(m,d,k):
    R = point_mult(G,k)
    r = hashcon(m,R)
    s = (k - r * d) % n
    return (r,s)

def shnorr_verify(m,r,s,Q):
    v = point_mult(G,s)
    H = point_mult(Q,r)
    V = point_add(v,H)
    Rv = hashcon(m,V)
    return Rv == r


def verify_without_m(R,r,s,Q):
    print(r)
    sigma = point_mult(G,r)
    alpha = point_mult(Q,s)
    y = point_add(sigma,alpha)
    return R == y


