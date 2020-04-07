# -*- coding: utf-8 -*-
"""
Created on Tue Apr  7 20:10:10 2020

@author: $parsh
"""
class DoubleNode:
    def __init__(self, value=None):
        self.value = value
        self.radd = None
        self.ladd = None
                
class DoublyLinkedList:
    def __init__(self):
        self.head = DoubleNode()
        
    def append(self, value) :
        if self.head is None:
            self.head = DoubleNode(value)
            self.radd = self.ladd
            return
        else:
            self.radd = DoubleNode(value)
            self.radd.radd = None
            self.radd.ladd = self.radd
            
    def display(self):
            elems = []
            cur_node = self.head
            while cur_node.radd != None:
                cur_node = cur_node.radd
                elems.append(cur_node.value)
            print(elems)
        
        
mylist = DoublyLinkedList()
mylist.append(2)
mylist.append(2)
mylist.display()
