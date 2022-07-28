import  ECC
import random
import json
import hashlib

def init():#n,G,d1,k1
    n=ECC.get_n()
    return (n,ECC.get_G(),random.randrange(1, n),random.randrange(1, n))

def geneP1(d1,G,n):
    i=ECC.multi_inverse(d1,n)
    return ECC.Multi(i,G)
def genQe(Z:str,M:str,k1,G):
    M1=Z+M
    e=hashlib.sha256(M1.encode('utf-8')).hexdigest()
    #print("e",e)
    Q1=ECC.Multi(k1,G)
    return (Q1,int(e,16))
def Gen_sig(r,s2,s3,d1,k1,n):
    s=((d1*k1)*s2+(d1*s3)-r)%n
    if s!=0 or s!=n-r:
        #print("signature :",(r,s))
        return (r,s)
    else:
        print("error")
        return -1
