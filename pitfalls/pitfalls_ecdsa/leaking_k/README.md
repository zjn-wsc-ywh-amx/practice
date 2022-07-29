# Leaking K

## 代码说明

当k的值被泄露时，攻击者可以根据公式
$$
\begin{array}{l}
s=(h+r d) k^{-1} \bmod n \\
d=(s k-h) r^{-1} \bmod n
\end{array}
$$
得到私钥值

## 运行指导

运行ecdsa_leakingk.py，需要下载ecdsa库

## 运行截图

![](D:\pythonProject2\pitfalls\leaking_k\QQ截图20220728215318.png)

## 引用

对ecdsa库中的代码进行了修改，即文件夹中的文件