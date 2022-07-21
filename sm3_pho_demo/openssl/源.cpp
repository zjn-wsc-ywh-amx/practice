extern "C"
{
#include <openssl/applink.c>
};
#include <stdio.h>
#include <openssl/evp.h>
#include <openssl/bio.h>
#include<time.h>
#include<iostream>
#include<random>
#define lenth 3//攻击长度
unsigned char* sm3(unsigned char* msg)
{
   EVP_MD_CTX* ctx = NULL;
   EVP_MD* SM3 = NULL;
   unsigned int len = 0;
   unsigned char* outdigest = NULL;
    unsigned char *ret=(unsigned char*)malloc(32*sizeof(unsigned char*));
    /* Create a context for the digest operation */
    ctx = EVP_MD_CTX_new();
    if (ctx == NULL)
        goto err;
    SM3 = EVP_MD_fetch(NULL, "SM3", NULL);
    if (SM3 == NULL)
        goto err;
    if (!EVP_DigestInit_ex(ctx, SM3, NULL))
        goto err;
    if (!EVP_DigestUpdate(ctx, msg, sizeof(msg)))
        goto err;
    outdigest = (unsigned char*)OPENSSL_malloc(EVP_MD_get_size(SM3));
    if (outdigest == NULL)
        goto err;
    if (!EVP_DigestFinal_ex(ctx, outdigest, &len))
        goto err;
     for (int i = 0; i < 32; i++)
    {
         ret[i] = outdigest[i];
    }

err:
    EVP_MD_free(SM3);
    EVP_MD_CTX_free(ctx);
    OPENSSL_free(outdigest);
    //std::cout << "error";
    return ret;
}
void birthday_attack()
{
    int count = 0;
    unsigned char m[10000] = "12332134124";
    unsigned char* temp_,*temp;
    unsigned char* temp1;
    unsigned char btemp[32], btemp1[32];
    unsigned char* tush;
    //const unsigned char r[] = "123";
   EVP_MD* SM3 = NULL;
   temp = (unsigned char*)malloc(32 * sizeof(unsigned char));
   temp_ = sm3(m);
   temp1 = (unsigned char *)malloc(32*sizeof(unsigned char));
   memcpy(temp1, temp_, lenth);
   memcpy(temp, temp_, lenth);
   while(++count){
    int f = 0;
    memcpy(btemp, temp, lenth);
    memcpy(temp, tush=sm3(btemp), 32);
    free(tush);
    memcpy(btemp, temp, lenth);
    memcpy(temp, tush=sm3(btemp), 32);
    free(tush);
    memcpy(btemp1,temp1,lenth);
    memcpy(temp1, tush=sm3(btemp1), 32);
    free(tush);
   for (int i = 0; i <lenth; i++)
   {
       if (temp[i] != temp1[i]) goto flag;
   }
   for (int i = 0; i < lenth; i++)
   {
       if (btemp[i] == btemp1[i]);
       else f=1;
   }
   if (!f) {
       int a, b;
       a = rand() % 11;
       b = rand() % 64;
       m[a] = b;
       temp_ = sm3(m);
       memcpy(temp1, temp_, lenth);
       memcpy(temp, temp_, lenth);
       goto flag;
   }
   printf("前%dbits sm4碰撞：\n",lenth*8);
   for (int i = 0; i < 32; i++)
   {
       printf("%02hx", btemp[i]);
   }
   printf("\n");
   for (int i = 0; i < 32; i++)
   {
       printf("%02hx", temp[i]);
   }
   printf("\n");
   for (int i = 0; i < 32; i++)
   {
       printf("%02hx", btemp1[i]);
   }
   printf("\n");
   for (int i = 0; i < 32; i++)
   {
       printf("%02hx", temp1[i]);
   }
   printf("\n");
   printf("%d", count);
 
   break;
flag:
   {
       //free(btemp);
       //free(btemp1);
       continue;

   }
   
   }
}
void  benchsm3()
{
    time_t sta, end;
    unsigned char  m[] = "12223";
    sta = clock();
    for (int i = 0; i < 1000000; i++)
    {
      
        sm3(m);
    }
    end = clock();
    std::cout << double(end - sta) / CLOCKS_PER_SEC << "s" <<std:: endl;
}
int main(void)
{
    birthday_attack();
    //benchsm3();
}