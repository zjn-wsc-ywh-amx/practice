import mysm2
#本示例测试加解密部分
private_key = '00B9AB0B828FF68872F21A837FC303668428DEA11DCD1B24429D0C99E24EED83D5'
public_key = 'B9C9A6E04E9C91F7BA880429273747D7EF5DDEB0BB2FF6317EB00BEF331A83081A6994B8993F3F5D6EADDDB81872266C87C018FB4162F5AF347B483E24620207'
sm2_crypt = mysm2.CryptSM2(public_key=public_key, private_key=private_key)
data = b"let's date tomorrow!"
enc_data = sm2_crypt.encrypt(data)
print(enc_data)
dec_data =sm2_crypt.decrypt(enc_data)
print(dec_data)
#签名部分
k = myrfc6979.rfc(data,int(private_key,16))
sigA = sm2_crypt.sign(data,k)
print(sigA)
verB = sm2_crypt.verify(sigA,data)
print(verB)
