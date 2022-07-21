de=[(1,2,3),(2,3,4)]
print(len(de))
print(de.pop(0))
print(de.pop(0))
if len(de) ==0:
    print(1)
import hashlib
def Hash(string):
    s = hashlib.sha256()
    s.update(string.encode())
    b = s.hexdigest()
    return b
