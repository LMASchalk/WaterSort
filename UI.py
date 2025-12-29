def UI(level=1):
    from Game import watersort
    from Solver import solver_initializer_ui
    import pygame
    from Sprites import button_sprite
    from HelperFunctions import Button

    game_size = 8
    capacity = 4
    
    screen_width = 1000
    screen_height = 600

    # pygame setup
    pygame.init()
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption('User Interface')
    clock = pygame.time.Clock()

    # A list of items which need to be drawn in each state. Can be updated according to user interaction
    drawn_items = []
    
    # The start button
    sprite = button_sprite((400,75),'Black','Blue','Start Game!')
    button_rect = sprite.get_rect(center=(screen_width / 2, screen_height/4))
    start_button = Button(button_rect,sprite,'srt_btn')
    drawn_items.append(start_button)
    
    # The game difficulty button 
    sprite = button_sprite((200,75),'Black','White','Game Difficulty')
    button_rect = sprite.get_rect(center=(screen_width / 4, screen_height/2))
    dif_button = Button(button_rect,sprite,'df_btn')
    drawn_items.append(dif_button)
    
    # The easy difficulty button
    sprite = button_sprite((150,50),'Black','Green','Easy')
    button_rect = sprite.get_rect(center=((screen_width / 4) - 155, (screen_height/2) + 80))
    easy_button = Button(button_rect,sprite,'easy_btn')
    drawn_items.append(easy_button)
    
    # The medium difficulty button
    sprite = button_sprite((150,50),'Black','Orange','Medium',selected=True)
    button_rect = sprite.get_rect(center=(screen_width / 4, (screen_height/2) + 80))
    medium_button = Button(button_rect,sprite,'medium_btn')
    drawn_items.append(medium_button)
    
    # The hard difficulty button
    sprite = button_sprite((150,50),'Black','Red','Hard')
    button_rect = sprite.get_rect(center=((screen_width / 4) + 155, (screen_height/2) + 80))
    hard_button = Button(button_rect,sprite,'hard_btn')
    drawn_items.append(hard_button)
    
    # The game Adjustable button 
    sprite = button_sprite((200,75),'Black','White','Level Selector')
    button_rect = sprite.get_rect(center=(screen_width*3 / 4, screen_height/2))
    adjustable_button = Button(button_rect,sprite,'slc_btn')
    drawn_items.append(adjustable_button)
    
    # The game level button 
    sprite = button_sprite((200,75),'Black','White',f"{level}")
    button_rect = sprite.get_rect(center=(screen_width*3 / 4, screen_height/2 + 80))
    adjustable_button = Button(button_rect,sprite,'lvl_btn')
    drawn_items.append(adjustable_button)
    
    # The game increase button 
    sprite = button_sprite((40,20),'Gray','Black','Up')
    button_rect = sprite.get_rect(center=((screen_width*3 / 4) + 65, (screen_height/2 + 80) - 15))
    increase_button = Button(button_rect,sprite,'inc_btn')
    drawn_items.append(increase_button)
    
    # The game decrease button 
    sprite = button_sprite((40,20),'Gray','Black','Down')
    button_rect = sprite.get_rect(center=((screen_width*3 / 4) + 65, (screen_height/2 + 80) + 15))
    decrease_button = Button(button_rect,sprite,'dcr_btn')
    drawn_items.append(decrease_button)
    
    # Solver mode button
    sprite = button_sprite((150,50),'Black','White','Solver mode')
    button_rect = sprite.get_rect(center=((screen_width / 2), (screen_height/4) - 100))
    solver_button = Button(button_rect,sprite,'slvr_btn')
    drawn_items.append(solver_button)
        
    running = True
    while running:
        click = None
        # pygame.QUIT event means the user clicked X to close your window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                raise SystemExit

            # Quit the game whenever the ESC key is pressed
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    raise SystemExit

            # Registers a mouse click and stores the location of the click in x_click and y_click
            if event.type == pygame.MOUSEBUTTONDOWN:
                click = event.pos

        # fill the screen with a color to wipe away anything from last frame
        screen.fill((105,105,105))
        
        # Draw all the current state
        for item in drawn_items:
            item.draw(screen)
        
        if click != None:
            if start_button.is_clicked(click):
                pygame.quit()
                watersort(game_size,capacity,level,screen_width,screen_height)
            
            if solver_button.is_clicked(click):
                pygame.quit()
                solver_initializer_ui(screen_width,screen_height)
                
            if easy_button.is_clicked(click):
                game_size = 6
                easy_button.change_sprite(button_sprite((150,50),'Black','Green','Easy',selected=True))
                medium_button.change_sprite(button_sprite((150,50),'Black','Orange','Medium'))
                hard_button.change_sprite(button_sprite((150,50),'Black','Red','Hard'))
                
            if medium_button.is_clicked(click):
                game_size = 8
                easy_button.change_sprite(button_sprite((150,50),'Black','Green','Easy'))
                medium_button.change_sprite(button_sprite((150,50),'Black','Orange','Medium',selected=True))
                hard_button.change_sprite(button_sprite((150,50),'Black','Red','Hard'))
                
            if hard_button.is_clicked(click):
                game_size = 10
                easy_button.change_sprite(button_sprite((150,50),'Black','Green','Easy'))
                medium_button.change_sprite(button_sprite((150,50),'Black','Orange','Medium'))
                hard_button.change_sprite(button_sprite((150,50),'Black','Red','Hard',selected=True))
        
            if increase_button.is_clicked(click):
                level += 1 
                
                for i,item in zip(range(len(drawn_items)),drawn_items):
                    if item.name() == 'lvl_btn':
                        # The game level button 
                        sprite = button_sprite((200,75),'Black','White',f"{level}")
                        item.change_sprite(sprite)
                        drawn_items[i] = item

            if decrease_button.is_clicked(click):
                if level != 0:
                    level -= 1 
                
                for i,item in zip(range(len(drawn_items)),drawn_items):
                    if item.name() == 'lvl_btn':
                        # The game level button 
                        sprite = button_sprite((200,75),'Black','White',f"{level}")
                        item.change_sprite(sprite)
                        drawn_items[i] = item
        
        
        # flip() the display to put your work on screen
        pygame.display.flip()

        clock.tick(60)  # limits FPS to 60

    pygame.quit()

if __name__ == "__main__":
    UI()