from gmssl import sm3, func
import mysm3
import struct

def padding(msg):
    leng = len(msg)
    msg.append(0x80)
    k = 56-(leng+1)%64
    r=56
    if (k<0):
        r=120
    for i in range((leng+1)%64,r):
        msg.append(0x00)
    L = leng*8
    msg.extend([int(x) for x in struct.pack('>q', L)])
    #print('msg={}'.format(msg))
    return msg


def length_extension_attack(length, hash, apd):
    IV = []
    for i in range(0,len(hash),8):
        IV.append(int(hash[i:i+8],16))
    print('哈希值分片后:{}'.format(IV))
    msg = "a"*length
    msg = func.bytes_to_list(bytes(msg, encoding='utf-8'))
    msg = padding(msg)
    #print('msg='+msg)
    msg.extend(func.bytes_to_list(bytes(apd,encoding = 'utf-8')))
    return mysm3.sm3_hash(msg,IV)


secret = 'we shall meet tonight at XA street'
#secret = "0.28923017773830817"
print('消息为'+secret)
hash_se = sm3.sm3_hash(func.bytes_to_list(bytes(secret,encoding='utf-8')))
print('消息的哈希值为'+hash_se)
length_se = len(secret)
append = 'position changed to tomorrow'
#append = "1901210403"
print('附加消息为'+append)


fake_hash = length_extension_attack(length_se,hash_se,append)

new_msg = padding(func.bytes_to_list(bytes(secret,encoding='utf-8')))
lent=len(new_msg)
new_msg.extend(func.bytes_to_list(bytes(append, encoding='utf-8')))
#new_msg_str = secret+(str(padding(func.bytes_to_list(bytes(secret,encoding='utf-8')))[length_se+1:]))+ append
pad_str=""
for i in range(length_se+1,lent):
    pad_str += str(new_msg[i])
new_msg_str=secret+pad_str+append
new_hash = sm3.sm3_hash(new_msg)

print('伪造的哈希为'+fake_hash)
print('伪造的消息为'+new_msg_str)
print('伪造消息应有的哈希为'+new_hash)

if(new_hash == fake_hash):
    print('伪造成功！好耶ヽ(✿ﾟ▽ﾟ)ノ')