## 小组成员：

| 小组成员姓名 | 学号         | Github账户名称                                               |
| ------------ | ------------ | ------------------------------------------------------------ |
| 安茂祥       | 202000180071 | [**hellowoe23 (Maoxiang An) **](https://github.com/hellowoe23) |
| 尹文浩       | 202000180069 | [**wynneyin (尹文浩)**](https://github.com/wynneyin)         |
| 张佳宁       | 202000161013 | [**zjn-wsc-ywh-amx** ](https://github.com/zjn-wsc-ywh-amx)   |
| 王思程       | 202000111024 | [**hsj10 (何斩斩) **](https://github.com/hsj10)              |

## 代码仓库地址：

## [zjn-wsc-ywh-amx/practice: 创新创业实践 (github.com)](https://github.com/zjn-wsc-ywh-amx/practice)

## 项目及完成情况：

（右4列为小组成员每个人的贡献以及排序① ，②， ③， ④依次递减）



| 项目序号 | 项目名称                                                     | 文件夹对应                                                   | 王思程 | 张佳宁 | 尹文浩 | 安茂祥 |
| -------- | ------------------------------------------------------------ | ------------------------------------------------------------ | ------ | ------ | ------ | ------ |
|          | ***SM3***                                                    |                                                              |        |        |        |        |
| 1        | Implement the naïve birthday attack of reduced SM3           | [生日攻击](https://github.com/zjn-wsc-ywh-amx/practice/tree/master/生日攻击) |        |        |        |        |
| 2        | Implement the Rho method of reduced SM3                      | [sm3_rho_demo](https://github.com/zjn-wsc-ywh-amx/practice/tree/master/sm3_rho_demo)\\[SM3](https://github.com/zjn-wsc-ywh-amx/practice/tree/master/SM3) |        |        |        |        |
| 3        | Implement length extension attack for SM3, SHA256, etc       | [SM3_Length_Extension_Attack](https://github.com/zjn-wsc-ywh-amx/practice/tree/master/SM3_Length_Extension_Attack) |        |        |        |        |
| 4        | Do your best to optimize SM3 implementation (software)       | [sm3](https://github.com/zjn-wsc-ywh-amx/practice/tree/master/sm3) （基础实现）\\ [sm3_SMID](https://github.com/zjn-wsc-ywh-amx/practice/tree/master/sm3_SMID)（优化和的sm3） |        |        |        |        |
| 5        | Impl Merkle Tree following RFC6962                           | [Merkle](https://github.com/zjn-wsc-ywh-amx/practice/tree/master/Merkle) |        |        |        |        |
| 6        | Try to Implement this scheme                                 |                                                              |        |        |        |        |
|          | ***SM2***                                                    |                                                              |        |        |        |        |
| 7        | Report on the application of this deduce technique in Ethereum with ECDSA | [ECDSA_Deduce_publickey](https://github.com/zjn-wsc-ywh-amx/practice/tree/master/ECDSA_Deduce_publickey) |        |        |        |        |
| 8        | Impl sm2 with RFC6979                                        | [impl_sm2_with_RFC6979](https://github.com/zjn-wsc-ywh-amx/practice/tree/master/impl_sm2_with_RFC6979) |        |        |        |        |
| 9        | Verify the above pitfalls with proof-of-concept code         | [pitfalls](https://github.com/zjn-wsc-ywh-amx/practice/tree/master/pitfalls) |        |        |        |        |
| 10       | Implement the above ECMH scheme                              | [UTXOcommit hash](https://github.com/zjn-wsc-ywh-amx/practice/tree/master/UTXOcommit hash) |        |        |        |        |
| 11       | Implement a PGP scheme with SM2                              | [PGP in SM2](https://github.com/zjn-wsc-ywh-amx/practice/tree/master/PGP in SM2) |        |        |        |        |
| 12       | Implement sm2 2P sign with real network communication        | [sm2_2P__SIG](https://github.com/zjn-wsc-ywh-amx/practice/tree/master/sm2_2P__SIG) |        |        |        |        |
| 13       | Implement sm2 2P decrypt with real network communication     | [2P_decrypt](https://github.com/zjn-wsc-ywh-amx/practice/tree/master/2P_decrypt) |        |        |        |        |
|          | ***Bitcoin***                                                |                                                              |        |        |        |        |
| 14       | PoC impl of the scheme, or do implement analysis by Google   |                                                              |        |        |        |        |
| 15       | Send a tx on Bitcoin testnet, and parse the tx data down to every bit, better write script yourself | [比特币交易分析](https://github.com/zjn-wsc-ywh-amx/practice/tree/master/比特币交易分析) |        |        |        |        |
| 16       | Forge a signature to pretend that you are Satoshi            | [Forged_Satoshi_Signature](https://github.com/zjn-wsc-ywh-amx/practice/tree/master/Forged_Satoshi_Signature) |        |        |        |        |
|          | ***Ethereum***                                               |                                                              |        |        |        |        |
| 17       | Research report on MPT                                       | [MPT_report](https://github.com/zjn-wsc-ywh-amx/practice/tree/master/MPT_report) |        |        |        |        |
|          | ***Real Hash Cryptanalysis***                                |                                                              |        |        |        |        |
| 18       | Find a key with hash value `sdu_cst_20220610` under a message composed of your name followed by your student ID. For example, `San Zhan 202000460001` |                                                              |        |        |        |        |
| 19       | Find a 64-byte message under some k fulfilling that their hash value is symmetrical |                                                              |        |        |        |        |
|          | ***Zero Knowledge***                                         |                                                              |        |        |        |        |
| 20.1     | Write a circuit to prove that your CET6 grade is larger than 425.（a. Your grade info is like `(cn_id, grade, year, sig_by_moe)`. These grades are published as commitments onchain by MoE. b. When you got an interview from an employer, you can prove to them that you have passed the exam without letting them know the exact grade.） |                                                              |        |        |        |        |
| 20.2     | The commitment scheme used by MoE is SHA256-based.（`commit` = `SHA256(cn_id, grade, year, sig_by_moe, r)`） |                                                              |        |        |        |        |
|          | ***SM4***                                                    |                                                              |        |        |        |        |
| 21       | Impl sm4（基础实现）                                         | [SM4_](https://github.com/zjn-wsc-ywh-amx/practice/tree/master/SM4_) |        |        |        |        |
| 22       | Impl sm4（t_table）                                          | [SM4_](https://github.com/zjn-wsc-ywh-amx/practice/tree/master/SM4_) |        |        |        |        |
| 23       | Impl sm4（SIMD)                                              | [SM4_](https://github.com/zjn-wsc-ywh-amx/practice/tree/master/SM4_) |        |        |        |        |

其中：

- ✅：独立完成项目；
- 🟢：合作完成项目；
- <留空>：未完成项目。