# WaterSort
A replica of a popular game where you sort bottles based on different coloured layers of liquids. Also added a AI assistant which is able to solve any game. It also tries to do it with the least amount of moves. 

## How to use
To start just run the UI.py

## To implement
1. A better mode where you can give a gamestate in a nice way maybe with a UI and it returns a solution with both a list of steps and some visual way.
2. When letting the AI evaluate add a means of showing the "Score" that the solve of the AI has. 

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

This class has three properties: gamestate (list of bottles of class (Bottle)), capacity (maximal amount of liquid which can fit in the bottle)
