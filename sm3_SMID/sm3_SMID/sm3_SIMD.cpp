#include <iostream>
#include<iomanip>
#include<stdio.h>
#include<time.h>
#include <immintrin.h>
#include <xmmintrin.h>
#include <intrin.h> 
using namespace std;
__m256i IV ;
void _mm256_print_epi32(__m256i p) {
    int* p1 = (int*)&p;
    printf("%x %x %x %x %x %x %x %x\n", p1[0], p1[1], p1[2], p1[3], p1[4], p1[5], p1[6], p1[7]);
};
void sm3_init(__m256i& IV)
{
  IV= _mm256_setr_epi32(0x7380166f, 0x4914b2b9, 0x172442d7, 0xda8a0600, 0xa96f30bc, 0x163138aa, 0xe38dee4d, 0xb0fb0e4e);
}
unsigned int shift(unsigned int val, int n)
{
    n = n % 32;
    return (val >> (32 - n) | (val << n));//左移
}
//int P0(int x)
//{
//    return x ^ (shift(x, 9 )) ^ (shift(x, 17 ));
//}
unsigned int P1(unsigned int x)
{
    return (x^ ((x >>17) | (x<< 15)) ^ ((x >> 9) | (x << 23)));
}
//int FF(unsigned int x, unsigned int y, unsigned int z, int j)
//{
//    if (j >= 0 && j <= 15)return x ^ y ^ z;
//    if (j >= 16 && j <= 64)return (x & y) | (y & z) | (x & z);
//}
//int GG(unsigned int x, unsigned int y, unsigned int z, int j)
//{
//    if (j >= 0 && j <= 15)return x ^ y ^ z;
//    if (j >= 16 && j <= 64)return (x & y) | (~x & z);
//}
unsigned char* block_padding(unsigned char* msg, long long len)
{
    int lenth = len % 64;
    long long size = lenth > 56 ? 2 : 1;
    unsigned char* padmsg = new unsigned char[size * 64];
    memcpy(padmsg, msg, lenth);
    padmsg[lenth] = 0x80;
    memset(padmsg + lenth + 1, 0, size * 64 - lenth - 1);
    len *= 8;
    for (int i = size * 64 - 1; i > size * 64 - 8; i--)
    {
        padmsg[i] = len & 0x000000FF;
        len >>= 8;
    }
    return padmsg;
}

unsigned char* msg_padding(unsigned char* msg, long long lenth)
{
    long long mul, mod;
    unsigned char* tush;
    mul = lenth / 64;
    mod = lenth % 64;
    int size = mod > 55 ? 2 : 1;
    unsigned char* pmsg = new unsigned char[(mul + size) * 64];
    memcpy(pmsg, msg, mul * 64);
    memcpy(pmsg + mul * 64, tush = block_padding(msg + mul * 64, lenth), size * 64);
    delete[] tush;
    return pmsg;
}


unsigned int* msg_ex(unsigned char* block)
{
    
    unsigned int* ex_msg = new unsigned int[132];
    memcpy(ex_msg, block, 64);
    for (int i = 0; i < 16; i++)
    {
        ex_msg[i] = _byteswap_ulong(ex_msg[i]);
    }
    for (int i = 16; i < 68; i++)
    {
        ex_msg[i] = P1(ex_msg[i - 16] ^ ex_msg[i - 9] ^ shift(ex_msg[i - 3], 15 )) ^ shift(ex_msg[i - 13], 7 ) ^ ex_msg[i - 6];
    }
    for (int i = 0; i < 64; i++)
    {
        ex_msg[68 + i] = ex_msg[i] ^ ex_msg[i + 4];
    }
    return ex_msg;
}

