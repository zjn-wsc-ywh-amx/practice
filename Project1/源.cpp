#include <stdio.h>
#include <string.h>
#include <openssl/evp.h>
#define MAX 1024
 char sm3_tables[MAX][MAX];
int order_number = 0;

void sm3_rho_method(unsigned char input[])
{
	if (order_number > 500)
	{
		FILE* fp;
		if ((fp = fopen("sm3_2.txt", "wb")) == NULL)
		{
			printf("cant open the file");
			exit(0);
		}
		for (int i = 0; i < 500; i++)
		{
			for (int j = 0; j < 16; j++) {
				fprintf(fp, "%c ", sm3_tables[i][j]);
			}
		}
		fclose(fp);
		return;
	}
	unsigned char sm3_value[EVP_MAX_MD_SIZE];
	unsigned int sm3_len, i;
	EVP_MD_CTX* sm3ctx;						
	sm3ctx = EVP_MD_CTX_new();
	//char msg1[] = "20191315";			
	//char msg2[] = "Test Message2";			

	EVP_MD_CTX_init(sm3ctx);					
	EVP_DigestInit_ex(sm3ctx, EVP_sm3(), NULL);	
	EVP_DigestUpdate(sm3ctx, input, strlen( (const char *) input));
	
	EVP_DigestFinal_ex(sm3ctx, sm3_value, &sm3_len);
	EVP_MD_CTX_reset(sm3ctx);						

	//printf("原始数据%s的摘要值为:\n", input);
	for (i = 0; i < sm3_len; i++)
	{
		sm3_tables[order_number][i] = sm3_value[i];

		printf("%02x ", sm3_value[i]);
	}
	printf("\n");
	order_number++;
	
	sm3_rho_method(sm3_value);
	
}
int main()
{
	OpenSSL_add_all_algorithms();
	unsigned char msg1[] = "123456789";
	sm3_rho_method(msg1);
	
	return 0;
}
