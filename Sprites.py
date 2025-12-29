import pygame
from HelperFunctions import GetBottlePositions

def draw_bottle(screen,x:int,y:int,size:int,width:float,thickness:float,content:list,capacity:int) -> None:
    width_bottle = size * width
    edge_width = int(size*thickness)
    
    rectangle_surface = pygame.Surface((width_bottle,size), pygame.SRCALPHA)
    # Creates a rectangle which will be the body of the bottle
    pygame.draw.rect(rectangle_surface,(0,0,0),(0,0,width_bottle,size),width=edge_width)
    pygame.draw.rect(rectangle_surface,(0,0,0,0),(edge_width,0,(width_bottle - (edge_width * 2)), edge_width))
        
    # Creates the fluid in the bottle with the appropriate color
    fluid_size = ((size - (edge_width*2))/ capacity)
    for i,color in enumerate(content,1):
        x_col = edge_width
        y_col = (size-edge_width)-(fluid_size*i) 
        w = width_bottle - (edge_width * 2)
        h = fluid_size
        
        pygame.draw.rect(rectangle_surface,color,
        (
            x_col, # x
            y_col, # y
            w, # width
            h  # height
        ))

    
    screen.blit(rectangle_surface,(x,y))

def draw_gamestate(screen,contents:list,capacity:int,n_bottles:int,bottle_width:float,bottle_thickness:float,screen_width:int,screen_height:int,BorderSize=50,SpacingY=40):
    BottlePositions,size = GetBottlePositions(n_bottles,bottle_width,screen_width,screen_height,BorderSize,SpacingY)

    for bottle_pos,content in zip(BottlePositions,contents):
        x,y = bottle_pos
        draw_bottle(screen,x,y,size,bottle_width,bottle_thickness,content,capacity)
        
def draw_selection(screen,bottle_positions,size,width,thickness,selection,color = 'Red'):
    edge_width = int(size*thickness)
    width_bottle = size * width 
    # Create canvas for the sprite
    rectangle_surface = pygame.Surface(((width_bottle + 2 * edge_width),(size + 2* edge_width)), pygame.SRCALPHA)
    
    # Draws a rectangle with around the bottle 
    pygame.draw.rect(
        rectangle_surface,
        color,
        (0,0,(width_bottle + 2 * edge_width),size + 2* edge_width,),
        width=edge_width
        )
    
    x,y = bottle_positions[selection]
    
    screen.blit(rectangle_surface,(x-edge_width,y-edge_width))
    
def remove_selection(screen,bottle_positions,size,width,thickness,selection,background_color):

    edge_width = int(size*thickness)
    width_bottle = size * width 
    # Create canvas for the sprite
    rectangle_surface = pygame.Surface(((width_bottle + 2 * edge_width),(size + 2* edge_width)), pygame.SRCALPHA)
    
    pass

def draw_convetti(color,size):
    # Creates a surface with a simple rectange with a certain color
    convetti_surface = pygame.Surface((size,size))
    pygame.draw.rect(convetti_surface,color,(0,0,size,size))
    return convetti_surface

def get_font_size(wh:tuple,text:str,padding:float):
    width,height = wh
    
    # Start with a reasonably large font size and decrease until the text fits
    font_size = min(width, height)  # Start with the smaller of width or height
    font = pygame.font.Font(None, font_size)
    text_surface = font.render(text, True, 'Black')

    while text_surface.get_width() > (width*padding) or text_surface.get_height() > (height*padding):
        font_size -= 1  # Decrease font size
        font = pygame.font.Font(None, font_size)
        text_surface = font.render(text, True, 'Black')

    return font_size

def button_sprite(wh:tuple,button_color:str,text_color:str,text:str,selected=False):
    width,height = wh

    if selected:
        edge_size = int(width * 0.02)
        
        # Creates a new surface with an slightly bigger size
        button = pygame.Surface((width + edge_size ,height + edge_size))
        button.fill(button_color)
        pygame.draw.rect(
            button,
            'Red',
            (0,0,(width + edge_size),(height + edge_size)),
            width = edge_size
        )

    else: 
        button = pygame.Surface((width,height))
        button.fill(button_color)
            
        
    font_size = get_font_size(wh,text,0.9)
    font = pygame.font.Font(None, font_size)
    
    text_surface = font.render(text, True, text_color)
    text_rect = text_surface.get_rect(center=(width / 2, height/2))
    button.blit(text_surface,text_rect)
    
    return button