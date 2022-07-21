import math
import random
import hashlib


class Node:
    def __init__(self, item):   #节点的内容
        self.item = item

        self.left = None
        self.right = None

        self.hash = None
        self.data = None   #如果data不是None那么就是叶子节点

        self.parent=None   #指向父节点

    def change_data(self, data):   #  求出每个节点的hash值
        self.data = data
        self.hash = hashlib.md5(data.encode('utf-8')).hexdigest()[8:-8]  # hexdigest()返回摘要，作为十六进制数据字符串值 [8:-8]将32位MD5转换为16进制
        print("make_hash", self.hash, "size", len(self.hash), end=" ")
        return self.hash


def generate_value(i):
    if i >= 0 and i < 10:  # 产生带数据节点
        raw_str = "base content"
        nums = math.floor(1e5 * random.random())  # 获取数字的下限
        nums = str(nums)
        nums = nums.zfill(5)  # 右对齐前面填0
        end_str = raw_str + nums
        print("end_str", end_str)
        return end_str
    # elif i >= 0 and i < 7:                        #产生不带数据节点
    #   return None
    else:
        return -1

class Tree:

    def __init__(self):
        self.root = None

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
        time=0
        num=0
        if len(elelist)==1:
            return elelist.pop(0)
        
        if len(elelist) !=0 and elelist[0].data is not None:
            pop_left=elelist.pop(0)
        else:
            pop_left=None
        if len(elelist) !=0 and elelist[0].data is not None:
            pop_right=elelist.pop(0)
        else:
            pop_right=None
        name="parent"+str(num)
        node_parent=Node(name)    ##初始化一个父亲节点

        if pop_left and pop_right is not None:
            pop_left.parent=node_parent
            pop_right.parent=node_parent
            node_parent.left=pop_left
            node_parent.right=pop_right
            node_parent.hash=hash(pop_left.hash+pop_right.hash)  ####构造父节点的hash
            elelist.append(node_parent)

        elif pop_left  is  None:
            pop_right.parent = node_parent
            node_parent.right = pop_right
            node_parent.hash = hash( pop_right.hash)
            elelist.append(node_parent)
            print("叶子节点遍历完毕")

        elif pop_right  is  None:
            pop_left.parent = node_parent
            node_parent.left= pop_left
            node_parent.hash = hash(pop_left.hash)
            elelist.append(node_parent)
            print("叶子节点遍历完毕")

        elif pop_left is None and pop_right is  None:

            print("叶子节点遍历完毕")

        ########递归构建##########
        print("第 %d层 " % (time))
        time=time+1
        self.merkle(elelist)

        num=num+1
        if self.root is None:
            self.root = node
        else:
            q = [self.root]
            while True:
                pop_node = q.pop(0)    #以栈内第一个节点为根节点
                if pop_node.left is None:    #如果根节点的左子树是空的就把该节点加入
                    pop_node.left = node
                    return
                elif pop_node.right is None:   #如果根节点的右子树是空的就把该节点加入
                    pop_node.right = node
                    return
                else:
                    q.append(pop_node.left)     #左右子树入栈
                    q.append(pop_node.right)


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

    def traverse(self):  # 层次遍历
        if self.root is None:
            return None
        temp=[self.root]
        store=[(self.root.item,self.root.data,self.root.hash)]
        while temp!=[]:
            node=temp.pop(0)
            if node.left is not None:
                temp.append(node.left)
                store.append((node.left.item,node.left.data,node.left.hash))
            elif node.right is not None:
                temp.append(node.right)
                store.append((node.right.item,node.right.data,node.right.hash))

        return (store)

if __name__ == '__main__':
    t = Tree()
    for i in range(10):
        t.add(i)

    for i in range(4, 0, -1):  # 刷新基础节点hash值
        print("第", i, '层节点hash刷新:')
        print(t.reload_hash())
print('前序遍历:\n节点名:数据：hash值', t.traverse())