void CF(unsigned int* ex_msg)
{
    unsigned int reg[8];//ABCDEFGH
    memcpy(reg, &IV, 32);
   // for (int i = 0; i < 8; i++)printf("%x   ", reg[i]);
   // printf("\n");
    unsigned int SS1, SS2, TT1, TT2, T;
    unsigned int p0r4p3_add;
    unsigned int* p;
    __m128i R015C, R015C_snum;
    for (int j = 0; j < 16; j++)
    {
         R015C = _mm_set_epi32(0x79cc4519, reg[5], reg[1], reg[0]);
         R015C_snum = _mm_set_epi32(j, 19, 9, 12);
        R015C = _mm_rolv_epi32(R015C, R015C_snum);
        p = (unsigned int*)&R015C;
        p0r4p3_add = p[0] + reg[4] + p[3];
        SS1 = p0r4p3_add << 7 | p0r4p3_add >> 25;
        SS2 = SS1 ^ p[0];
        TT1 = (reg[0] ^ reg[1] ^ reg[2]) + reg[3] + SS2 + ex_msg[68 + j];
        TT2 = (reg[4] ^ reg[5] ^ reg[6]) + reg[7] + SS1 + ex_msg[j];
        //__m256i R =_mm256_set_m128i(R0_3,R4_7);
        reg[3] = reg[2];
        reg[2] = p[1];
        reg[1] = reg[0];
        reg[0] = TT1;
        reg[7] = reg[6];
        reg[6] = p[2];
        reg[5] = reg[4];
        reg[4] = TT2 ^ (TT2 << 9 | TT2 >> 23) ^ (TT2 << 17 | TT2 >> 15);
    }
    for (int j = 16; j < 64; j++)
    {
        R015C = _mm_set_epi32(0x7a879d8a, reg[5], reg[1], reg[0]);
        R015C_snum = _mm_set_epi32(j%32, 19, 9, 12);
        R015C = _mm_rolv_epi32(R015C, R015C_snum);
        p = (unsigned int*)&R015C;
        p0r4p3_add = p[0] + reg[4] + p[3];
        SS1 = p0r4p3_add << 7 | p0r4p3_add >> 25;
        SS2 = SS1 ^ p[0];
        TT1 = ((reg[0] & reg[1]) | (reg[1] & reg[2]) | (reg[0] & reg[2])) + reg[3] + SS2 + ex_msg[68 + j];
        TT2 = ((reg[4] & reg[5]) | (~reg[4] & reg[6])) + reg[7] + SS1 + ex_msg[j];
        reg[3] = reg[2];
        reg[2] = p[1];
        reg[1] = reg[0];
        reg[0] = TT1;
        reg[7] = reg[6];
        reg[6] = p[2];
        reg[5] = reg[4];
        reg[4] = TT2 ^ (TT2 << 9 | TT2 >> 23) ^ (TT2 << 17 | TT2 >> 15);
    }
    __m256i R = _mm256_loadu_epi32(reg);//异或
    IV=_mm256_xor_epi32(IV, R);
    delete[] ex_msg;
}

unsigned int* sm3(unsigned char* msg, long long lenth)
{

    sm3_init(IV);
    // cout << "sm3 Hash Val:  ";
    unsigned char* temp = msg_padding(msg, lenth);
    unsigned int* tush=NULL;
    int block_num = (lenth / 64) + (lenth % 64 > 57 ? 2 : 1);
    for (int i = 0; i < block_num; i++)
    {
        CF (tush=msg_ex(temp + i * 64));
    }
    delete[] temp;
    return NULL;
}

int main()
{
    //example 1
    unsigned char msg1[64] = { 0x61,0x62,0x63,0x64,0x61,0x62,0x63,0x64, 0x61,0x62,0x63,0x64, 0x61,0x62,0x63,0x64, 0x61,0x62,0x63,0x64, 0x61,0x62,0x63,0x64, 0x61,0x62,0x63,0x64, 0x61,0x62,0x63,0x64, 0x61,0x62,0x63,0x64, 0x61,0x62,0x63,0x64, 0x61,0x62,0x63,0x64, 0x61,0x62,0x63,0x64, 0x61,0x62,0x63,0x64, 0x61,0x62,0x63,0x64, 0x61,0x62,0x63,0x64, 0x61,0x62,0x63,0x64 };//左边数的高位 右边是低位
    //example 2
    unsigned char msg2[3] = { 0x61,0x62,0x63 };
    time_t sta, end;
    for (int i = 0; i < 1000000; i++)//预热
        sm3(msg2, 3);
    sta = clock();
    for (int i = 0; i < 1000000; i++)
        sm3(msg2, 3);
    end = clock();
    _mm256_print_epi32(IV);
    cout << "一百万次sm3运行时间 time :" << double(end - sta) / CLOCKS_PER_SEC <<"s" << endl;
}
