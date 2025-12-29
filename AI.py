from GameInitializer import WaterSortGame
from HelperFunctions import generate_layout

def evaluate(GameInstance) -> int:
    """ 
    This function evaluates a game state based on a set of 4 heuristics.
    1. If a game is finished it gives the gamestate 100000 points
    2. For every bottle which is finished the gamestate gets 5 points
    3. For every consecutive color from the bottom up 2 points gets awarded
    4. For every duplicate bottom color 3 points get deducted
    """
    
    score = 0
    gamestate = GameInstance.gamestate
    
    # Heuristic 1 - Finished Game increases score by 100000
    if GameInstance.is_finished():
        score += 100000
    
    # Heuristic 2 - A finished bottle counts for 5 points
    for bottle in gamestate:
        if bottle.is_finished():
            score += 5
    
    # Heuristic 3 - Consecutive colors from the bottom up counts for 1 point
    for bottle in gamestate:
        if not bottle.is_empty():
            prev_color = bottle.content[0]
            for color in bottle.content[1:]:
                if color == prev_color:
                    score += 2
                else: 
                    break
    
    # Heuristic 4 - Duplicate bottom colors will deduct 3 points            
    bottom_colors = []
    for bottle in gamestate:
        if not bottle.is_empty():
            bottom_colors.append(bottle.content[0])
    
    set_bottom_colors = set(bottom_colors)
    duplicates = len(bottom_colors) - len(set_bottom_colors)
    score -= duplicates * 3
    
    return score

def get_evaluation_list(GameInstance) -> list:
    """ 
    This functions takes a GameInstance and returns all possible moves which are legal.
    
    Illegal moves include:
    1. Whenever the first bottle is empty
    2. Whenever the second bottle is full
    3. Whenever the pour exceeds the limit of bottle 2
    4. Whenever the first bottle is already finshed 
    """
    import copy
    
    current_evals = []
    game_size = GameInstance.size + 1
    choices = []
    
    # Creates a list of all possible moves which adhere to the game rules (choices)
    for i in range(game_size):
        for j in range(game_size):
            if i != j:
                if GameInstance.is_transfer_possible((i,j)):
                    choices.append((i,j))

    # Evaluates each move and adds their score to current_evals
    for move in choices:
        b1,b2 = move
        tmp = copy.deepcopy(GameInstance)
        tmp.transfer_liquid(b1,b2)
        current_evals.append(evaluate(tmp))
    
    return current_evals, choices

# This is the logic behind the AI 
def solve_gameinstance(GameInstance, iterations=1000,show_iterations=True) -> list:
    """ 
    It analyses a GameInstance and returns a list of moves which lead to the best possible result.

    This is based on a heuristic search on a tree.
    """
    import copy
    from Tree import Tree, Node
    
    # Makes a deepcopy of the gameinstance to avoid directly editing the gameinstance later on
    GameInstance_copy = copy.deepcopy(GameInstance)
    
    # Creates a tree in which the search will happen
    tree = Tree()
    
    # Creates the root node of the tree. Identified by only Null pointers
    prev_node = Node(None,None,None)
    tree.add_node(prev_node)
    
    i=0
    running = True
    while running:
    
        # Runs throught the evaluation of the gameinstance copy and adds all posible solutions to the tree
        current_evals, choices = get_evaluation_list(GameInstance_copy)
    
        for score, move in zip(current_evals,choices):
            depth = prev_node.get_depth() + 1 
            tree.add_node(Node(prev_node,score - int(depth/3),move))

        # Finds the node highest scoring node
        current_node = tree.get_bestnode()
        
        
        # Brings the gameinstance copy to the state of the current node. This is dependent on if the move was 
        # originating from the same path. Otherwise the game needs to reset and follow the movelist of bestnode. 
        if current_node.edge() == prev_node:        
            ## If it has the same parent 
            b1,b2 = current_node.move()
            GameInstance_copy.transfer_liquid(b1,b2)
        else:
            ## Get the movelist of that other node and create a new copy of gameinstance and walk through movelist
            GameInstance_copy = copy.deepcopy(GameInstance)
            movelist = tree.get_movelist(current_node)
            
            for move in movelist:
                b1,b2 = move
                GameInstance_copy.transfer_liquid(b1,b2)
        
        prev_node = current_node
        if len(choices) == 0:
            running = False
        if i == iterations:
            running = False
        if prev_node.score() > 10000:
            running = False 
        
        i+=1
        
        # Prints iteration every 100 iterations.
        if show_iterations:
            if i % 100 == 0:
                print(f'Itteration: {i}')
        
    return tree.get_movelist(current_node)   

