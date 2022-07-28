import  ECC
import random
import hashlib
def init():
    n=ECC.get_n()
    return (n,ECC.get_G(),random.randrange(1, n),random.randrange(1, n),random.randrange(1, n))
#n,G,d2,k2,k3
def Gen_pk(d2,P1,G,n):
    id2=ECC.multi_inverse(d2,n)
    G_ne=ECC.Neg_ele(G)
    pk=ECC.Point_Add(ECC.Multi(id2,P1),G_ne)
    print("public key:", pk)
    return pk
def Gen_r(d2,k2,k3,Q1,e,n,G):
    Q2=ECC.Multi(k2,G)
    x1,y1=ECC.Point_Add(ECC.Multi(k3,Q1),Q2)
    r=(x1+e)%n
    s2=(d2*k3)%n
    s3=(d2*(r+k2))%n
    return (r,s2,s3)

