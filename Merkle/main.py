import math
import random
import hashlib

another_list = []  ####两个队列来回倒
hash_verify =[]

class Node:
    def __init__(self, item):   #节点的内容
        self.item = item

        self.left = None
        self.right = None

        self.hash = None
        self.data = None

        self.parent=None   #指向父节点
        self.flag=0  #如果flag不是0那么就是叶子节点
        self.time=0

    def change_data(self, data):   #  求出每个节点的hash值
        self.data = data
        self.hash =Hash_single(data)  # hexdigest()返回摘要，作为十六进制数据字符串值
        print("make_hash", self.hash, "size", len(self.hash), end=" ")
        if(self.item==2):
            hash_verify.append(self.hash)
        return self.hash


def generate_value(i):
    if i >= 0 and i < 10:  # 产生带数据节点
        raw_str = "base content"
        nums = math.floor(1e5 * random.random())  # 获取数字的下限
        nums = str(nums)
        #nums=input('请输入区块的值')
        nums = nums.zfill(5)  # 右对齐前面填0
        end_str = raw_str + nums
        print("data", end_str)
        return end_str
    # elif i >= 0 and i < 7:                        #产生不带数据节点
    #   return None
    else:
        return -1
def Hash(string1,string2):
    string=str(int(string1,16)+int(string2,16))
    s = hashlib.sha256()
    s.update(string.encode())
    b = s.hexdigest()
    return b

def Hash_single(string):
    s = hashlib.sha256()
    s.update(string.encode())
    b = s.hexdigest()
    return b

class Tree:

    def __init__(self):
        self.root = None
        self.time = 0
        self.num=0
        self.root_obj=None


    def generatr_tree(self, itemlist):  # 逐层添加子节点
        elelist = []
        for item in itemlist:
            node = Node(item)   #初始化一个节点
            gen_data = generate_value(item)
            print("add node ", item)

            if gen_data != None and gen_data != -1:   #根节点入栈
                node.change_data(gen_data)   #产生hash
                print("data= %s " % (node.data))
                print("hash= %s " % (node.hash))
            elelist.append(node)
        return elelist

################构建根#############

    def merkle(self,elelist):

###############如果节点为奇数个就要复制

        if len(elelist)==1 and len(another_list)==0:
            print("结束")
            self.root_obj=elelist.pop(0)
            return self.root_obj

        if len(elelist) !=0 :
            pop_left=elelist.pop(0)
        else:
            pop_left=None
        if len(elelist) !=0 :
            pop_right=elelist.pop(0)
        else:
            pop_right=None
        name="parent"+str(self.num)
        node_parent=Node(name)    ##初始化一个父亲节点

        if pop_left and pop_right is not None:
            pop_left.parent=node_parent
            pop_right.parent=node_parent
            node_parent.left=pop_left
            node_parent.right=pop_right
            node_parent.hash=Hash(pop_left.hash,pop_right.hash)  ####构造父节点的hash
            node_parent.flag=node_parent.flag^1
            node_parent.left.flag=node_parent.left.flag^1
            node_parent.right.flag=node_parent.right.flag^1
            print("left hash %s ,right hash %s ,hash %s"%(pop_left.hash,pop_right.hash,node_parent.hash))
            another_list.append(node_parent)


        elif pop_left  is  None and pop_right is not None :
            pop_right.parent = node_parent
            node_parent.right = pop_right
            node_parent.hash = pop_right.hash
            node_parent.flag = node_parent.flag ^ 1
            node_parent.right.flag = node_parent.right.flag ^ 1
            another_list.append(node_parent)
            print("right hash %s ,hash %s" % (pop_right.hash, node_parent.hash))
            print("叶子节点遍历完毕")


        elif pop_right  is  None and pop_left is not None:
            pop_left.parent = node_parent
            node_parent.left= pop_left
            node_parent.hash = pop_left.hash
            node_parent.flag = node_parent.flag ^ 1
            node_parent.left.flag = node_parent.left.flag ^ 1
            another_list.append(node_parent)
            print("left hash %s ,hash %s" % (pop_left.hash, node_parent.hash))
            print("叶子节点遍历完毕")


        elif pop_left is None and pop_right is  None:

            print("叶子节点遍历完毕")


        ########递归构建##########
        print("第 %d层 " % (self.time))
        self.time=self.time+1
        self.num=self.num+1
        if len(elelist)==0:
            while another_list!=[]:
                ele=another_list.pop(0)   #########清空another_list
                elelist.append(ele)
        self.merkle(elelist)


    def reload_hash(self):  # 层次遍历更新hash
        if self.root is None:
            return None
        temp = [self.root]  # 根节点入栈
        item = [(self.root.item, self.root.data, self.root.hash)]
        while temp != []:
            pop_node = temp.pop(0)
            if pop_node.left and pop_node.right:
                if pop_node.left and pop_node.right:
                    print("更新节点", pop_node.item, end=" ")
                    end_str = pop_node.left.hash + pop_node.right.hash
                    end_hash = pop_node.change_data(end_str)  # 把左右孩子节点的hash进行hash得出父节点的hash值
                    print("end_hash= %s " % (end_hash))
            if pop_node.left is not None:
                temp.append(pop_node.left)

            if pop_node.right is not None:
                temp.append(pop_node.right)
            return

