#include <stdio.h>
#include "sm4_f.h"
#include<math.h>
#define u8 unsigned char
#define u32 unsigned int
/*
	测试数据：
	明文：	01234567 89abcdef fedcba98 76543210
	密钥：	01234567 89abcdef fedcba98 76543210
	密文：	681edf34 d206965e 86b3e94f 536e4246
*/

int main(void) {
	u32 X[4]; // 明文 
	u32 DX[4] = { 0 };
	u32 MK[4]; // 密钥 
	u32 RK[32]; // 轮密钥  
	u32 Y[4]; // 密文 
	X[0] = 0x01234567; X[1] = 0x89abcdef;
	X[2] = 0xfedcba98; X[3] = 0x76543210;
	MK[0] = 0x01234567; MK[1] = 0x89abcdef;
	MK[2] = 0xfedcba98; MK[3] = 0x76543210;
	GetRK(MK, RK);
	encryptSM4(X, RK, Y);
	printf("****************正常计算结果为：**********\n");
	printf("%08x %08x %08x %08x\n", Y[0], Y[1], Y[2], Y[3]);

	int flag = 1;
	while (1)
	{
		if (flag == 1)
		{
			/*计算每一个表*/
			for (u32 i = 0; i < SIZE; i++)
			{
				t1_table[i] = T(i << 24);
				t2_table[i] = T(i << 16);
				t3_table[i] = T(i << 8);
				t4_table[i] = T(i);
			}
			flag += 1;
			printf("计算T_table完成\n");
		}
		else
		{
			GetRK(MK, RK);
			encryptSM4_t_table(X, RK, Y);
			printf("****************T_table计算结果为：**********\n");
			printf("%08x %08x %08x %08x\n", Y[0], Y[1], Y[2], Y[3]);
			break;
		}


	}

	decryptSM4(Y, RK, DX);
	printf("****************解密计算结果为：**********\n");
	printf("%08x %08x %08x %08x\n", DX[0], DX[1], DX[2], DX[3]);
	return 0;
	
}


