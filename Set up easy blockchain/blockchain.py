from hashlib import sha256

class B():#区块类
    prev_hash ='0'*64

    def __init__(self,data,num = 0,nonce = 0):
        self.data = data
        self.num = num
        self.nonce = nonce

    def calhash(self):
        text =str(self.prev_hash)+str(self.num)+str(self.data)+str(self.nonce)
        h = sha256()
        h.update(text.encode())
        return h.hexdigest()

    def __str__(self):
        return str("Block:%s\n"
                   "Blockhash:%s\n"
                   "Pre_hash:%s\n"
                   "Data:%s\n"
                   "Nonce:%s"
                   %(self.num,self.calhash(),self.prev_hash,self.data,self.nonce))#此处借鉴youtube视频


class BC():#区块链类
    difficuty=4

    def __init__(self,chain=[]):
        self.chain=chain

    def __str__(self):
        return str(self.chain)

    def add(self,block):
        self.chain.append(block)

    def remove(self,block):
        self.chain.remove(block)

    def mining(self,block):
        try:
            block.prev_hash=self.chain[-1].calhash()
        except IndexError:#借鉴视频，这样可以防止空list报错
            pass
        while True:
            if block.calhash()[:self.difficuty] == '0'*self.difficuty:
                self.add(block)
                break
            else:
                block.nonce+=1
                #print(block.self_hash())

    def verify(self):
        for i in range(1,len(self.chain)):
            prev=self.chain[i].prev_hash
            curt=self.chain[i-1].calhash()
            if curt[:self.difficuty]!='0'*self.difficuty or prev!=curt:
                return False
        return True


database = ['l','54']
blockchain = BC()
num = 0
for data in database:
    num += 1
    blockchain.mining(B(data,num))

for block in blockchain.chain:
    print(block)

print(blockchain.verify())


