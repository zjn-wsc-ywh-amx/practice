# impl RFC6979 on SM2

注：使用test.py测试本代码需要安装gmssl库（可恶github和typora上显示的居然不一样，凑合看吧）,testsm2.py则不用

## RFC6979

参照RFC文档中的实现方式，首先可以明确大致思路如下：^[1]^

+ 设置私钥为pk，私钥长度为qlen，消息为m

1. 计算h1 = H(m),H即哈希函数，我选用的是SHA256，hlen为哈希值的比特长度
2. 设置V = 0x01 0x01... 0x01，长度为hlen
3. 设置K = 0x00 0x00... 0x00，长度为heln
4. 计算K = HMAC(V||0x00||int2octets(x)||bits2octets(h1))
5. V = HMAC(V)
6. K = HMAC(V||0x01||int2octets(x)||bits2octets(h1))
7. V = HMAC(V)
8. 执行以下循环至找到合适的K
   * 设T为空序列，T长度为tlen个bit
   * tlen<qlen时执行
     * V = HMAC(V)
     * T = T||V
   * 计算k=bits2int(T),k∈[1,q-1]，则可输出，否则计算
     * K =  HMAC(V||0x00)
     * V = HMAC(V)

按照此流程初步实现了一种写法，但是在最后的循环部分有些小瑕疵，会出bug，于是参考了pybitcointools中的处理方法，详见代码

## SM2

RFC6979主要是为SM2中的随机数生成部分服务。mysm2.py中的代码参照了GMSSL库中的实现方式，流程图如下^[2]^

![img](https://img-blog.csdn.net/20180622110145207?watermark/2/text/aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3NhbXNobzI=/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70)

SM2算法中的私钥是大整数，公钥是椭圆曲线上的点。公私钥可以采用支付宝提供的密钥生成工具生成后转换为16进制，以加密为例，流程图如下[生成并配置密钥 - 支付宝文档中心 (alipay.com)](https://opendocs.alipay.com/common/02kdnc)^[3]^

![img](https://webencrypt.org/sm2/sm2encrypt.png)

SM2的优势之一在于采用随机数，因此同样的明文数据每一次加密结果都不一样，而使用RFC6979生成的k值由消息与私钥决定，因此可能会得到一样的结果，故在实现中同时采用RFC6979和随机数生成k值，并将二者相加从而使每次的加密结果不同，这样既保证泄露随机数种子也不能泄密，又能使同样的明文密钥能够得到不同的加密数值。

## 运行结果
![image](https://user-images.githubusercontent.com/95538947/182013411-ea3cfd16-26f6-4018-aa33-213039c21135.png)


## 参考文献

[1]Mykeylab0003期-从未触网的私钥是如何丢失的[DB/OL] . (2019-5-10) https://www.youtube.com/watch?v=FzWltJQ4ra4&t=626s

[2]关于SM2国密算法开发流程[DB/OL] . (2021-04-02) https://blog.csdn.net/I_O_fly/article/details/115391340

[3]Web Encrypt-SM2加密算法[EB/OL] https://webencrypt.org/sm2/#sm2encrypt
