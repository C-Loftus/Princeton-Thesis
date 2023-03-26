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
        node.children = [new_child]
    else:
        node.children = list(node.children).extend(new_child)

    return node.children

def create_tree(yaml_dict):
    head = Node()

    for key in yaml_dict:
        node = Node(key)
        node.parent = head
        head.children = extend_children(head, node)
        for sub_key in yaml_dict[key]:
            sub_node = Node(sub_key)
            node.children = extend_children(node, sub_node)
            sub_node.parent = node
        
    return head

[print(node) for node in create_tree(yaml_dict)]


    
print(yaml_dict)

 


    

