# WaterSort
A replica of a popular game where you sort bottles based on different coloured layers of liquids. Also added a AI assistant which is able to solve any game. It also tries to do it with the least amount of moves. 

## How to use
To start just run the UI.py

## To implement
2. When letting the AI evaluate add a means of showing the "Score" that the solve of the AI has.
3. Refactor how the UI is shown to make it easier to implement new functions.

## Description of different files and classes
### Bottle.py
Contains a class for the bottles in the game (Bottle(capacity: int,content: list)). 

This class has two properties: capacity (maximal amount of liquid which can fit in the bottle) and content (A list of colours where the first element is the bottom colour of the bottle). The bottle class has the following methods:


volume(), Returns how many items is currently in the bottle (int).

is_full(), Returns if the bottle is currently at the maximal capacity (bool).

is_empty(), Returns if the bottle is currently empty (bool).

space_left(), Returns how many items still fit into the bottle (int).

is_finished(), Returns if the bottle is full and with one colour (bool).

top_of_bottle(), Returns the current item which is at the top of the bottle (str).

liquid_depth(), Returns how many items below the top is of the same colour (int).

add_content(item:str), Adds a colour to the top of the bottle.

remove_content(), Removes the top colour from the bottle. 

### GameInitializer.py
Contains the class to generate a WaterSort game, WaterSortGame(size: int, capacity: int,layout: list). 

This class has three properties: gamestate (list of bottles of class (Bottle)), capacity (maximal amount of liquid which can fit in the bottle) and size (the amount of bottles in the game). The GameInitializer class has the following methods:


show_gamestate(), prints the contents of all bottles in the game.

get_content_bottles(), returns a list of lists where each list in the list is a list of colours inside each bottle.

transfer_liquid(bottle_1: int,bottle_2: int), makes a move where liquid is transfered between bottles adhering to the rules of the game. Whenever it is an illegal move nothing will happen. 

is_finished(), returns whether the game is finished (bool).

is_transfer_possible(move), returns if it is an legal move (bool).

get_layout(), returns a list containing the layout of the gamestate.

### Tree.py
Contains two classes Node(edge_pointer,eval_score,move) and Tree. These two classes are at the core of the AI solver. The Node class has the following methods:


edge(), returns the pointer of this node (Node object)

score(), returns the score attached to this node (int)

move(), returns the move which led to this node so the move from the previous node to this node.


The Tree class has the following methods:


add_node(node), adds a node to the list of nodes of the Tree.

nodes(), returns the list of nodes in the current Tree

has_children(target_node), if there is a node which has a pointer towards the target node (bool). 

get_leafnode(), Returns a list of all the bottom nodes of the tree (list).

get_movelist(node), Walks up the tree from node up to the root node to find the movelist to reach this gamepoint (list).

get_bestnode(), Chooses the best scoring node among all leafnodes (Node).




