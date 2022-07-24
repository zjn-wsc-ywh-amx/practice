# coding:utf-8
# 欧几里得算法求最大公约数
# 椭圆曲线部分参考 https://www.jianshu.com/p/eece4117cb63
import copy
import hashlib
def get_gcd(a, b):
    k = a // b
    remainder = a % b
    while remainder != 0:
        a = b
        b = remainder
        k = a // b
        remainder = a % b
    return b


# 改进欧几里得算法求线性方程的x与y
def get_(a, b):
    if b == 0:
        return 1, 0
    else:
        k = a // b
        remainder = a % b
        x1, y1 = get_(b, remainder)
        x, y = y1, x1 - k * y1
    return x, y


# 返回乘法逆元
def multi_inverse(a, b):
    # 将初始b的绝对值进行保存
    if b < 0:
        m = abs(b)
    else:
        m = b

    flag = get_gcd(a, b)
    # 判断最大公约数是否为1，若不是则没有逆元
    if flag == 1:
        x, y = get_(a, b)
        x0 = x % m  # 对于Python '%'就是求模运算，因此不需要'+m'
        # print(x0) #x0就是所求的逆元
        return x0

    else:
        print("Do not have!")

### y^2=x^3+ax+by mod (mod_value)
def Point_Add(P,Q):
    if P[0] == Q[0]:
        fenzi = (3 * pow(P[0], 2) + a)
        fenmu = (2 * P[1])
        if fenzi % fenmu != 0:
            val = multi_inverse(fenmu, 17)
            y = (fenzi * val) % 17
        else:
            y = (fenzi / fenmu) % 17
    else:
        fenzi = (Q[1] - P[1])
        fenmu = (Q[0] - P[0])
        if fenzi % fenmu != 0:
            val = multi_inverse(fenmu, 17)
            y = (fenzi * val) % 17
        else:
            y = (fenzi / fenmu) % 17

    Rx = (pow(y, 2) - P[0] - Q[0]) % 17
    Ry = (y * (P[0] - Rx) - P[1]) % 17
    return(Rx,Ry)


def Multi(n, point):
    if n == 0:
         return 0
    elif n == 1:
        return point

    t = point
    while (n >= 2):
        t = Point_Add(t, point)
        n = n - 1
    return t

def ECDSA_Sign(m, G, d,k):
    e = Hash(m)
    R = Multi(k, G)   #R=kg
    #print("R",R)
    r = R[0] % mod_value      #r=R[x] mod mod_value
    s = (multi_inverse(k, mod_value) * (e + d * r)) % mod_value
    return r, s

def ECDSA_Verify(m, G, r, s, P):
    e = Hash(m)
    w = multi_inverse(s, mod_value)
    ele1 = (e * w) % mod_value
    ele2 = (r * w) % mod_value
    w = Point_Add(Multi(ele1, G), Multi(ele2, P))
    if (w == 0):
        print('false')
        return False
    else:
        if (w[0] % mod_value == r):
            print("签名验证通过")
            return True
        else:
            print('签名不通过')
            return False

def Hash(string):
    s = hashlib.sha256()
    s.update(string.encode())
    b = s.hexdigest()
    return int(b,16)


def deduce_pubkey(s, r, k, G):
    ele1=multi_inverse((s+r),17)

    ele2=Multi(k,G)

    ele3=Multi(s,G)
    ele4=(ele3[0],(-ele3[1])%17)
    print(ele2,ele4)

    result=Point_Add(ele2,ele4)

    print("根据签名推出公钥",result)

mod_value = 19
a = 2
b = 2
G=[7,1]
k=2
message="hello word"
#print(Point_Add([5,1],G))
#print(Multi(k,G))
d=5
r,s=ECDSA_Sign(message,G,d,k)
P = Multi(d, G)
print("公钥为",P)
#print((r,s))
ECDSA_Verify(message,G,r,s,P)
deduce_pubkey(s,r,k,G)