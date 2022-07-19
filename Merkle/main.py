import math
import random
import hashlib


class Node:
    def __init__(self, item):
        self.item = item
        self.child1 = None
        self.child2 = None
        self.hash = None
        self.data = None

    def change_data(self, data):
        self.data = data
        self.hash = hashlib.md5(data.encode('utf-8')).hexdigest()[
                    8:-8]  # hexdigest()返回摘要，作为十六进制数据字符串值 [8:-8]将32位MD5转换为16进制
        print("make_hash", self.hash, "size", len(self.hash), end=" ")
        return self.hash




class Tree:

    def __init__(self):
        self.root = None

    def add(self, item):  # 逐层添加子节点
        node = Node(item)
        end_str = make_data(item)
        print("add node ", item)
        if end_str != None and end_str != -1:
            node.change_data(end_str)
            print("data= %s " % (node.data))
            print("hash= %s " % (node.hash))
        if self.root is None:
            self.root = node
        else:
            q = [self.root]
            while True:
                pop_node = q.pop(0)
                if pop_node.child1 is None:
                    pop_node.child1 = node
                    return
                elif pop_node.child2 is None:
                    pop_node.child2 = node
                    return
                else:
                    q.append(pop_node.child1)
                    q.append(pop_node.child2)

    def reload_hash(self):  # 层次遍历更新hash
        pass

    def traverse(self):  # 层次遍历
        pass