def traverse(root_node):  # 层次遍历
       # if root_node.root is None:
       #     return None

        temp=[root_node]
        store=[(root_node.item,root_node.data,root_node.hash)]

        while temp!=[]:
            node=temp.pop(0)

            if node.left is not None:
                temp.append(node.left)
                store.append((node.left.item,node.left.data,node.left.hash))

            if node.right is not None:
                temp.append(node.right)
                store.append((node.right.item,node.right.data,node.right.hash))

        return (store)

def flesh(root_obj):
    temp = [root_obj]

    while temp != []:
        node = temp.pop(0)
        node.time=0

        if node.left is not None:
            temp.append(node.left)

        if node.right is not None:
            temp.append(node.right)



def POP(root_obj,id):  #返回关键路径
    #######根据item在列表里面找到相应的hash
    temp = [root_obj]
    store = [(root_obj.item, root_obj.data, root_obj.hash)]
    key=[]
    while temp != []:
        node = temp.pop(0)
        node.time+=1
        if  node.hash==root_obj.hash and node.time>1:
              #key.append((root_obj.item,root_obj.hash))
              key.append(root_obj.hash)
              flesh(root_obj)
              return key   ####返回关键路径

        if(node.item==id):       ########找到这个节点
            parent=node.parent
            temp.append(parent)

            if(parent.left.item!=id):
              brother=parent.left
              #key.append((brother.item,brother.hash))
              key.append(brother.hash)
              id = parent.item

            elif (parent.right.item != id):
                brother = parent.right
                #key.append((brother.item, brother.hash))
                key.append(brother.hash)
                id = parent.item

        if node.left is not None:
            temp.append(node.left)
            store.append((node.left.item, node.left.data, node.left.hash))

        if node.right is not None:
            temp.append(node.right)
            store.append((node.right.item, node.right.data, node.right.hash))



def POA(root_obj,id):
    #返回上一个前一个id和后一个id的存在性证明 最大的小于目标交易的交易，记为pre，最小的大于目标交易的交易，记为next 这两个节点相邻且都存在于merkle中
    ##找到next 就是第一个节点大于id
    temp = [root_obj]
    store = [(root_obj.item, root_obj.data, root_obj.hash)]
    path=[]
    next_id=0
    times=0
    temp2=[]
    max_pre_number=0
    cycle=0

    while temp != [] :
        node = temp.pop(0)
        if(cycle<1):
            temp2.append(node)

        if isinstance(node.item,int):
            if(node.item>id and times<1):
                id=node.item
                pop_next=POP(t.root_obj, id)
                path.append(pop_next)
                next_id=node.item
                times+=1
                #print(node.item)

                if(node.parent.left.item!=id and node.parent.left.item<id):
                    pop_pre=node.parent.left.item
                    pop_next = POP(t.root_obj, pop_pre)
                    path.append(pop_next)

                elif(node.parent.right.item!=id and node.parent.right.item<id) :
                    pop_pre = node.parent.right.item
                    pop_next = POP(t.root_obj, pop_pre)
                    path.append(pop_next)
                #print(pop_pre)     ############获取前一个区块得位置




        if node.left is not None:
            temp.append(node.left)
            store.append((node.left.item, node.left.data, node.left.hash))

        if node.right is not None:
            temp.append(node.right)
            store.append((node.right.item, node.right.data, node.right.hash))

        if len(temp)==0:   ####把值从temp2里面倒出来
            while len(temp2)!=0:
                temp_value=temp2.pop(0)
                temp.append(temp_value)
                cycle+=1

    return (path)

def reconstruct(Input,KeyPath):
      print(Input)
      roothash=KeyPath.pop(-1)
      roothash_1=None
      while len(KeyPath) !=0:
          ele=KeyPath.pop(0)
          roothash_1=Hash(Input,ele)
          Input=roothash_1
          print(Input)
      if roothash_1==roothash:
          print("验证成功")
      else:
          print("验证失败")


if __name__ == '__main__':
    t = Tree()
    itemList=[]
    for i in range(10):
        itemList.append(i)

    list1=t.generatr_tree(itemList)
    t.merkle(list1)
    print(t.root_obj.hash)
    print('层次遍历:\n节点名:数据：hash值', traverse(t.root_obj))
    key=POP(t.root_obj,id=2)
    print("关键路径为",key)

    reconstruct(hash_verify[0],key)
    poa_list=POA(t.root_obj,id=2)
    print("不存在性证明关键路径1:",poa_list[0],"\n不存在性证明关键路径2:",poa_list[1])
