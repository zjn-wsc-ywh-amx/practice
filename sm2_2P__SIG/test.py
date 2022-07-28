
#没有网络环境的测试版
import  ECC
import random
import hashlib
import sig_partone as s1
import sig_partwo as s2
def sig_verify(M,sig,pk,n,G):
    r,s=sig
    e =int(hashlib.sha256(M.encode('utf-8')).hexdigest(),16)
    print(hex(e))
    t=(r+s)%n
    x,y=ECC.Point_Add(ECC.Multi(s,G),ECC.Multi(t,pk))
    R=(e+x)%n
    if R==r:
        return True
    else:
        return False

n,G,d1,k1=s1.init()
print("d1:   ",d1)
f,q,d2,k2,k3=s2.init()
print("d2:   ",d2)
P1=s1.geneP1(d1=d1,G=G,n=n)
pk=s2.Gen_pk(d2=d2,P1=P1,G=G,n=n)
M="hello"
Z="1234"
Q1,e=s1.genQe(k1=k1,G=G,M=M,Z=Z)
r,s2,s3=s2.Gen_r(d2=d2,k2=k2,k3=k3,Q1=Q1,e=e,n=n,G=G)
sig=s1.Gen_sig(r=r,s2=s2,s3=s3,d1=d1,k1=k1,n=n)
print(sig_verify(Z+M,sig,pk,n,G))