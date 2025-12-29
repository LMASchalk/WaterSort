import pygame
from AI import AI_assistance
from UI import UI
from Sprites import draw_gamestate, draw_selection,button_sprite
from GameInitializer import WaterSortGame
from Animation import Animation
from HelperFunctions import GetBottlePositions,find_clicked_bottle, user_input_to_action,game_is_finished,start_animations, generate_layout, Button

def watersort(game_size,capacity,level,screen_width,screen_height, GameInstance=None):
    if GameInstance == None:
        # Input for the game settings
        layout = generate_layout(game_size,capacity,level)
        # Starts an game object
        GameInstance = WaterSortGame(game_size,capacity,layout)

    else:
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

    pygame.init()
    screen = pygame.display.set_mode((screen_width,screen_height))
    clock = pygame.time.Clock()
    pygame.display.set_caption('Water Sort!')

    # Return to menu button
    sprite = button_sprite((75,30),'Black','White','< Menu')
    button_rect = sprite.get_rect(center=(40,18))
    return_button = Button(button_rect,sprite,'rtn_btn')

    # Return to menu button
    sprite = button_sprite((75,30),'Black','White','Reset')
    button_rect = sprite.get_rect(center=(120,18))
    reset_button = Button(button_rect,sprite,'rst_btn')
    
    # Initiate AI solve button
    sprite = button_sprite((75,30),'Black','White','AI assistant')
    button_rect = sprite.get_rect(center=(960,18))
    AI_button = Button(button_rect,sprite,'AI_btn')    
    
    
    # Game loop
    while True:
        click = None
        ## Process player inputs.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit

            # Quit the game whenever the ESC key is pressed
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    raise SystemExit

            # Registers a mouse click and stores the location of the click in x_click and y_click
            if event.type == pygame.MOUSEBUTTONDOWN:
                (x_click,y_click) = event.pos
                click = x_click, y_click
                # Searches if the user clicked on a bottle and if so stores it in chosen_bottle
                chosen_bottle = find_clicked_bottle(bottle_positions,bottle_size,bottle_width,x_click,y_click)
                # Updates the item which is selected and changes the status to draw a selection box
                selection, selection_is_drawn, remove_selection,finished_bottle = user_input_to_action(
                    chosen_bottle,
                    selection,
                    GameInstance
                )
                                
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
        reset_button.draw(screen)
        
        
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
            chosen_bottle,
            color = background_color
            )
                    
            remove_selection = False

        if click != None:
            if return_button.is_clicked(click):
                pygame.quit()
                UI(level=level)
            elif AI_button.is_clicked(click):
                pygame.quit()
                AI_assistance(GameInstance,screen_width,screen_height,level=level,iterations=400,speed=0.3)
            elif reset_button.is_clicked(click):
                pygame.quit()
                watersort(game_size,capacity,level,screen_width,screen_height)
                
            
            
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
    watersort(8,4,1,1000,600)