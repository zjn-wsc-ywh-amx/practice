# coding:utf-8
# 欧几里得算法求最大公约数
# 椭圆曲线部分参考 https://www.jianshu.com/p/eece4117cb63
#https://blog.csdn.net/qq_43339242/article/details/123221091
import copy
import hashlib

p = 0x8542D69E4C044F18E8B92435BF6FF7DE457283915C45517D722EDB8B08F1DFC3
a = 0x787968B4FA32C3FD2417842E73BBFEFF2F3C848B6831D7E0EC65228B3937E498
b = 0x63E4C6D3B23B0C849CF84241484BFE48F61D59A5B16BA06E6E12D1DA27C5249A
Gx =0x421DEBD61B62EAB6746434EBC3CC315E32220B3BADD50BDC4C4E6C147FEDD43D
Gy =0x0680512BCBB42C07D47349D2153B70C4E5D7FDFCBFA36EA1A85841B9E46E09A2
n = 0x8542D69E4C044F18E8B92435BF6FF7DD297720630485628D5AE74EE7C32E79B7
G=(Gx,Gy)
e=(-1,-1)#定义无穷远点
def get_G():
    return G
def get_n():
    return n
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

def tonelli(n, p):
# 勒让德符号
    def legendre(a, p):
        return pow(a, (p - 1) // 2, p)

    assert legendre(n, p) == 1, "不是二次剩余"
    q = p - 1
    s = 0
    while q % 2 == 0:
        q //= 2
        s += 1
    if s == 1:
        return pow(n, (p + 1) // 4, p)
    for z in range(2, p):
        if p - 1 == legendre(z, p):
            break
    c = pow(z, q, p)
    r = pow(n, (q + 1) // 2, p)
    t = pow(n, q, p)
    m = s
    t2 = 0
    while (t - 1) % p != 0:
        t2 = (t * t) % p
        for i in range(1, m):
            if (t2 - 1) % p == 0:
                break
            t2 = (t2 * t2) % p
        b = pow(c, 1 << (m - i - 1), p)
        r = (r * b) % p
        c = (b * b) % p
        t = (t * c) % p
        m = i
    return r
# 返回乘法逆元
def Neg_ele(point):
    return (point[0],p-point[1])
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
        return None
def get_y(x,a,b,p):
        y2=(pow(x,3)+a*x+b)%p
        return tonelli(y2,p)
### y^2=x^3+ax+by mod (mod_value)
def Point_Add(P,Q):
    x1,y1=P
    if P == Q:
        if P==e:
            return e
        k = (3 * x1 * x1 + a) * multi_inverse((2 * y1), p) % p
        # 计算目标点坐标
        x3 = (k * k - x1 - x1) % p
        y3 = (k * (x1 - x3) - y1) % p
    else:
        x2, y2 = Q
        if P==e:
            return Q
        if Q==e:
            return P
        if P[0]==Q[0]:
            return e
        k = (y2 - y1) * multi_inverse((x2 - x1), p) % p
        # 计算目标点坐标
        x3 = (k * k - x1 - x2) % p
        y3 = (k * (x1 - x3) - y1) % p
    return(x3,y3)

def double(Q):
    return Point_Add(Q,Q)
def Multi(k, P):
    if k == 0 or P == e:
        return e
    if k == 1:
        return P
    elif k == 2:
        return double(P)
    elif k == 3:
        return Point_Add(P, double(P))
    elif k & 1 == 0:  # k/2 * P + k/2 * P
        return double(Multi(k >> 1, P))
    elif k & 1 == 1:  # P + k/2 * P + k/2 * P
        return Point_Add(P, double(Multi(k >> 1, P)))