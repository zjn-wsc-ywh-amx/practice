#include <stdio.h>
#include "sm4_f.h"
#include<math.h>
#include <intrin.h>  
#include<windows.h>

#define u8 unsigned char
#define u32 unsigned int
/*
	测试数据：
	明文：	01234567 89abcdef fedcba98 76543210
	密钥：	01234567 89abcdef fedcba98 76543210
	密文：	681edf34 d206965e 86b3e94f 536e4246
*/
/*
int main(void) 
{
	u32 X[4]; // 明文 
	u32 DX[4] = { 0 };//解密
	u32 MK[4]; // 密钥 
	u32 RK[32]; // 轮密钥  
	u32 Y[4]; // 密文 
	X[0] = 0x01234567; X[1] = 0x89abcdef;
	X[2] = 0xfedcba98; X[3] = 0x76543210;
	MK[0] = 0x01234567; MK[1] = 0x89abcdef;
	MK[2] = 0xfedcba98; MK[3] = 0x76543210;
	//正常方法
	GetRK(MK, RK);
	encryptSM4(X, RK, Y);
	printf("****************正常计算结果为：**********\n");
	printf("%08x %08x %08x %08x\n", Y[0], Y[1], Y[2], Y[3]);

	//T_table方法

	int flag = 1;
	while (1)
	{
		if (flag == 1)
		{
			//计算每一个表
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


	//解密验证
	decryptSM4(Y, RK, DX);
	printf("****************解密计算结果为：**********\n");
	printf("%08x %08x %08x %08x\n", DX[0], DX[1], DX[2], DX[3]);
	return 0;
}*/
int main()
{
	
	
	/*SIMD加速优化对比*/
	__declspec(align(16)) u32 X1[4], X2[4], X3[4],X4[4]; // 明文 
	__declspec(align(16)) u32 MK1[4], MK2[4], MK3[4], MK4[4]; // 密钥 
	__declspec(align(16)) u32 RK1[32], RK2[32], RK3[32], RK4[32]; // 轮密钥  
	__declspec(align(16)) u32 Y1[4], Y2[4], Y3[4], Y4[4]; // 密文 
	//初始化
	X1[0] = 0x10234567; X1[1] = 0x89abcdef;X1[2] = 0xfedcba98; X1[3] = 0x76543210;
	X2[0] = 0x10134567; X2[1] = 0x98abcdef;X2[2] = 0xefdcba98; X2[3] = 0x77543210;
	X3[0] = 0x10324567; X3[1] = 0x89bacdef;X3[2] = 0xfecdba98; X3[3] = 0x66453210;
	X4[0] = 0x10235467; X4[1] = 0x89abdcef;X4[2] = 0xfedcab98; X4[3] = 0x76542310;
	MK1[0] = 0x10234567; MK1[1] = 0x89abcdef;MK1[2] = 0xfedcba98; MK1[3] = 0x76543210;
	MK2[0] = 0x20134567; MK2[1] = 0x98abcdef;MK2[2] = 0xefdcba98; MK2[3] = 0x67543210;
	MK3[0] = 0x10324567; MK3[1] = 0x89bacdef;MK3[2] = 0xfecdba98; MK3[3] = 0x76453210;
	MK4[0] = 0x10235467; MK4[1] = 0x89abdcef;MK4[2] = 0xfedcab98; MK4[3] = 0x76542310;


	GetRK(MK1, RK1);
	GetRK(MK2, RK2);
	GetRK(MK3, RK3);
	GetRK(MK4, RK4);
	

	double run_time1 =0, run_time2 = 0;//运行时间 
	LARGE_INTEGER Frequency;//计数器频率 
	LARGE_INTEGER start_PerformanceCount;//起始计数器  
	LARGE_INTEGER end_PerformanceCount;//结束计数器  
	//
	
	QueryPerformanceFrequency(&Frequency);
	QueryPerformanceCounter(&start_PerformanceCount);
	
	encryptSM4(X1, RK1, Y1);
	encryptSM4(X2, RK2, Y2);
	encryptSM4(X3, RK3, Y3);
	encryptSM4(X4, RK4, Y4);

	QueryPerformanceCounter(&end_PerformanceCount);
	run_time1= (end_PerformanceCount.QuadPart - start_PerformanceCount.QuadPart) / (double)Frequency.QuadPart;
	printf("正常计算时间为：%e\n", run_time1);

	printf("****************计算结果为：**********\n");
	printf("%08x %08x %08x %08x\n", Y1[0], Y1[1], Y1[2], Y1[3]);
	printf("%08x %08x %08x %08x\n", Y2[0], Y2[1], Y2[2], Y2[3]);
	printf("%08x %08x %08x %08x\n", Y3[0], Y3[1], Y3[2], Y3[3]);
	printf("%08x %08x %08x %08x\n", Y4[0], Y4[1], Y4[2], Y4[3]);
	//

	QueryPerformanceFrequency(&Frequency);
	QueryPerformanceCounter(&start_PerformanceCount);

	encrypt_simd( X1,  X2,  X3,  X4,  RK1,  RK2,  RK3,  RK4 , Y1,  Y2, Y3, Y4);
	
	QueryPerformanceCounter(&end_PerformanceCount);
	run_time2= (end_PerformanceCount.QuadPart - start_PerformanceCount.QuadPart) / (double)Frequency.QuadPart;
	printf("SIMD计算时间为：%e\n", run_time2);
	
	
	printf("****************SIMD计算结果为：**********\n");
	printf("%08x %08x %08x %08x\n", Y1[0], Y1[1], Y1[2], Y1[3]);
	printf("%08x %08x %08x %08x\n", Y2[0], Y2[1], Y2[2], Y2[3]);
	printf("%08x %08x %08x %08x\n", Y3[0], Y3[1], Y3[2], Y3[3]);
	printf("%08x %08x %08x %08x\n", Y4[0], Y4[1], Y4[2], Y4[3]);
	
	return 0;
}


