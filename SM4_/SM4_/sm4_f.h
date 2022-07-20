#include "sm4_table.h"


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
		printf("x[%d]:%x", i,x[i+4]);
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



