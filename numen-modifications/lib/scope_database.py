import  yaml
from pathlib import Path
import os

class Node(): 
    def __init__(self, name=None, parent=None, children=None, next=None):
        self.name = name
        self.parent = parent
        self.children = children
        self.next = None
    def __repr__(self):
        return f"Node(name={self.name}, parent={self.parent}, children={self.children}, value={self.value})"

yaml_dict = yaml.safe_load(Path("hierarchy.yaml").read_text())


def extend_children(node, new_child):
    if node.children is None:
        node.next = new_child
    else:
        while node.next is not None:
            node = node.next
        node.next = new_child

def create_tree(yaml_dict):
    head = Node()

    for key in yaml_dict:
        node = Node(key)
        node.parent = head
        extend_children(head, yaml_dict[key])
        for sub_key in yaml_dict[key]:
            sub_node = Node(sub_key)
            extend_children(node, yaml_dict[key][sub_key])
            sub_node.parent = node
        
    return head


node= create_tree(yaml_dict)
while node.next is not None:
    node = node.next
    print(node)    
print(yaml_dict)

 


    

