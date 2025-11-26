def GetBottlePositions(n_bottles:int,bottle_width:float,screen_width:int,screen_height:int,BorderSize=50,SpacingY=40) -> tuple: 
    
    """
    Function to get equal spacing accros the screen. 
    Returns a list of x and y coordinates and the size of the object
    """
    
    # How much of the screen can be filled taking into acount of empty space
    SpaceLeftY = screen_height - (BorderSize * 2) - SpacingY
    size = SpaceLeftY / 2 
    width = size * bottle_width
    
    
    # The game will consist of two rows of bottles
    if n_bottles % 2 == 0:
        n_bottles_row1 = int(n_bottles / 2)
    else:
        n_bottles_row1 = int((n_bottles + 1) / 2)
        
    # A bottle has a width of size*0.4
    SpaceLeftX = screen_width - (width * n_bottles_row1) - (BorderSize * 2)
    SpacingX = SpaceLeftX / (n_bottles_row1 - 1)
    
    BottlePositions = []
    x = BorderSize 
    y = BorderSize
    
    for i in range(n_bottles):
        if i > 0 and i != (n_bottles_row1):
            x += SpacingX + (width)
        
        BottlePositions.append((x,y))
        
        # Go down a row when we reach the last bottle of the row
        if i == (n_bottles_row1 - 1):
            x = BorderSize 
            y += SpacingY + size    

    return BottlePositions,size

def find_clicked_bottle(bottle_positions:list,size:int,bottle_width:float,xclick:int,yclick:int) -> int:
    n = len(bottle_positions)
    coordinate_span = int(size * bottle_width)
    # To keep the index of the items in the list
    search_index = [i for i in range(n)]
    
    # Find the amount of bottles on the first row
    if n % 2 == 0:
        n_r1 = n/2
    else:
        n_r1 = (n+1)/2
    
    # First search if the click is on the first or second row
    _,y_r1 = bottle_positions[0]
    _,y_r2 = bottle_positions[-1]
    
    # Whenever it is inbetween the gaps on the y axis return nothing
    if yclick < y_r1 or yclick > (y_r2 + size) or (yclick > y_r1+size and yclick < y_r2):
        return None
    
    # Now we have halved the list and now this list needs to be searched
    search_x, search_index = get_row(yclick,n_r1,y_r2,bottle_positions,search_index)
    
    return binary_search(search_x,search_index,coordinate_span,xclick)
    
def get_middle_index(list:list) -> int:
    if len(list) % 2 == 0:
        return int((len(list) / 2) - 1) 
    else:
        return int(((len(list)+1)/2)-1)
    
def get_row(yclick,n_r1,y_r2,bottle_positions,search_index):
    # Whenever we are on r1 we only have to search the first part of the list
    if yclick < y_r2:
        search = bottle_positions[0:int(n_r1)]
        search_index = search_index[0:int(n_r1)]
    
    # Whenever we are on r2 we only have to search the second part of the list
    if yclick > y_r2: 
        search = bottle_positions[int(n_r1):]
        search_index = search_index[int(n_r1):]
    
    # Only return the important x coordinates
    search_x = [x for x,y in search]
    
    return search_x, search_index

def binary_search(coordinates:list,coordinates_index:list,coordinate_span:int,target:int) -> int:
    """
    It takes in a list of of coordinates, indexes and its span which is the size 
    of the object. It then searches for the object which contains the target. 
    If the target is not in any object it returns None 
    """
    
    if len(coordinates) == 0:
        return None
    else:
        i_middle = get_middle_index(coordinates)
        if target >= coordinates[i_middle] and target <= (coordinates[i_middle] + coordinate_span):
            return coordinates_index[i_middle]
        
        elif target < coordinates[i_middle]: 
            # So we do not change the original list
            search = coordinates.copy()
            search_index = coordinates_index.copy()
            
            # Not inclusive since we already check if this one is it
            search = search[0:i_middle]
            search_index = search_index[0:i_middle]
        elif target > coordinates[i_middle] + coordinate_span: 
            # So we do not change the original list
            search = coordinates.copy()
            search_index = coordinates_index.copy()
            
            # Not inclusive since we already check if this one is it
            search = search[i_middle+1:]
            search_index = search_index[i_middle+1:]            
       
        # At this point we have not found the target so try again with the other half of the list
        return binary_search(search,search_index,coordinate_span,target)   

def user_input_to_action(chosen_bottle:int,selection:int,GameInstance) -> tuple:
    """
    Will convert user input into a game action. I.e. should we pour yes or no. 
    Will also draw a selection box. Returns the (x,y) where the box was drawn. 
    """
    # Start with base case
    remove_selection = False
    selection_is_drawn = False
    finished_bottle = None
    
    # This decides what action we will perform. Either remove the selection or draw a selection
    if chosen_bottle != None:
        if selection == None:
            # Whenever there is an empty selection we add the chosen object
            selection = chosen_bottle
            
            # Then we draw the new selection box
            selection_is_drawn = True
        
        elif chosen_bottle == selection:
            # Whenever we select the same item we should unselect it
            # Then we draw the new selection box which is transparent
            remove_selection = True
            selection = None
            
        elif selection != None:
            # If there is another unique item then transfer fluid from object 1 to 2 
            GameInstance.transfer_liquid(selection,chosen_bottle)
            if GameInstance.gamestate[chosen_bottle].is_finished():
                finished_bottle = chosen_bottle
            ## REMOVE BOTTLE SELECTION
            remove_selection = True
            selection = None
    else:
        selection = None
    
    return selection,selection_is_drawn,remove_selection,finished_bottle



