class Node:
    def __init__(self,edge_pointer,eval_score,move):
        self.__edge = edge_pointer
        self.__score = eval_score
        self.__move = move
        
    def edge(self):
        return self.__edge
    
    def score(self):
        return self.__score
    
    def move(self):
        return self.__move
    
    def get_depth(self):
        import copy
        
        depth = 0
        tmp = copy.deepcopy(self)
        
        while tmp.edge() != None:
            tmp = tmp.edge()
            depth += 1
        
        return depth
        
        
            
class Tree:
    def __init__(self):
        self.__nodes = []
    
    def add_node(self,node):
        self.__nodes.append(node)
    
    def nodes(self):
        return self.__nodes
    
    def has_children(self,target_node):
        for node in self.nodes():
            if node.edge() == target_node:
                return True
        
        return False

    def get_leafnode(self):
        """ 
        Returns a list of the bottom of the tree e.g. the leaf nodes.
        """
        
        leafnodes = []
        
        for node in self.nodes():
            if not self.has_children(node):
                leafnodes.append(node)
       
        return leafnodes

    def get_movelist(self,node):
        
        import copy
        move_list = []
        
        tmp = copy.deepcopy(node)
        while tmp.edge() != None:
            move_list.insert(0,tmp.move())
            tmp = tmp.edge()
        
        return move_list


    def get_bestnode(self):
        """
        1. First finds all nodes without any children (leaf nodes). Since these are all our option to select from. 
        2. Selects the node with the highest score. If score is the same picks the first node. 
        3. returns the Node object
        """
        import numpy as np
        
        
        
        leafnodes = self.get_leafnode()
        scores = [node.score() for node in leafnodes]
        bestnode = leafnodes[np.argmax(scores)]
        
        return bestnode

if __name__ == "__main__":
    pass