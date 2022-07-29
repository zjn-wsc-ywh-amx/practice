# Deduce Private Key

## 代码说明

一旦两个人使用了相同的随机数k，那么两个人可以推断出彼此的私钥，这可以被攻击者利用。
$$
\begin{array}{l}
s_{1}=k^{-1}\left(h_{1}+r_{1} x\right) mod n\\
s_{2}=k^{-1}\left(h_{2}+r_{2} x\right) mod n
\end{array}
$$
h即消息哈希值，(r,s)为签名。由于r只由k和椭圆曲线决定，因此r~1~=r~2~.

由此可以推出
$$
\frac{s_{1}}{s_{2}}=\frac{h_{1}+d_{1} r}{h_{2}+d_{2} r} mod  n
$$

$$
\frac{s_{1}\left( h_{2}+d_{2} r\right)}{s_{2}}=h_{1}+d_{1} r\quad mod n
$$

最后得到
$$
d_{1}=\frac{s_{1} h_{2}+d r s_{1}-s_{2} h_{1}}{s_{2} r} \bmod n
$$

## 运行指导

运行ecdsa_deduced.py，需要下载ecdsa库

## 运行截图

![](D:\pythonProject2\pitfalls\deduce_d\QQ截图20220728214728.png)

## 引用说明

在ecdsa库的基础上进行了修改，即同一文件夹中的代码