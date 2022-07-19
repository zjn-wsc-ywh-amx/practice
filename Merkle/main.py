import math
import random
import hashlib


class Node:
    def __init__(self, item):   #节点的内容
        self.item = item
        self.child1 = None
        self.child2 = None
        self.hash = None
        self.data = None

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

    def add(self, item):  # 逐层添加子节点
        node = Node(item)   #初始化一个节点
        end_str = generate_value(item)
        print("add node ", item)

        if end_str != None and end_str != -1:   #根节点入栈
            node.change_data(end_str)
            print("data= %s " % (node.data))
            print("hash= %s " % (node.hash))

        if self.root is None:
            self.root = node
        else:
            q = [self.root]
            while True:
                pop_node = q.pop(0)    #以栈内第一个节点为根节点
                if pop_node.child1 is None:    #如果根节点的左子树是空的就把该节点加入
                    pop_node.child1 = node
                    return
                elif pop_node.child2 is None:   #如果根节点的右子树是空的就把该节点加入
                    pop_node.child2 = node
                    return
                else:
                    q.append(pop_node.child1)     #左右子树入栈
                    q.append(pop_node.child2)

    def reload_hash(self):  # 层次遍历更新hash
        pass

    def traverse(self):  # 层次遍历
        pass

if __name__ == '__main__':
    t = Tree()
    for i in range(10):  # 基础节点
        t.add(i)


