import hashlib
import os
import ECC
def str_hash_int(msg:str):
    hmsg=hashlib.sha256(msg.encode("utf-8")).hexdigest()
    return int(hmsg,16)
def Gen_msg_ECCP(msg):#求消息对应的椭圆曲线的点的坐标
    nonce = 0
    while True:
        t=str_hash_int(msg)
        temp =str(nonce)+str(t)
        #print(temp)
        x = str_hash_int(temp)
        y = ECC.get_y(x)  # 求出哈希值作为x，求出对应的y
        if y != None:
            #print(nonce)
            return (str(msg)+"  ||  "+str(nonce),x,y)
        nonce += 1
def hash_add(hash_a,hash_b):#利用椭圆曲线将两个集合的hash值相加
   return ECC.Point_Add(hash_a,hash_b)
def textadd(filenamea,filenameb):#将两个文件内容整合
    filenamec=open("totaltext.txt","w+")
    with open(filenamea) as f:
        for line in f:
            filenamec.write(line)
    with open(filenameb) as g:
        for line in g:
            filenamec.write(line)
    filenamec.close()
def cacu_hash(filename):
    hashoutput=open("hashoutput","w+")
    hash_ret=[-1,-1]#集合hash结果初始值为无穷远点
    with open(filename) as f:
        for line in f:
            m,h_num,y=Gen_msg_ECCP(line[:-1])
            hashoutput.write(m+"  ||  "+str(h_num)+" : "+str(y)+"\n")
            hash_ret=ECC.Point_Add(hash_ret,(h_num,y))
    hashoutput.close()
    return hash_ret
def verify_hab_equal_hahb():#验证同态性
    filenamec=textadd("UTXOa.txt","UTXOb.txt")
    print("(UTXOa+UTXOb) hash value:  ")
    print(cacu_hash("totaltext.txt"))
    print("UTXOa hash:",cacu_hash("UTXOa.txt"))
    print("UTXOb hash",cacu_hash("UTXOb.txt"))
    print("UTXOa hash+UTXOb hash:")
    print(hash_add(cacu_hash("UTXOa.txt"),cacu_hash("UTXOb.txt")))