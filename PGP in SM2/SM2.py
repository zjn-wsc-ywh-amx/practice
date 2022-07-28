import random
import time
import math
import numpy as np
from pysmx.SM3 import digest as sm3
 
# 小素数列表，加快判断素数速度
small_primes = np.array([2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41,
                         43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109,
                         113, 127, 131, 137, 139, 149, 151, 157, 163, 167, 173, 179, 181, 191,
                         193, 197, 199, 211, 223, 227, 229, 233, 239, 241, 251, 257, 263, 269,
                         271, 277, 281, 283, 293, 307, 311, 313, 317, 331, 337, 347, 349, 353,
                         359, 367, 373, 379, 383, 389, 397, 401, 409, 419, 421, 431, 433, 439,
                         443, 449, 457, 461, 463, 467, 479, 487, 491, 499, 503, 509, 521, 523,
                         541, 547, 557, 563, 569, 571, 577, 587, 593, 599, 601, 607, 613, 617,
                         619, 631, 641, 643, 647, 653, 659, 661, 673, 677, 683, 691, 701, 709,
                         719, 727, 733, 739, 743, 751, 757, 761, 769, 773, 787, 797, 809, 811,
                         821, 823, 827, 829, 839, 853, 857, 859, 863, 877, 881, 883, 887, 907,
                         911, 919, 929, 937, 941, 947, 953, 967, 971, 977, 983, 991, 997])
 
 
def is_prime(num):
    # 排除0,1和负数
    if num < 2:
        return False
    # 排除小素数的倍数
    for prime in small_primes:
        if num % prime == 0:
            return False
    # 未分辨出来的大整数用rabin算法判断
    return rabin_miller(num)
 
 
def rabin_miller(num):
    s = num - 1
    t = 0
    while s & 1 == 0:
        s >>= 1
        t += 1
    for trials in range(5):
        a = random.randrange(2, num - 1)
        v = pow(a, s, num)
        if v != 1:
            i = 0
            while v != (num - 1):
                if i == t - 1:
                    return False
                else:
                    i = i + 1
                    v = v * v % num
    return True
 
 
# 将字节转换为int
def to_int(byte):
    return int.from_bytes(byte, byteorder='big')
 
 
# 转换为bytes，第二参数为字节数（可不填）
def to_byte(x, size=None):
    if isinstance(x, int):
        if size is None:  # 计算合适的字节数
            size = 0
            tmp = x >> 64
            while tmp:
                size += 8
                tmp >>= 64
            tmp = x >> (size << 3)
            while tmp:
                size += 1
                tmp >>= 8
        elif x >> (size << 3):  # 指定的字节数不够则截取低位
            x &= (1 << (size << 3)) - 1
        return x.to_bytes(size, byteorder='big')
    elif isinstance(x, str):
        x = x.encode()
        if size != None and len(x) > size:  # 超过指定长度
            x = x[:size]  # 截取左侧字符
        return x
    elif isinstance(x, bytes):
        if size != None and len(x) > size:  # 超过指定长度
            x = x[:size]  # 截取左侧字节
        return x
    elif isinstance(x, tuple) and len(x) == 2 and type(x[0]) == type(x[1]) == int:
        # 针对坐标形式(x, y)
        return to_byte(x[0], size) + to_byte(x[1], size)
    return bytes(x)
 
 
# 将列表元素转换为bytes并连接
def join_bytes(data_list):
    return b''.join([to_byte(i) for i in data_list])
 
 
# 求最大公约数
def gcd(a, b):
    return a if b == 0 else gcd(b, a % b)
 
 
# 求乘法逆元过程中的辅助递归函数
def get_(a, b):
    if b == 0:
        return 1, 0
    x1, y1 = get_(b, a % b)
    x, y = y1, x1 - a // b * y1
    return x, y

# 求乘法逆元
def get_inverse(a, p):
    # return pow(a, p-2, p) # 效率较低、n倍点的时候两种计算方法结果会有不同
    if gcd(a, p) == 1:
        x, y = get_(a, p)
        return x % p
    return 1
 
