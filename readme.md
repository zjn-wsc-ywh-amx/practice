## *Project: implement sm2 2P sign with real network communication



### 代码介绍：

代码一共分为6个py文件：

ECC文件中是椭圆曲线运算的实现以及椭圆曲线的参数

sig_partone以及sigpartwo中主要写了两方前面的主要计算过程的API调用，

test文件是没有网络通信的测试环境

socket_p1,socket-p2是在UDP协议下签名两方交互过程

### 代码运行方法：

##### 1、将代码load到本地

##### 2、安装必要的第三方库（json,hashlib,socket等）

##### 3、test.py可直接运行

##### 4、socket_p1,socket_p2,运行时要先运行socket_p2.py，再运行socket_p2.py

### 运行结果：

<img src="C:\Users\amx\AppData\Roaming\Typora\typora-user-images\image-20220727212212137.png" alt="image-20220727212212137" style="zoom: 50%;" />

<img src="C:\Users\amx\AppData\Roaming\Typora\typora-user-images\image-20220727212326287.png" alt="image-20220727212326287" style="zoom:50%;" />





