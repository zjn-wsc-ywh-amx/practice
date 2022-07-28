# project：PGP in SM2
# 代码文件介绍
该文件夹下共三个.py文件，  
SM2.py文件中为基本的椭圆曲线类的方法以及SM2中定义的加解密函数、密钥协商确定回复等函数    
client.py文件模拟Alice，包含三个过程，分别为：密钥协商 对称加密消息 SM2加密密钥。  
server.py文件模拟Bob，同样包含三个过程，分别为：密钥协商 对称解密信息 SM2解密密钥。  

# 代码运行方法
将代码load到本地后下载必要的库（json  socket Crypto）  
运行时先运行server.py文件，再运行client.py文件。  
# PGP构建
![image](https://github.com/zjn-wsc-ywh-amx/practice/blob/master/PGP%20in%20SM2/PGP.png)
# 代码运行结果
## Alice运行结果
![image](https://github.com/zjn-wsc-ywh-amx/practice/blob/master/PGP%20in%20SM2/PGP-Alice.png)
## Bob运行结果
![image](https://github.com/zjn-wsc-ywh-amx/practice/blob/master/PGP%20in%20SM2/PGP-Bob.png)
#  参考文献
[](https://blog.csdn.net/qq_42248536/article/details/105805078)
[](https://blog.csdn.net/qq_43339242/article/details/123221091)