def game_is_finished(GameInstance) -> bool:
    from GameInitializer import WaterSortGame
    
    for bottle in GameInstance.gamestate:
        if not bottle.is_empty():
            if not bottle.is_finished():
                return False
        
    return True

def FinishedBottle(animation):
    from Sprites import draw_convetti
    import random
    import numpy as np
    
    step = animation.step()
    
    # At the first step we will initialize a randomizer the positions slightly of every color
    if step == 0: 
        length = animation.length()
        start_x,start_y = animation.position()
        width, height = animation.screendims()
        
        tmp1 = np.linspace(-int(height * 0.08), 0, num=int(length/2)+1)
        tmp2 = np.linspace(0, int(height * 0.15), num=int(length/2)+1)
        accelerations_y = np.concatenate((tmp1, tmp2))
        
        tmp1 = np.linspace(0,int(width * 0.01),num=int(length/3)+1)
        tmp2 = np.linspace(int(width*0.01),0,num=int(length/3)+1)
        tmp3 = np.zeros(int(length/3)+1)
        accelerations_x = np.concatenate((tmp1,tmp2,tmp3))
        
        attribute = []
        for color in animation.attribute: 
            randomizer_x = random.uniform(-1, 1)
            randomizer_y = random.uniform(0.8, 1)
            
            path = []
            x = start_x
            y = start_y
            for acceleration_x,acceleration_y in zip(accelerations_x,accelerations_y): 
                x = int(x + (acceleration_x * randomizer_x))
                y = int(y + acceleration_y * randomizer_y)
                path.append((x,y))
            attribute.append((color,path))

        animation.attribute = attribute
        
    # Now we shoot it in a straight line 
    for color, path in animation.attribute:
        x,y = path[step]
        
        animation.screen().blit(
        draw_convetti(color,10),
        (x,y)
        )

    animation.next_step()

def celebrations(animation):
    ## Select 15 random points to start a spark animation
    ## Repeat this for half the duration of a spart animation
    ## a spark animation is ~ 0.5 so every 0.25s
    import random
    from Animation import Animation
    
    screen_width, screen_height = animation.screendims()
    step = animation.step()
    
    if step == 0 or (step % 15 == 0):
        points = [(random.randint(0,screen_width),random.randint(0,screen_height)) for _ in range(15)]
        for point in points:
            x,y = point
            animation.attribute.append(
                Animation(
                    f'Spark_{x,y}',
                    'FinishedBottle',
                    animation.starttime() + step,
                    int(animation.starttime() + step + (.5 * 60)),
                    ['red','yellow','fuchsia','lime','cyan','orange','magenta','dodgerblue','gold','mediumspringgreen'],
                    (x,y),
                    animation.screen(),
                    (screen_width,screen_height)
                )
                
            )
    
    animation.next_step()
 
def start_animations(ongoing_animations:list):
    for animation in ongoing_animations:
        if animation.type() == 'FinishedBottle':
            FinishedBottle(animation)
        
        if animation.type() == 'Celebrations':
            celebrations(animation)
                    
        if animation.finished():
            ongoing_animations.remove(animation)
        
def generate_layout(game_size:int,capacity:int,level:int) -> list:
    import random
    random.seed(level)
    
    colors = ['Red','Blue','Green','yellow','Orange','Purple','cadetblue2','darkcyan','darkmagenta','gold','crimson','darkorchid3','firebrick3','fuchsia','lightgoldenrod']
    # We will need two empty bottle so we need gamesize - 2 amount of different colors 
    colors = colors[0:game_size-2]
    layout = [[] for _ in range(game_size)]
    options = [color for color in colors for _ in range(capacity)]
    for i in range(game_size-2):
        for _ in range(capacity):
            rand = random.randint(0,len(options)-1)
            layout[i].append(options[rand])
            options.pop(rand)

    return layout

class Button:
    import pygame
    
    def __init__(self,position:pygame.rect,sprite,name:str):
        self.__position = position
        self.__sprite = sprite
        self.__name = name
    
    def draw(self,screen) -> None:
        screen.blit(self.__sprite,self.__position)
    
    def is_clicked(self,click:tuple) -> bool:
        x,y,w,h = self.__position
        c_x, c_y = click
        
        if (c_x >= x and c_x <= x+w) and (c_y >= y and c_y <= y+h):
            return True
        else: 
            return False

    def change_sprite(self,sprite) -> None:
        self.__sprite = sprite
    
    def name(self) -> str:
        return self.__name