# 密钥派生函数（从一个共享的秘密比特串中派生出密钥数据）
# SM2第3部分 5.4.3
# Z为bytes类型
# klen表示要获得的密钥数据的比特长度（8的倍数），int类型
# 输出为bytes类型
def KDF(Z, klen):
    ksize = klen >> 3
    K = bytearray()
    for ct in range(1, math.ceil(ksize / HASH_SIZE) + 1):
        K.extend(sm3(Z + to_byte(ct, 4)))
    return K[:ksize]
 
# 计算比特位数
def get_bit_num(x):
    if isinstance(x, int):
        num = 0
        tmp = x >> 64
        while tmp:
            num += 64
            tmp >>= 64
        tmp = x >> num >> 8
        while tmp:
            num += 8
            tmp >>= 8
        x >>= num
        while x:
            num += 1
            x >>= 1
        return num
    elif isinstance(x, str):
        return len(x.encode()) << 3
    elif isinstance(x, bytes):
        return len(x) << 3
    return 0
 
 
# 椭圆曲线密码类（实现一般的ECC运算，不局限于SM2）
class ECC:
    def __init__(self, p, a, b, n, G, h=None):
        self.p = p
        self.a = a
        self.b = b
        self.n = n
        self.G = G
        if h:
            self.h = h
        self.O = (-1, -1)  # 定义仿射坐标下无穷远点（零点）
 
        # 预先计算Jacobian坐标两点相加时用到的常数
        self._2 = get_inverse(2, p)
        self.a_3 = (a + 3) % p
 
    # 椭圆曲线上两点相加（仿射坐标）
    # SM2第1部分 3.2.3.1
    # 仅提供一个参数时为相同坐标点相加
    def add(self, P1, P2=None):
        x1, y1 = P1
        if P2 is None or P1 == P2:  # 相同坐标点相加
            # 处理无穷远点
            if P1 == self.O:
                return self.O
            # 计算斜率k（k已不具备明确的几何意义）
            k = (3 * x1 * x1 + self.a) * get_inverse(2 * y1, self.p) % self.p
            # 计算目标点坐标
            x3 = (k * k - x1 - x1) % self.p
            y3 = (k * (x1 - x3) - y1) % self.p
        else:
            x2, y2 = P2
            # 处理无穷远点
            if P1 == self.O:
                return P2
            if P2 == self.O:
                return P1
            if x1 == x2:
                return self.O
            # 计算斜率k
            k = (y2 - y1) * get_inverse(x2 - x1, self.p) % self.p
            # 计算目标点坐标
            x3 = (k * k - x1 - x2) % self.p
            y3 = (k * (x1 - x3) - y1) % self.p
        return x3, y3
 
    # 椭圆曲线上的点乘运算（仿射坐标）
    def multiply(self, k, P):
        # 判断常数k的合理性
        assert type(k) is int and k >= 0, 'factor value error'
        # 处理无穷远点
        if k == 0 or P == self.O:
            return self.O
        if k == 1:
            return P
        elif k == 2:
            return self.add(P)
        elif k == 3:
            return self.add(P, self.add(P))
        elif k & 1 == 0:  # k/2 * P + k/2 * P
            return self.add(self.multiply(k >> 1, P))
        elif k & 1 == 1:  # P + k/2 * P + k/2 * P
            return self.add(P, self.add(self.multiply(k >> 1, P)))
 
    # 输入P，返回-P
    def minus(self, P):
        Q = list(P)
        Q[1] = -Q[1]
        return tuple(Q)
 
 
    # 判断是否为无穷远点（零点）
    def is_zero(self, P):
        if len(P) == 2:  # 仿射坐标
            return P == self.O
        else:  # Jacobian加重射影坐标
            return P[2] == 0
 
    # 判断是否为域Fp中的元素
    # 可输入多个元素，全符合才返回True
    def on_Fp(self, *x):
        for i in x:
            if 0 <= i < self.p:
                pass
            else:
                return False
        return True
 
    # 判断是否在椭圆曲线上
    def on_curve(self, P):
        if self.is_zero(P):
            return False
        x, y = P
        return y * y % self.p == (x * x * x + self.a * x + self.b) % self.p
       
    # 生成密钥对
    # 返回值：d为私钥，P为公钥
    # SM2第1部分 6.1
    def gen_keypair(self):
        d = random.randint(1, self.n - 2)
        P = self.multiply(d, self.G)
        return d, P
 
    # 公钥验证
    # SM2第1部分 6.2.1
    def pk_valid(self, P):
        # 判断点P的格式
        if P and len(P) == 2 and type(P[0]) == type(P[1]) == int:
            pass
        else:
            self.error = '格式有误'  # 记录错误信息
            return False
        # a) 验证P不是无穷远点O
        if self.is_zero(P):
            self.error = '无穷远点'
            return False
        # b) 验证公钥P的坐标xP和yP是域Fp中的元素
        if not self.on_Fp(*P):
            self.error = '坐标值不是域Fp中的元素'
            return False
        # c) 验证y^2 = x^3 + ax + b (mod p)
        if not self.on_curve(P):
            self.error = '不在椭圆曲线上'
            return False
        # d) 验证[n]P = O
       
        return True
 
    # 确认目前已有公私钥对
    def confirm_keypair(self):
        if not hasattr(self, 'pk') or not self.pk_valid(self.pk) or self.pk != self.multiply(self.sk, self.G):
            # 目前没有合格的公私钥对则生成
            while True:
                d, P = self.gen_keypair()
                if self.pk_valid(P):  # 确保公钥通过验证
                    self.sk, self.pk = d, P
                    return
 
 
