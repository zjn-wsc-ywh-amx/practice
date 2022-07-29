# reusing k

## 代码描述

如果同一个人使用了两次同一个k那么私钥可以被计算得到
$$
k=\left(h_{1}-h_{2}\right)\left(s_{1}-s_{2}\right)^{-1} \bmod n
$$

## 运行指导

运行ecdsa_reusingk.py，需要下载ecdsa库

## 运行截图

![](D:\pythonProject2\pitfalls\reusing_k\QQ截图20220728222032.png)

## 引用

对ecdsa库中的代码进行了修改，即文件夹中的文件