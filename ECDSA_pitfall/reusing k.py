import ECDSA_Deduce_publickey.main
def reusing_k(r1,s1,r2,s2):
    e1=ECDSA_Deduce_publickey.main.Hash(message)
    e2=ECDSA_Deduce_publickey.main.Hash(message2)
    d=(s1*e2-s2*e2)*ECDSA_Deduce_publickey.main.multi_inverse((s2 * r1 - s1 * r2),mod_value)%mod_value
    return d
mod_value = 19
a = 2
b = 2
G=[7,1]
k=2
d=5
message="hello world"
message2="bad world"
r,s=ECDSA_Deduce_publickey.main.ECDSA_Sign(message,G,d,k)
r2,s2=ECDSA_Deduce_publickey.main.ECDSA_Sign(message,G,d,k)
P = ECDSA_Deduce_publickey.main.Multi(d, G)
#print("公钥为",P)
print("签名",(r,s))

ECDSA_Deduce_publickey.main.ECDSA_Verify(message,G,r,s,P)
print(reusing_k(r,s,r2,s2))