# 国家密码管理局：SM2椭圆曲线公钥密码算法推荐曲线参数
SM2_p = 0xFFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF00000000FFFFFFFFFFFFFFFF
SM2_a = 0xFFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF00000000FFFFFFFFFFFFFFFC
SM2_b = 0x28E9FA9E9D9F5E344D5A9E4BCF6509A7F39789F515AB8F92DDBCBD414D940E93
SM2_n = 0xFFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFF7203DF6B21C6052B53BBF40939D54123
SM2_Gx = 0x32C4AE2C1F1981195F9904466A39C9948FE30BBFF2660BE1715A4589334C74C7
SM2_Gy = 0xBC3736A2F4F6779C59BDCEE36B692153D0A9877CC62A474002DF32E52139F0A0
 
PARA_SIZE = 32  # 参数长度（字节）
HASH_SIZE = 32  # sm3输出256位（32字节）
KEY_LEN = 128  # 默认密钥位数
 
# SM2类继承ECC
class SM2(ECC):
    # 默认使用SM2推荐曲线参数
    def __init__(self, p=SM2_p, a=SM2_a, b=SM2_b, n=SM2_n, G=(SM2_Gx, SM2_Gy), h=None,
                 ID=None, sk=None, pk=None, genkeypair=True):  # genkeypair表示是否自动生成公私钥对
        if not h:  # 余因子h默认为1
            h = 1
        ECC.__init__(self, p, a, b, n, G, h)
 
        self.keysize = len(to_byte(n))  # 密钥长度（字节）
        if type(ID) in (int, str):  # 身份ID（数字或字符串）
            self.ID = ID
        else:
            self.ID = ''
        if sk and pk:  # 如果提供的公私钥对通过验证，即使genkeypair=True也不会重新生成
            self.sk = sk  # 私钥（int [1,n-2]）
            self.pk = pk  # 公钥（x, y）
            self.confirm_keypair()  # 验证该公私钥对，不合格则生成
        elif genkeypair:  # 自动生成合格的公私钥对
            self.confirm_keypair()
 
        # 预先计算用到的常数
        if hasattr(self, 'sk'):  # 签名时
            self.d_1 = get_inverse(1 + self.sk, self.n)
 
    # 计算Z
    # SM2第2部分 5.5
    # ID为数字或字符串，P为公钥（不提供参数时返回自身Z值）
    def get_Z(self, ID=None, P=None):
        save = False
        if not P:  # 不提供参数
            if hasattr(self, 'Z'):  # 再次计算，返回曾计算好的自身Z值
                return self.Z
            else:  # 首次计算自身Z值
                ID = self.ID
                P = self.pk
                save = True
        entlen = get_bit_num(ID)
        ENTL = to_byte(entlen, 2)
        Z = sm3(join_bytes([ENTL, ID, self.a, self.b, *self.G, *P]))
        if save:  # 保存自身Z值
            self.Z = Z
        return Z
 
    # A 发起协商
    # SM2第3部分 6.1 A1-A3
    # 返回rA、RA
    def agreement_initiate(self):
        return self.gen_keypair()
 
    # B 响应协商（option=True时计算选项部分）
    # SM2第3部分 6.1 B1-B9
    def agreement_response(self, RA, PA, IDA, option=False, rB=None, RB=None, klen=None):
        # 参数准备
        if not self.on_curve(RA):
            return False, 'RA不在椭圆曲线上'
        x1, y1 = RA
        w = math.ceil(math.ceil(math.log(self.n, 2)) / 2) - 1
        if not hasattr(self, 'sk'):
            self.confirm_keypair()
        h = 1  # SM2推荐曲线的余因子h=1
        ZA = self.get_Z(IDA, PA)
        ZB = self.get_Z()
        # B1-B7
        rB, RB = self.gen_keypair()
        x2, y2 = RB
        x_2 = (1 << w) + (x2 & (1 << w) - 1)
        tB = (self.sk + x_2 * rB) % self.n
        x_1 = (1 << w) + (x1 & (1 << w) - 1)
        V = self.multiply(h * tB, self.add(PA, self.multiply(x_1, RA)))
        if self.is_zero(V):
            return False, 'V是无穷远点'
        xV, yV = V
        if not klen:
            klen = KEY_LEN
        KB = KDF(join_bytes([xV, yV, ZA, ZB]), klen)
        if not option:
            return True, (RB, KB)
        # B8、B10（可选部分）
        tmp = join_bytes([yV, sm3(join_bytes([xV, ZA, ZB, x1, y1, x2, y2]))])
        SB = sm3(join_bytes([2, tmp]))
        S2 = sm3(join_bytes([3, tmp]))
        return True, (RB, KB, SB, S2)
 
    # A 协商确认
    # SM2第3部分 6.1 A4-A10
    def agreement_confirm(self, rA, RA, RB, PB, IDB, SB=None,KA=0,option=False, klen=None):
        # 参数准备
        if not self.on_curve(RB):
            return False, 'RB不在椭圆曲线上'
        x1, y1 =RA
        x2, y2 =RB
        w = math.ceil(math.ceil(math.log(self.n, 2)) / 2) - 1
        if not hasattr(self, 'sk'):
            self.confirm_keypair()
        h = 1  # SM2推荐曲线的余因子h=1
        ZA = self.get_Z()
        ZB = self.get_Z(IDB, PB)
        # A4-A8
        x_1 = (1 << w) + (x1 & (1 << w) - 1)
        tA = (self.sk + x_1 * rA) % self.n
        x_2 = (1 << w) + (x2 & (1 << w) - 1)
        U = self.multiply(h * tA, self.add(PB, self.multiply(x_2, RB)))
        if self.is_zero(U):
            return False, 'U是无穷远点'
        xU, yU = U
        if not klen:
            klen = KEY_LEN
        KA = KDF(join_bytes([xU, yU, ZA, ZB]), klen)
        print(type(KA))
        print("KA:",KA)
        print("KA:",KA.hex())
        if not option or not SB:
            return True, KA
        # A9-A10（可选部分）
        tmp = join_bytes([yU, sm3(join_bytes([xU, ZA, ZB, x1, y1, x2, y2]))])
        S1 = sm3(join_bytes([2, tmp]))
        if S1 != SB:
            return False, 'S1 != SB',KA
        SA = sm3(join_bytes([3, tmp]))
        return True, (KA, SA)
 
    # B 协商确认（可选部分）
    # SM2第3部分 6.1 B10
    def agreement_confirm2(self, S2, SA):
        if S2 != SA:
            return False, 'S2 != SA'
        return True, ''
 
    # 加密
    # SM2第4部分 6.1
    # 输入：待加密的消息M（bytes或str类型）、对方的公钥PB、随机数k（不填则自动生成）
    # 输出(True, bytes类型密文)或(False, 错误信息)
    def encrypt(self, M, PB, k=None):
        if self.is_zero(self.multiply(self.h, PB)):  # S
            return False, 'S是无穷远点'
        M = to_byte(M)
        klen = get_bit_num(M)
        while True:
            if not k:
                k = random.randint(1, self.n - 1)
            x2, y2 = self.multiply(k, PB)
            
            t = to_int(KDF(join_bytes([x2, y2]), klen))
            if t == 0:  # 若t为全0比特串则继续循环
                k = 0
            else:
                break
        C1 = to_byte(self.multiply(k, self.G), self.keysize) # (x1, y1)
        C2 = to_byte(to_int(M) ^ t, klen >> 3)
        C3 = sm3(join_bytes([x2, M, y2]))
        return True, join_bytes([C1, C2, C3])
 
    # 解密
    # SM2第4部分 7.1
    # 输入：密文C（bytes类型）
    # 输出(True, bytes类型明文)或(False, 错误信息)
    def decrypt(self, C):
        x1 = to_int(C[:self.keysize])
        y1 = to_int(C[self.keysize:self.keysize << 1])
        C1 = (x1, y1)
        if not self.on_curve(C1):
            return False, 'C1不满足椭圆曲线方程'
        if self.is_zero(self.multiply(self.h, C1)):  # S
            return False, 'S是无穷远点'
        x2, y2 = self.multiply(self.sk, C1)
        klen = len(C) - (self.keysize << 1) - HASH_SIZE << 3
        t = to_int(KDF(join_bytes([x2, y2]), klen))
        if t == 0:
            return False, 't为全0比特串'
        C2 = C[self.keysize << 1:-HASH_SIZE]
        M = to_byte(to_int(C2) ^ t, klen >> 3)
        u = sm3(join_bytes([x2, M, y2]))
        C3 = C[-HASH_SIZE:]
        #if u != C3:
            #return False, 'u != C3'
        return True, M
    
 #d1是其中一个人的私钥，由两人公钥来计算合成后的公钥和私钥
    '''
     def two_party_decrypt_first(self,C):
          x1 = to_int(C[:self.keysize])
        y1 = to_int(C[self.keysize:self.keysize << 1])
        C1 = (x1, y1)
        if not self.on_curve(C1):
            return False, 'C1不满足椭圆曲线方程'
        if self.is_zero(self.multiply(self.h, C1)):  # S
            return False, 'S是无穷远点'
        T1 = self.multiply(get_inverse(self.sk), C1)
        #收到T2
        x2,y2=self.add(T2,minus(C1))
        t=to_int(KDF(join_bytes([x2, y2]), klen))
        M = to_byte(to_int(C2) ^ t, klen >> 3)
        u = sm3(join_bytes([x2, M, y2]))
        C3 = C[-HASH_SIZE:]
        if u != C3:
            return False, 'u != C3'
        return True, M
    def two_party_decrypt_second(self,C):
        #收到T1
        T2=self.multiply(get_inverse(self.sk),T1)
        #将T2发送过去 
  '''
# SM2加解密测试
# SM2第4部分 A.1 A.2
def test_encryption():
  
 
    # A将密文C发送给B
 
    # B用自己的私钥对密文C进行解密
    res, M2 = sm2_B.decrypt(C)
    if not res:
        print('B报告解密错误：', M2)
        return
    time_2 = get_cpu_time()
    print('SM2加解密完毕，耗时%.2f ms' % ((time_2 - time_1) * 1000))
    print('结果：%s，解密得：%s(%s)' % (res, M2.hex(), M2.decode()))
    # 加解密成功，解密后的16进制值(656e6372797074696f6e207374616e64617264)与SM2第4部分 A.2中的结果一致
