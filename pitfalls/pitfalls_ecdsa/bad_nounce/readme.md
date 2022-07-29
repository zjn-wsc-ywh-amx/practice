# bad nonce

## 代码说明

利用LLL算法输入一个值的矩阵，而后得到一个新值的矩阵，LLL输出的一行将包括k值。

可以通过调用ecdsa库和lll库实现该算法。

首先生成签名，对各参数进行定义。然后构造传入的矩阵：
$$
\left|\begin{array}{cccc}
N & 0 & 0 & 0 \\
0 & N & 0 & 0 \\
r_{1} s_{1}^{-1} & r_{2} s_{2}^{-1} & B / N & 0 \\
m_{1} s_{1}^{-1} & \mathrm{~m}_{2} s_{2}^{-1} & 0 & B
\end{array}\right|
$$
其中，N代表使用的椭圆曲线的阶数，本代码中使用NIST256p；B是k的上限；m~1~和m~2~是两条消息；（r,s)是返回的签名对。使用SVP计算算法和格基约化算法得到一组输出矩阵。但这个算法是一个概率算法，不一定每次都能成功。

## 运行指导

运行ecdsa_badnounce.py，需要下载ecdsa和olll库

## 运行截图

![C10FA0@(N37B_74IIE(SCSW](D:\pythonProject2\pitfalls\bad_nounce\C10FA0@(N37B_74IIE(SCSW.png)

## 引用

[1]ECDSA: Handle with Care[DB/OL] (2020.6.11) https://blog.trailofbits.com/2020/06/11/ecdsa-handle-with-care/

[2]Breitner J, Heninger N. Biased nonce sense: Lattice attacks against weak ECDSA signatures in cryptocurrencies[C]//International Conference on Financial Cryptography and Data Security. Springer, Cham, 2019: 3-20.