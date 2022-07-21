#include <iostream>
#include<iomanip>
#include<stdio.h>
#include<time.h>
#define LEFT 0
#define RIGHT 1
using namespace std;
unsigned int IV[8] = {0x7380166f, 0x4914b2b9,0x172442d7 ,0xda8a0600 ,0xa96f30bc ,0x163138aa ,0xe38dee4d, 0xb0fb0e4e };
void sm3_init(unsigned int IV[])
{
   unsigned int  V[8] = {0x7380166f,0x4914b2b9,0x172442d7 ,0xda8a0600 ,0xa96f30bc ,0x163138aa ,0xe38dee4d, 0xb0fb0e4e };
   memcpy(IV, V, 32);
}
unsigned int shift(unsigned int val, int n, bool d)
{
    int size = sizeof(val) * 8;
    n = n % size;
    if (d)
        return (val << (size - n) | (val >> n));
    else
        return (val >> (size - n) | (val << n));//左移
}
int P0(int x)
{
    return x ^ (shift(x, 9, LEFT)) ^ (shift(x, 17, LEFT));
}
int P1(int x)
{
    return x ^ (shift(x, 15, LEFT)) ^ (shift(x, 23, LEFT));
}
int FF(unsigned int x, unsigned int y, unsigned int z, int j)
{
    if (j >= 0 && j <= 15)return x ^ y ^ z;
    if (j >= 16 && j <= 64)return (x & y) | (y & z) | (x & z);
}
int GG(unsigned int x, unsigned int y, unsigned int z, int j)
{
    if (j >= 0 && j <= 15)return x ^ y ^ z;
    if (j >= 16 && j <= 64)return (x & y) | (~x & z);
}
unsigned char* block_padding(unsigned char* msg, long long len)
{
    int lenth = len % 64;
    long long size = lenth > 57 ? 2 : 1;
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
    int size = mod > 57 ? 2 : 1;
    unsigned char* pmsg = new unsigned char[(mul + size) * 64];
    memcpy(pmsg, msg, mul * 64);
    memcpy(pmsg + mul * 64, tush = block_padding(msg + mul * 64, lenth), size * 64);
    free(tush);
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
        ex_msg[i] = P1(ex_msg[i - 16] ^ ex_msg[i - 9] ^ shift(ex_msg[i - 3], 15, LEFT)) ^ shift(ex_msg[i - 13], 7, LEFT) ^ ex_msg[i - 6];
    }
    for (int i = 0; i < 64; i++)
    {
        ex_msg[68 + i] = ex_msg[i] ^ ex_msg[i + 4];
    }
    return ex_msg;
}

void CF(unsigned int* ex_msg)
{

    unsigned int* reg = new unsigned int[8];//ABCDEFGH
    memcpy(reg, IV, 32);
    unsigned int SS1, SS2, TT1, TT2, T;
    for (int j = 0; j < 64; j++)
    {

        if (j <= 15)T = 0x79cc4519;
        else        T = 0x7a879d8a;
        SS1 = shift(shift(reg[0], 12, LEFT) + reg[4] + shift(T, j % 32, LEFT), 7, LEFT);
        SS2 = SS1 ^ shift(reg[0], 12, LEFT);
        TT1 = FF(reg[0], reg[1], reg[2], j) + reg[3] + SS2 + ex_msg[68 + j];
        TT2 = GG(reg[4], reg[5], reg[6], j) + reg[7] + SS1 + ex_msg[j];
        reg[3] = reg[2];
        reg[2] = shift(reg[1], 9, LEFT);
        reg[1] = reg[0];
        reg[0] = TT1;
        reg[7] = reg[6];
        reg[6] = shift(reg[5], 19, LEFT);
        reg[5] = reg[4];
        reg[4] = P0(TT2);
    }
    for (int i = 0; i < 8; i++)
    {
        IV[i] = reg[i] ^ IV[i];
    }
    free(ex_msg);
}

unsigned int* sm3(unsigned char* msg, long long lenth)
{
    sm3_init(IV);
   // cout << "sm3 Hash Val:  ";
    unsigned char* temp = msg_padding(msg, lenth);
    unsigned int* m;
    int block_num = (lenth / 64) + (lenth % 64 > 57 ? 2 : 1);
    for (int i = 0; i < block_num; i++)
    {
        m = msg_ex(temp + i * 64);
        CF(m);
    }
   for (int i = 0; i < 8; i++)
        cout << setfill('0') << setw(8) << hex << IV[i];
    cout << endl;
    return NULL;
}
int main()
{
    //example 1
    unsigned char msg1[64] = { 0x61,0x62,0x63,0x64,0x61,0x62,0x63,0x64, 0x61,0x62,0x63,0x64, 0x61,0x62,0x63,0x64, 0x61,0x62,0x63,0x64, 0x61,0x62,0x63,0x64, 0x61,0x62,0x63,0x64, 0x61,0x62,0x63,0x64, 0x61,0x62,0x63,0x64, 0x61,0x62,0x63,0x64, 0x61,0x62,0x63,0x64, 0x61,0x62,0x63,0x64, 0x61,0x62,0x63,0x64, 0x61,0x62,0x63,0x64, 0x61,0x62,0x63,0x64, 0x61,0x62,0x63,0x64 };//左边数的高位 右边是低位
    //example 2
    unsigned char msg2[3] = { 0x61,0x62,0x63 };
    unsigned char msg3[6] = "12223";
    time_t sta, end;
    sta = clock();
    for(int i=0;i<1000000;i++)
    sm3(msg2, sizeof(msg2));
    end = clock();
    cout << "time :" << double(end - sta) / CLOCKS_PER_SEC << endl;
}
