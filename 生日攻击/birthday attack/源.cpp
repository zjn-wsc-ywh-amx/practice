#include <stdio.h>
#include <string.h>
#include "sm3hash.h"
#include "openssl/evp.h"
#include "sm3hash.h"
#include<iostream>


using namespace std;

unsigned char hash_value_static[64];
int flag = 0;
int times = 1;

int sm3_hash(const unsigned int* message, size_t len, unsigned char* hash, unsigned int* hash_len)
{
	EVP_MD_CTX* md_ctx;
	const EVP_MD* md;

	md = EVP_sm3();
	md_ctx = EVP_MD_CTX_new();
	EVP_DigestInit_ex(md_ctx, md, NULL);
	EVP_DigestUpdate(md_ctx, message, len);
	EVP_DigestFinal_ex(md_ctx, hash, hash_len);
	EVP_MD_CTX_free(md_ctx);
	return 0;
}
void birthday_attack()
{
	unsigned int sample1[256] = {};
	for (int i = 0; i < 256; i++)
	{
		sample1[i] = rand();
	}
	unsigned int sample1_len = strlen((char*)sample1);
	unsigned char hash_value[64];
	unsigned int i, hash_len;

	sm3_hash(sample1, sample1_len, hash_value, &hash_len);
	printf("raw data: %s\n", sample1);
	printf("hash length: %d bytes.\n", hash_len);
	printf("hash value:\n");
	for (i = 0; i < hash_len; i++)
	{
		printf("0x%x  ", hash_value[i]);
		if (flag == 1)
		{
			for (i = 0; i < hash_len; i++)
			{
				hash_value_static[i] = hash_value[i]; /////第一次的hash值
			}

		}
		
		if (flag > 1)
		{
			hash_value_static[i] = hash_value[i]^ hash_value_static[i];  ///之后的每一次和前一次做异或
		}

		flag++;
	}
	cout << "第" << times << "次";
	
	
	if (hash_value_static == 0)
	{
		return;
	}

	if (hash_value_static != 0)
	{
		//for (i = 0; i < hash_len; i++)
		//{
		//	cout << hash_value_static[i];
		//}

		times++;
		birthday_attack();
	}
	else
	{
		return;
	}
}

int main(void)
{
	birthday_attack();
	
	
	return 0;
}