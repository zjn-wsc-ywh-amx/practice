import hmac,hashlib

code_strings = {
    2: '01',
    10: '012356789',
    16: '0123456789abcdef',
    32: 'abcdefghijklmnopqrstuvwxyz234567',
    58: '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz',
    256: ''.join([chr(x) for x in range(256)])
}

def encode(val):#参考了pybitcointools中的编码实现base即进制数，决定使用的编码方式，不过我们这只用256所以简化一下desu~
    code_string = ''.join([chr(x) for x in range(256)])#256，所以搞一下unicode编码
    result_bytes = bytes()#以字节形式返回一个新的 bytes 对象，是 0 <= x < 256 区间内的整数不可变序列
    while val>0:#循环几次要看val是几倍的256
        curcode = code_string[val % 256]#val转换为所需进制
        result_bytes = bytes([ord(curcode)]) + result_bytes#以ascii码形式转换为bytes对象
        val //= 256

    pad_size = 32 - len(result_bytes)#计算填充的个数
    padding_element = b'\x00'

    if (pad_size > 0):
        result_bytes = padding_element * pad_size + result_bytes#连接起来

    return result_bytes

def extract(d,cs,base):#decode里要用，从cs串里找到所需的
    if base == '256':
        return d
    else:
        if isinstance(d, str):
            return cs.find(d)
        else:
            return cs.find(chr(d))

def decode(string, base):#解码
    if base == 256 and isinstance(string, str):
        string = bytes(bytearray.fromhex(string))#还是经典的256转byte环节
    base = int(base)
    code_string = code_strings[base]#还是熟悉的流程
    result = 0
    if base == 16:
        string = string.lower()#16进制都转成小写
    while len(string) > 0:
        result *= base
        result += extract(string[0], code_string,base)
        string = string[1:]#把b去掉！去掉！
    return result

def hash_to_int(x):#其实就相当于一个解码过程
    if len(x) in [40, 64]:
        return decode(x, 16)
    return decode(x, 256)

# def bits2int(data, qlen):#仿照rfc文档写的，不过注释掉了循环之后就用不上了
#     x = int(hexlify(data), 16)
#     l = len(data) * 8
#
#     if l > qlen:
#         return x >> (l - qlen)
#     return x


def rfc(m,pk):#按照RFC6979文档中给定的流程来
    qlen=len(str(pk))*8
    h1 = hashlib.sha256()  # 创建sha1加密对象
    h1.update(str(m).encode("utf-8"))  # 转码（字节流）
    h1 = h1.hexdigest()  # 将字节码转成16进制
    hlen = hashlib.sha256().digest_size#哈希值长度

    V=b"\x01"*hlen
    K=b"\x00"*hlen

    pk=encode(pk)#对私钥进行编码
    h1=encode(hash_to_int(h1))#对消息的哈希值进行编码，注意要把哈希值转换成int类型才能用编码函数

    K = hmac.new(K, V + b'\x00' + pk + h1, hashlib.sha256).digest()
    V = hmac.new(K, V, hashlib.sha256).digest()
    K = hmac.new(K, V + b'\x01' + pk + h1, hashlib.sha256).digest()
    V = hmac.new(K, V, hashlib.sha256).digest()

    return int(decode(hmac.new(K, V, hashlib.sha256).digest(), 256))#由于在循环中的解码过程一直失败，因此参考了库pybitcointools中的实现方法，到底为什么能这样我也没看透，大概是比特币的神秘力量
    # while True:
    #     T = ""
    #     tlen=len(T)*8
    #     while(tlen < qlen):
    #         V=hmac.new(K,V,digestmod='sha1').digest()
    #         T += V
    #
    #     k = bits2int(T,qlen)
    #     if(k>=1 and k< m):
    #         return k
    #     else:
    #         K=hmac.new(K,V+b"\x00",digestmod='sha256').digest()
    #         V=hmac.new(K,V,digestmod='sha256').digest()

