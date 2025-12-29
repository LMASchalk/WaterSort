import pygame
from AI import AI_assistance
from UI import UI
from Sprites import draw_gamestate, draw_selection,button_sprite,draw_bottle
from GameInitializer import WaterSortGame
from Animation import Animation
from HelperFunctions import GetBottlePositions,find_clicked_bottle, user_input_to_action,game_is_finished,start_animations, generate_layout, Button

def solver_initializer_ui(screen_width,screen_height):
    ## UI to select game_size and capacity
    
    # Graphical Input
    bottle_width = 0.4
    bottle_edge_thickness = 0.05
    background_color = (105,105,105)    
    game_size = 8
    capacity = 4
    
    pygame.init()
    screen = pygame.display.set_mode((screen_width,screen_height))
    clock = pygame.time.Clock()
    pygame.display.set_caption('Water Sort! Solver!')

    # Buttons
    drawn_items = []
    
    # The enter button
    sprite = button_sprite((420,75),'Black','Blue','Enter')
    button_rect = sprite.get_rect(center=(screen_width / 2, screen_height/2 - 100))
    enter_button = Button(button_rect,sprite,'ntr_btn')
    drawn_items.append(enter_button)
    
    ## The four buttons for a adjustable button thing
    # The game Adjustable button 
    sprite = button_sprite((200,75),'Black','White','Number of bottles in the game')
    button_rect = sprite.get_rect(center=(screen_width/2 - 110, screen_height/2))
    txt_gamesize_button = Button(button_rect,sprite,'slc_btn')
    drawn_items.append(txt_gamesize_button)
    
    # The game game_size button 
    sprite = button_sprite((200,75),'Black','White',f"{game_size}")
    button_rect = sprite.get_rect(center=(screen_width/2 - 110, screen_height/2 + 80))
    adj_gamesize_button = Button(button_rect,sprite,'adj_gs_btn')
    drawn_items.append(adj_gamesize_button)

    # The game increase button 
    sprite = button_sprite((40,20),'Gray','Black','Up')
    button_rect = sprite.get_rect(center=((screen_width/2 - 110) + 65, (screen_height/2 + 80) - 15))
    increase_button = Button(button_rect,sprite,'inc_btn')
    drawn_items.append(increase_button)
    
    # The game decrease button 
    sprite = button_sprite((40,20),'Gray','Black','Down')
    button_rect = sprite.get_rect(center=((screen_width/2 - 110) + 65, (screen_height/2 + 80) + 15))
    decrease_button = Button(button_rect,sprite,'dcr_btn')
    drawn_items.append(decrease_button)
    
    ## The four buttons for a adjustable button thing
    # The game Adjustable button 
    sprite = button_sprite((200,75),'Black','White','Number of liquids in each bottle')
    button_rect = sprite.get_rect(center=(screen_width/2 + 110, screen_height/2))
    txt_capacity_button = Button(button_rect,sprite,'slc_btn')
    drawn_items.append(txt_capacity_button)
    
    # The game game_size button 
    sprite = button_sprite((200,75),'Black','White',f"{capacity}")
    button_rect = sprite.get_rect(center=(screen_width/2 + 110, screen_height/2 + 80))
    adj_capacity_button = Button(button_rect,sprite,'adj_cp_btn')
    drawn_items.append(adj_capacity_button)

    # The game increase button 
    sprite = button_sprite((40,20),'Gray','Black','Up')
    button_rect = sprite.get_rect(center=((screen_width/2 + 110) + 65, (screen_height/2 + 80) - 15))
    increase_cap_button = Button(button_rect,sprite,'inc_cap_btn')
    drawn_items.append(increase_cap_button)
    
    # The game decrease button 
    sprite = button_sprite((40,20),'Gray','Black','Down')
    button_rect = sprite.get_rect(center=((screen_width/2 + 110) + 65, (screen_height/2 + 80) + 15))
    decrease_cap_button = Button(button_rect,sprite,'dcr_cap_btn')
    drawn_items.append(decrease_cap_button)
    
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
                click = event.pos
        
            if click != None:
                if enter_button.is_clicked(click):
                    print(f"Game size: {game_size}\nCapacity: {capacity}")
                    solver_layout_ui(game_size,capacity,screen_width,screen_height)
                
                if increase_button.is_clicked(click):
                    game_size += 1 
                    
                    for i,item in zip(range(len(drawn_items)),drawn_items):
                        if item.name() == 'adj_gs_btn':
                            # The game game_size button 
                            sprite = button_sprite((200,75),'Black','White',f"{game_size}")
                            item.change_sprite(sprite)
                            drawn_items[i] = item

                if decrease_button.is_clicked(click):
                    if game_size != 0:
                        game_size -= 1 
                    
                    for i,item in zip(range(len(drawn_items)),drawn_items):
                        if item.name() == 'adj_gs_btn':
                            # The game game_size button 
                            sprite = button_sprite((200,75),'Black','White',f"{game_size}")
                            item.change_sprite(sprite)
                            drawn_items[i] = item
                            
                if increase_cap_button.is_clicked(click):
                    capacity += 1 
                    
                    for i,item in zip(range(len(drawn_items)),drawn_items):
                        if item.name() == 'adj_cp_btn':
                            # The game game_size button 
                            sprite = button_sprite((200,75),'Black','White',f"{capacity}")
                            item.change_sprite(sprite)
                            drawn_items[i] = item

                if decrease_cap_button.is_clicked(click):
                    if capacity != 2:
                        capacity -= 1 
                    
                    for i,item in zip(range(len(drawn_items)),drawn_items):
                        if item.name() == 'adj_cp_btn':
                            # The game game_size button 
                            sprite = button_sprite((200,75),'Black','White',f"{capacity}")
                            item.change_sprite(sprite)
                            drawn_items[i] = item                            
                            
                            
                                        
        # fill the screen with a color to wipe away anything from last frame
        screen.fill((105,105,105))
        # Draw all the current state
        for item in drawn_items:
            item.draw(screen)
    
        pygame.display.flip()
        clock.tick(60)

