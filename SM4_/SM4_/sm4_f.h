#include "sm4_table.h"
#include <intrin.h>  
#include<windows.h>


u32 T1(u32 m)/*密钥生成函数*/
{
	u8 s[4];
	u32 res = 0;
	for (int i = 0; i < 4; i++)
	{
		s[i] = m >> (24 - i * 8);
		s[i] = Sbox[s[i] >> 4][s[i] & 0x0f];
		res |= s[i] << (24 - i * 8);
	}
	return res ^ (((res << 13) | (res >> 19)) & num) ^ (((res << 23) | (res >> 9)) & num);
}
void GetRK(u32 MK[], u32 RK[]) {
	u32 k[36] = { 0 };
	int i;
	for (i = 0; i < 4; i++)k[i] = MK[i] ^ FK[i];
	for (i = 0; i < 32; i++)
	{
		k[i + 4] = k[i] ^ T1(k[i + 1] ^ k[i + 2] ^ k[i + 3] ^ CK[i]);
		RK[i] = k[i + 4];
	}
}




u32 T(u32 m)
{
	u8 s[4] = { 0 };
	u32 res = 0;
	u32 r = 0;
	u32 l = 0;

	for (int i = 0; i < 4; i++)
	{
		s[i] = m >> (24 - i * 8);
		r = s[i] >> 4;
		l = s[i] & 0x0f;
		s[i] = Sbox[r][l];
		res |= s[i] << (24 - i * 8);
	}
	return res ^ (((res << 2) | (res >> 30)) & num) ^ (((res << 10) | (res >> 22)) & num) ^ (((res << 18) | (res >> 14)) & num) ^ (((res << 24) | (res >> 8)) & num);
}
/*
	加密算法
	参数：	u32 X[4]：明文    u32 RK[32]：轮密钥    u32 Y[4]：密文，保存结果
	返回值：无
*/
void encryptSM4(u32 X[4], u32 RK[32], u32 Y[4]) {
	short i;
	u32 x[36] = { 0 };
	x[0] = X[0];
	x[1] = X[1];
	x[2] = X[2];
	x[3] = X[3];
	u32 t;
	
	for (i = 0; i < 32; i++) {
		t = x[i + 1] ^ x[i + 2] ^ x[i + 3] ^ RK[i];
		x[i + 4] = x[i] ^ T(t);
	}
	for (i = 0; i < 4; i++) {
		Y[i] = x[35 - i];
	}
}

/*
	解密算法
	参数： 	u32 X[4]：密文    u32 RK[32]：轮密钥    u32 Y[4]：明文，保存结果
	返回值：无
*/
void decryptSM4(u32 X[4], u32 RK[32], u32 Y[4]) {
	short i;
	u32 x[36] = { 0 };
	x[0] = X[0];
	x[1] = X[1];
	x[2] = X[2];
	x[3] = X[3];
	u32 t;

	for (i = 0; i < 32; i++)
	{
		t = x[i + 1] ^ x[i + 2] ^ x[i + 3] ^ RK[31 - i];
		x[i + 4] = x[i] ^ T(t);
	}
	for (i = 0; i < 4; i++)
	{
		Y[i] = x[35 - i];
	}
}
void encryptSM4_t_table(u32 X[4], u32 RK[32], u32 Y[4])
{
	u32 x[36] = { 0 };
	x[0] = X[0];
	x[1] = X[1];
	x[2] = X[2];
	x[3] = X[3];
	for (int i = 0; i < 32; i++) {
		u32 t = x[i + 1] ^ x[i + 2] ^ x[i + 3] ^ RK[i];
		u32 s1 = (t&0xff000000)>>24;
		u32 s2 = (t&0x00ff0000)>>16;
		u32 s3 = (t&0x0000ff00)>>8;
		u32 s4 = (t&0x000000ff);
		x[i + 4] = t1_table[s1] ^ t2_table[s2] ^ t3_table[s3] ^ t4_table[s4];
		printf("x[%d]:%x", i, x[i + 4]);
	}
	for (int i = 0; i < 4; i++) {
		Y[i] = x[35 - i];
	}
}
void encrypt_simd(u32 X1[4], u32 X2[4], u32 X3[4], u32 X4[4], u32 RK1[32], u32 RK2[32], u32 RK3[32], u32 RK4[32], u32 Y1[4], u32 Y2[4], u32 Y3[4], u32 Y4[4])
{
	short i;
	u32 x1[36] = { 0 }; u32 x2[36] = { 0 }; u32 x3[36] = { 0 }; u32 x4[36] = { 0 };
	printf("x3:%x\n", X3[3]);
	x1[0] = X1[0]; x1[1] = X1[1]; x1[2] = X1[2]; x1[3] = X1[3];
	x2[0] = X2[0]; x2[1] = X2[1]; x2[2] = X2[2]; x2[3] = X2[3];
	x3[0] = X3[0]; x3[1] = X3[1]; x3[2] = X3[2]; x3[3] = X3[3];
	x4[0] = X4[0]; x4[1] = X4[1]; x4[2] = X4[2]; x4[3] = X4[3];
	__m128i M1, M2, M3, M4;
	__m128i K1, K2;
	unsigned int tmpC1[4],tmpC2[4];
	for (i = 0; i < 32; i++) {
		M1 = _mm_set_epi32(x4[i+1], x3[i+1], x2[i+1], x1[i+1]);
		M2 = _mm_set_epi32(x4[i+2], x3[i+2], x2[i+2], x1[i+2]);
		M3 = _mm_set_epi32(x4[i+3], x3[i+3], x2[i+3], x1[i+3]);
		M4 = _mm_set_epi32(RK4[i], RK3[i], RK2[i],RK1[i]);
		


		__m128i N1 = _mm_xor_epi32(M1, M2);
		unsigned int tmpC[4];
		_mm_store_si128((__m128i*)(tmpC), N1);
	

		__m128i N2 = _mm_xor_epi32(M3, M4);
	
		__m128i N3 = _mm_xor_si128(N1, N2);
		
		_mm_store_si128((__m128i*)(tmpC1), N3);
	
		u32 k1 = T(tmpC1[0]);
		u32 k2 = T(tmpC1[1]);
		u32 k3 = T(tmpC1[2]);
		u32 k4 = T(tmpC1[3]);
	
		
		K1 = _mm_set_epi32(x4[i], x3[i], x2[i], x1[i]);
		K2= _mm_set_epi32(k4, k3, k2, k1);
		
		__m128i K3= _mm_xor_epi32(K1, K2);
		
		_mm_store_si128((__m128i*)(tmpC2), K3);

		x1[i + 4] = tmpC2[0];
		x2[i + 4] = tmpC2[1];
		x3[i + 4] = tmpC2[2];
		x4[i + 4] = tmpC2[3];
	}
		for (i = 0; i < 4; i++) 
		{
			Y1[i] = x1[35 - i];
			Y2[i] = x2[35 - i];
			Y3[i] = x3[35 - i];
			Y4[i] = x4[35 - i];
		}
	}




