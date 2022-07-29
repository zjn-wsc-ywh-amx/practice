# schnorr签名漏洞利用

## 代码说明

shnorr.py中的point_mult函数是在借鉴了[schnorr-examples/schnorr.py at master · yuntai/schnorr-examples (github.com)](https://github.com/yuntai/schnorr-examples/blob/master/schnorr/schnorr.py)后写的，说实话shnorr拼错了但懒得改了，希望给予文盲或半文盲一点关爱

整体跟ecdsa大差不差的，就不挨个写readme了

其中One can forge signature if the verification does not check m和ecdsa相差较大，详情双击文件夹forge

此外参照了一篇论文^[1]^中的攻击手法，写了一个demo代码，我感觉只能应用在小规模的曲线上，原理如下：

* 攻击者收集签名者的正确签名集 ，记为
  $$
  M_1,(r||s)、M_2,(r_2||s_2)
  $$
  若需要签名的消息为 M-，然后进行如下计算 ：

  * $$
    r' = r_1 ·r_2 \bmod n  \longrightarrow r' = g^{k_1}·g^{k_2} \bmod n
    $$
    
  * $$
    e' = H(r'||M') \bmod n
    $$
  
    
  
  * $$
    e_1 = H(r_1||M_1) \bmod n
    $$
  
    
  
  * $$
    e_2 = H(r_2||M_2) \bmod n
    $$
  
    

* 若集合中有签名使得
  $$
  e' \equiv e_1 + e_2 \bmod n
  $$
  则攻击者可以选择这个签名集，即

$$
M_1,(r||s)、M_2,(r_2||s_2)
$$

来骗，来偷袭，欺负schnorr79岁的老同志。然后进行后续计算：
$$
s^{\prime}=s_{1}+s_{2} \bmod n \Rightarrow s^{\prime}=k_{1}+x e_{1}+k_{2}+x e_{2}\bmod n
$$

$$
s' =k_{1}+k_{2}+x\left(e_{1}+e_{2}\right) \bmod n
$$

则M-，(r'||s')就是一对假冒的正确签名。

证明：
$$
\begin{aligned}
&g^{s^{\prime}} y^{-e^{\prime}}=g^{s_{1}+s_{2}} g^{-x e^{\prime}}=g^{k_{1}+k_{2}+x\left(e_{1}+e_{2}\right)} g^{-x\left(e_{1}+e_{2}\right)}=g^{k_{1}+k_{2}}= 
r^{\prime} \bmod p
\end{aligned}
$$
但我觉得在这个算法复杂度不低，可能相当于碰撞了，所以没采用。

## 引用

[1]:刘景美 王新梅. Schnorr签名方案的一种攻击[J]. 计算机科学, 2006, 33(7): 141-142.

LIU Jing-Mei, WANG Xin-Mei （National Key Lab. of Integrated Service Networks,Xidian Univ. ,Xi＇an 710071）. [J]. Computer Science, 2006, 33(7): 141-142.