def color_selector_ui(layout,chosen_bottle,game_size,capacity,screen_width,screen_height):
    ## UI to select the contents of a bottle
    
    colors = ['Red','Blue','Green','yellow','Orange','Purple','cadetblue2','darkcyan','darkmagenta','crimson']
    cur_layout = layout[chosen_bottle]
    
    pygame.init()
    screen = pygame.display.set_mode((screen_width,screen_height))
    clock = pygame.time.Clock()
    pygame.display.set_caption('Water Sort! Solver!')    
    
    # The enter button
    sprite = button_sprite((200,75),'Black','White','Confirm')
    button_rect = sprite.get_rect(center=(screen_width / 4 - 50, screen_height/2))
    confirm_button = Button(button_rect,sprite,'ntr_btn')
    
    # Var that keeps track of what is pressed considering swatch/bottle
    select = 0
    
    # Game loop
    while True:
        screen.fill((105,105,105))
        confirm_button.draw(screen)
        # Made an incredibly difficult algorithm which was replaced by these two beautifull numbers
        # I am just going to ignore fixing this now. It is just the box within the bottle sits on the x axis
        # Deal with it. 
        x = (screen_width/2 - 100) + 25
        w = 150
        
        draw_bottle(screen,screen_width/2 - 100,screen_height/2 - 250,500,0.4,0.05,cur_layout,capacity)
        
        # Draws the swatch to the right hand of the screen 
        size = screen_height / len(colors)
        for i,color in enumerate(colors): 
            pygame.draw.rect(
            screen,
            color,
            (screen_width - size,0 + (i*size),size,size)
            )
        
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
                click = event.pos
                x_click, y_click = click
                
                # Confirm bottle:
                if confirm_button.is_clicked(click):
                    layout[chosen_bottle] = cur_layout
                    solver_layout_ui(game_size,capacity,screen_width,screen_height,layout=layout)
                
                # Checks if the bottle was pressed
                if x_click > x and x_click < x + w:
                    # Add stuff if swatch was pressed
                    if type(select) == str:
                        if len(cur_layout) != capacity:
                            cur_layout.append(select)
                        select = 0
                        
                    # Double press removes stuff
                    elif select > 0 and len(cur_layout) != 0:
                        cur_layout.pop() 
                        select = 0
                    else:
                        select = 1                        
                    
                # Checks if you pressed swatch
                elif x_click > screen_width - size: 
                    # Checks which swatch you pressed. Chefs kiss solution. 
                    size_swatch  = screen_height / len(colors)
                    j = y_click // size_swatch
                    select = colors[int(j)]
                
                # Check if you clicked away
                else:
                    select = 0
                             
 
        pygame.display.flip()
        clock.tick(60)  

    
def solver_layout_ui(game_size,capacity,screen_width,screen_height,layout=None):
    ## UI to get the layout of the game
    if layout == None:
        layout = [[] for _ in range(game_size)]  
    # Graphical Input
    bottle_width = 0.4
    bottle_edge_thickness = 0.05
    background_color = (105,105,105)    
    game_size = 8
    capacity = 4
    
    bottle_positions,bottle_size = GetBottlePositions(game_size,bottle_width,screen_width,screen_height)
    
    pygame.init()
    screen = pygame.display.set_mode((screen_width,screen_height))
    clock = pygame.time.Clock()
    pygame.display.set_caption('Water Sort! Solver!')
    
    # The enter button
    sprite = button_sprite((100,30),'Black','Blue','Enter')
    button_rect = sprite.get_rect(center=(screen_width / 2, screen_height/2))
    enter_button = Button(button_rect,sprite,'ntr_btn')

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
        
            if event.type == pygame.MOUSEBUTTONDOWN:
                (x_click,y_click) = event.pos
                click = x_click, y_click
                # Searches if the user clicked on a bottle and if so stores it in chosen_bottle
                chosen_bottle = find_clicked_bottle(bottle_positions,bottle_size,bottle_width,x_click,y_click)
                
                # Lets you adjust the contents of the clicked bottle 
                if chosen_bottle != None:
                    color_selector_ui(layout,chosen_bottle,game_size,capacity,screen_width,screen_height)
        
        if click != None:
            if enter_button.is_clicked(click):
                print(layout)
        
        # fill the screen with a color to wipe away anything from last frame
        screen.fill((105,105,105))
        # Draw all the current state
        draw_gamestate(
            screen,
            layout,
            capacity,
            game_size,
            bottle_width,
            bottle_edge_thickness,
            screen_width,
            screen_height
            )
        
        enter_button.draw(screen)
        
        pygame.display.flip()
        clock.tick(60)     
        
     
if __name__ == "__main__":
    #solver_initializer_ui(1000,600)
    layout = [[] for _ in range(8 )]   
    layout[0] = ['Red','Green','Orange','Yellow']
    color_selector_ui(layout,0,8,4,1000,600)