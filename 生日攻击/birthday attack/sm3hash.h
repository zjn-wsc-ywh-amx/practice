/**************************************************
* File name: sm3hash.h
* Author: HAN Wei
* Author's blog: http://blog.csdn.net/henter/
* Date: June 18th, 2018
* Description: declare a sm3 hash calculation function
**************************************************/

#ifndef HEADER_C_FILE_SM3_HASH_H
#define HEADER_C_FILE_SM3_HASH_H

#ifdef  __cplusplus
extern "C" {
#endif

	int sm3_hash(const unsigned char* message, size_t len, unsigned char* hash, unsigned int* hash_len);

#ifdef  __cplusplus
}
#endif

#endif  /* end of HEADER_C_FILE_SM3_HASH_H */