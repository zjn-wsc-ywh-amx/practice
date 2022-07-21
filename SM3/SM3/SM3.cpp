#include <stdio.h>
#include <string.h>
#include "openssl/evp.h"
#include "sm3hash.h"
#include<iostream>


using namespace std;

unsigned char hash_value_static[64];
int flag = 0;
int times = 1;

int sm3_hash(const unsigned char* message, size_t len, unsigned char* hash, unsigned int* hash_len)
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
void pollard_rho_attack()
{
	unsigned char sample[] = { 0x61, 0x62, 0x63, 0x64, 0x61, 0x62, 0x63, 0x64,
							0x61, 0x62, 0x63, 0x64, 0x61, 0x62, 0x63, 0x64,
							0x61, 0x62, 0x63, 0x64, 0x61, 0x62, 0x63, 0x64,
							0x61, 0x62, 0x63, 0x64, 0x61, 0x62, 0x63, 0x64 };
	//unsigned char hash_value[8];
	unsigned int sample_len = sizeof(sample);
	cout << sample_len << endl;
	unsigned int hash_len ;
	
	unsigned char a[32];
	unsigned char b[32];
	unsigned char t[32];

	sm3_hash(sample, sample_len, a, &hash_len);
	//cout << hash_len << endl;
	sm3_hash(a, sample_len, b, &hash_len);

	while (1)
	{
		int count = 0;
		for (int i = 0; i < 2; i++)
		{
			if (a[i] != b[i])
			{
				break;
			}
			else
				count++;
		}
		if (count == 2)
		{
			printf("0x");
			for (int i = 0; i < sample_len; i++)
			{
				printf("%x", a[i]);
			}
			printf("\n0x");
			for (int i = 0; i < sample_len; i++)
			{
				printf("%x", b[i]);
			}
			printf("\n的前16位hash值相同，即找到了碰撞\n");
			break;
		}
		sm3_hash(a, sample_len, t, &hash_len);

		for (int i = 0; i < hash_len; i++)
		{
			a[i] = t[i];
		}

		sm3_hash(b, sample_len, t, &hash_len);

		sm3_hash(t, sample_len, b, &hash_len);

	}

	
}
int main()
{
	pollard_rho_attack();
	return 0;
}