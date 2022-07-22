de=[(1,2,3),(2,3,4)]
print(len(de))
print(de.pop(0))
print(de.pop(0))
if len(de) ==0:
    print(1)
import hashlib
def Hash(string1,string2):
    string=str(int(string1,16)+int(string2,16))
    s = hashlib.sha256()
    s.update(string.encode())
    b = s.hexdigest()
    return b
str1="48f133e11aa5a2902a17aa7ad8dbc117be637a02a5d6f594c9fc136b41e97eaf"
str2="a12d31b529df9722185c1382106ab28c4b413d56e10b9e1e9e8eec6cfcb4dd59"
print(Hash(str1,str2))
print(Hash(str2,str1))