## *Project: lmplement the above ECMH scheme

#### 代码说明：

本项目代码主要有四个文件ECC.py,UTXOhash.py,UTXO.txt,hashoutput

##### ECC.py 主要实现了椭圆曲线的相关运算

##### UTXOhash.py为本项目的主体代码，其中实现了将任意长度信息转化为某一椭圆曲线上的点，并在此基础上完成对整个集合的hash值

##### hashoutput记录了集合中每一条UTXO经过转化后的坐标值其记录结构为 UTXO原始值  ||  nonce  ||  x坐标:y坐标

##### UTXO.txt 用来记录要进行哈希的UTXO数据

#### 代码运行方法：

##### 将代码下载到本地

##### 直接运行UTXOhash.py即可
