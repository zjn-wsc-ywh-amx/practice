import random
from hashlib import sha256
from pysmx.SM3 import hash_msg
from gmssl import sm2,func

photo = 111

def sign(k,d0,photo):
    seed = str(random.getrandbits(256))
    s = hash_msg(seed)

    if k>0:
        c = sha256()
        c.update(s.encode())
        cc = c.hexdigest()
    else:
        cc = s

    if d0>0:
        p = sha256()
        p.update(s.encode())
        cp = p.hexdigest()
    else:
        cp = s

    for i in range(k-1):
        c = sha256()
        c.update(cc.encode())
        cc = c.hexdigest()
    for i in range(d0-1):
        p = sha256()
        p.update(cp.encode())
        cp = p.hexdigest()
    private_key = '00B9AB0B828FF68872F21A837FC303668428DEA11DCD1B24429D0C99E24EED83D5'
    public_key = 'B9C9A6E04E9C91F7BA880429273747D7EF5DDEB0BB2FF6317EB00BEF331A83081A6994B8993F3F5D6EADDDB81872266C87C018FB4162F5AF347B483E24620207'
    sm2_crypt = sm2.CryptSM2(public_key=public_key, private_key=private_key)
    random_hex_str = func.random_hex(sm2_crypt.para_len)
    sign = sm2_crypt.sign(photo, random_hex_str)
    return cp,cc,sign

def verify(d1,c,p,photo,sign):
    if d1>0:
        c1 = sha256()
        c1.update(p.encode())
        cc1 = c1.hexdigest()
    else:
        cc1 = p
    for i in range(d1-1):
        c1 = sha256()
        c1.update(cc1.encode())
        cc1 = c1.hexdigest()
    private_key = '00B9AB0B828FF68872F21A837FC303668428DEA11DCD1B24429D0C99E24EED83D5'
    public_key = 'B9C9A6E04E9C91F7BA880429273747D7EF5DDEB0BB2FF6317EB00BEF331A83081A6994B8993F3F5D6EADDDB81872266C87C018FB4162F5AF347B483E24620207'
    sm2_crypt = sm2.CryptSM2(public_key=public_key, private_key=private_key)
    if sm2_crypt.verify(sign, photo) and cc1 ==c:
        return True



MDP = [312, 303, 233]

def v(number):
    if number < MDP[2]:
        mdp = MDP[2]
    elif number<MDP[1]:
        mdp=MDP[1]
    else:
        mdp = MDP[0]
    b = number//100
    s = number//10-10*b
    g = number%10
    B = mdp//100
    S = mdp//10-10*B
    G = mdp % 10
    cpb,ccb,signb = sign(B,B-b,photo)
    cps,ccs,signs = sign(S,S-s,photo)
    cpg,ccg,signg = sign(G,G-g,photo)
    return (verify(b,ccb,cpb,photo,signb) and verify(s,ccs,cps,photo,signs) and verify(g,ccg,cpg,photo,signg))

print(v(123))