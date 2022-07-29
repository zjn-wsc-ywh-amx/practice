from shnorr import *

M1 = "m1"
M2 = "m2"
M_ = "m_"

def generate():
    d1,Q1 = key()
    d2,Q2 = key()

    (r1,s1) = shnorr_sign(M1,d1)
    (r2,s2) = shnorr_sign(M2,d2)

    c1 = (r1,s1)
    c2 = (r2,s2)

    sig = {M1:c1,M2:c2}
    return sig

def cal(sig):
    r_ = sig[M1][0]*sig[M2][0] % n
    e_,e1,e2=hashlib.sha256()
    e_ = e_.update(str(r_).encode())
    e_ = e_.update(M_.encode())
    e1 = e1.update(str(sig[M1][0].encode()))
    e1 = e1.update(M1.encode())
    e2 = e2.update(str(sig[M2][0].encode()))
    e2 = e2.update(M2.encode())
    return e_,e1,e2

def judge(e_,e1,e2,sig):
    if e_% n == (e1+e2) % n:
        s_ = sig[M1][1]+sig[M2][1] %n
    return s_

