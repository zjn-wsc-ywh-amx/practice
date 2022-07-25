import ECDSA_Deduce_publickey.main
mod_value = 19
a = 2
b = 2
G=[7,1]
k=2
d=5
message="hello word"
r,s=ECDSA_Deduce_publickey.main.ECDSA_Sign(message,G,d,k)
P = ECDSA_Deduce_publickey.main.Multi(d, G)
#print("公钥为",P)
print("签名",(r,s))
ECDSA_Deduce_publickey.main.ECDSA_Verify(message,G,r,s,P)
def leaking_k(r,s,k):
  e=ECDSA_Deduce_publickey.main.Hash(message)
  ele1=ECDSA_Deduce_publickey.main.multi_inverse(r,mod_value)
  ele2=(k*s-e)%mod_value

  return (ele1*ele2)%mod_value
#print(Point_Add([5,1],G))
#print(Multi(k,G))
d=5
print("泄露k，计算出私钥为",leaking_k(r,s,k))