# This is the visual aspect
def AI_assistance(GameInstance,screen_width,screen_height,level=1,iterations = 2000,speed=0.5,print_movelist = False):
    import pygame
    from Game import watersort
    from UI import UI
    from Sprites import draw_gamestate, draw_selection,button_sprite
    from Animation import Animation
    from HelperFunctions import GetBottlePositions, user_input_to_action,start_animations, Button

    game_size = GameInstance.size + 1
    capacity = GameInstance.capacity
    
    
    # Graphical Input
    bottle_width = 0.4
    bottle_edge_thickness = 0.05
    background_color = (105,105,105)
    
    # Variables associated with updating graphics
    selection_is_drawn = False
    remove_selection = False
    finished_bottle = None
    GameFinished = False
    ongoing_animations = []
    
    # Required for the calculations to find which bottle the user clicks
    bottle_positions,bottle_size = GetBottlePositions(game_size,bottle_width,screen_width,screen_height)
    selection = None
    chosen_bottle = None
    movelist = None
    move = None
    
    
    # Required for the timing of the AI
    i = 0
    
    pygame.init()
    screen = pygame.display.set_mode((screen_width,screen_height))
    clock = pygame.time.Clock()
    pygame.display.set_caption('Water Sort!   *AI assisted*')    

    # Return to menu button
    sprite = button_sprite((75,30),'Black','White','< Menu')
    button_rect = sprite.get_rect(center=(40,18))
    return_button = Button(button_rect,sprite,'rtn_btn')

    # Initiate AI solve button
    sprite = button_sprite((75,30),'Black','White','AI assistant',selected=True)
    button_rect = sprite.get_rect(center=(960,18))
    AI_button = Button(button_rect,sprite,'AI_btn')  

    # Game loop
    while True:
        click = None

        ## Process player inputs.
        for event in pygame.event.get():
            # Quit at press of close button
            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit

            # Quit the game whenever the ESC key is pressed
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    raise SystemExit
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                click = event.pos
            
            ## DO SOME ACTION! BASED ON THE LIST PROVIDED DO THIS AFTER THE SCREEN IS LOADED ONCE!

        ## Graphics
        screen.fill(background_color)  # Fill the display with a solid gray color 

        # Draws the board of bottles
        draw_gamestate(
            screen,
            GameInstance.get_content_bottles(),
            capacity,
            game_size,
            bottle_width,
            bottle_edge_thickness,
            screen_width,
            screen_height
            )

        return_button.draw(screen)
        AI_button.draw(screen)
        
        
        ## IMPORTANT TO SPLIT UP THE MOVE INTO MULTIPLE ACTIONS AND ADJUST SELECT
        #  This way it is preceived as clicks.
        #  selection_is_drawn and remove_selection needs to be updated somewhere
        
        # This first lets the gamestate be drawn and then after 10 frames it will initiate the search for the movelist
        if i == 10:
            movelist = solve_gameinstance(GameInstance,iterations=iterations)
            if print_movelist:
                print(movelist)
            i+=1
        else: 
            i+=1
        
        
        # Every second I want the AI to start a action
        if i % int(60*speed) == 0:
            if move == None and len(movelist) != 0:
                move = movelist[0]
                movelist.pop(0)
                selection, move = move
                selection_is_drawn = True
            else:
                selection,selection_is_drawn,remove_selection,finished_bottle = user_input_to_action(move,selection,GameInstance)
                
            
        
        # Handles the logic of drawing the selection around a bottle
        if selection_is_drawn:
            draw_selection(
            screen,
            bottle_positions,
            bottle_size,
            bottle_width,
            bottle_edge_thickness,
            selection,
            color = 'Red'
            )

        elif remove_selection: 
            draw_selection(
            screen,
            bottle_positions,
            bottle_size,
            bottle_width,
            bottle_edge_thickness,
            move,
            color = background_color
            )
                    
            remove_selection = False
            move = None
            
        if click != None:
            if return_button.is_clicked(click):
                pygame.quit()
                UI(level=level)
            elif AI_button.is_clicked(click):
                pygame.quit()
                watersort(None,None,level,screen_width,screen_height,GameInstance=GameInstance)
                
        ## finished_bottle still needs to be updated somewhere based on the move
        #
        
        # Add any animations to the animation list
        if finished_bottle != None:
            x,y = bottle_positions[finished_bottle]
            x += int(bottle_size * bottle_width/2)
            y += int(bottle_size*4/5)
            
            ongoing_animations.append(
            Animation(
                    f'FinishedBottle{finished_bottle}',
                    'FinishedBottle',
                    pygame.time.get_ticks(),
                    int(pygame.time.get_ticks() + (.5 * 60)),
                    ['red','yellow','fuchsia','lime','cyan','orange','magenta','dodgerblue','gold','mediumspringgreen'],
                    (x,y),
                    screen,
                    (screen_width,screen_height)
                    )
            )
            finished_bottle = None

        # This initiates the finishing animation whenever the game finishes. 
        if GameFinished == False:
            if GameInstance.is_finished():
                ongoing_animations.append(
                Animation(
                    'Finish',
                    'Celebrations',
                    pygame.time.get_ticks(),
                    int(pygame.time.get_ticks() + (5 * 60)),
                    ongoing_animations,
                    (None,None),
                    screen,
                    (screen_width,screen_height)
                )
                )

                GameFinished = True
                
        # Do any type of animation. 
        start_animations(ongoing_animations)

        if GameInstance.is_finished() and len(ongoing_animations) == 0:
            pygame.quit()
            UI(level=level)
        
        pygame.display.flip()  # Refresh on-screen display
        clock.tick(60)         # wait until next frame (at 60 FPS)

if __name__ == "__main__":

    # Input for the game settings
    layout = generate_layout(12,4,2)
    GameInstance = WaterSortGame(12,4,layout)
    AI_assistance(GameInstance,1000,600)
    
    #print(solve_gameinstance(GameInstance,iterations=2000))

    
