# project：2P-decrypt in SM2
# 代码文件介绍
该文件夹下共三个.py文件，  
SM2__.py文件中为基本的椭圆曲线类的方法以及SM2中定义的加解密函数、密钥协商确定回复等函数    
client2-Alice.py文件模拟Alice，主要由Alice得到密文并在Bob的协助下得到明文。  
server2-Bob.py文件模拟Bob，主要给Alice提供一些解密必要的信息发送过去。  

# 代码运行方法
将代码load到本地后下载必要的库（json  socket）  
运行时先运行server2-Bob.py文件，再运行client2-Alice.py文件。  
# 代码运行结果
## Alice端运行结果
![image](https://github.com/zjn-wsc-ywh-amx/practice/blob/master/2P_decrypt/Alice-two_party_decrypt.png)
## Bob端运行结果
![image](https://github.com/zjn-wsc-ywh-amx/practice/blob/master/2P_decrypt/Bob-two_party_decrypt.png)
