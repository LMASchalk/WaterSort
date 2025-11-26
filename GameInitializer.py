from Bottle import Bottle

class WaterSortGame:
    def __init__(self,size: int, capacity: int,layout: list) -> None:
        self.gamestate = [Bottle(capacity,layout[i]) for i in range(size)]
        self.size = size - 1
        self.capacity = capacity
    
    def show_gamestate(self) -> None:
        for bottle in self.gamestate:
            print(bottle.content)
    
    def get_content_bottles(self) -> list:
        contents = []
        for Bottle in self.gamestate:
            contents.append(Bottle.content)
        return contents
    
    def transfer_liquid(self,bottle_1: int,bottle_2: int) -> None:
        
        if bottle_1 > self.size or bottle_2 > self.size:
            raise Exception('There are not that many bottles')
    
    # Use case when not possible
    # Bottle 2 is full
    # Bottle 1 is empty
    # bottle 1 is finished
    # if the top of bottle one is not the same as the top of bottle two unless bottle 2 is empty
    
        if self.gamestate[bottle_2].is_full():
            return
        if self.gamestate[bottle_1].volume() == 0:
            return
        if self.gamestate[bottle_1].is_finished():
            return
        if not self.gamestate[bottle_2].is_empty():
            if self.gamestate[bottle_1].top_of_bottle() != self.gamestate[bottle_2].top_of_bottle():
                return
        
        # fill it till the depth of bottle 1 unless there is not enough space in bottle 2 then just fill it till bottle 2 is full
        transfer_color = self.gamestate[bottle_1].top_of_bottle()
        if self.gamestate[bottle_2].space_left() >= self.gamestate[bottle_1].liquid_depth():
            for _ in range(self.gamestate[bottle_1].liquid_depth()):
                self.gamestate[bottle_1].remove_content()
                self.gamestate[bottle_2].add_content(transfer_color)
        else:
            for _ in range(self.gamestate[bottle_2].space_left()):
                self.gamestate[bottle_1].remove_content()
                self.gamestate[bottle_2].add_content(transfer_color)                            
        
    def is_finished(self) -> bool: 
        for bottle in self.gamestate:
            if not bottle.is_empty():
                if not bottle.is_finished():
                    return False
        return True
    
    def is_transfer_possible(self,move) -> bool:
        bottle_1, bottle_2 = move 
        
        if bottle_1 > self.size or bottle_2 > self.size:
            raise Exception('There are not that many bottles')
        
    # Use case when not possible
    # Bottle 2 is full
    # Bottle 1 is empty
    # bottle 1 is finished
    # if the top of bottle one is not the same as the top of bottle two unless bottle 2 is empty
        
        if self.gamestate[bottle_2].is_full():
            return False
        if self.gamestate[bottle_1].volume() == 0:
            return False
        if self.gamestate[bottle_1].is_finished():
            return False
        if not self.gamestate[bottle_2].is_empty():
            if self.gamestate[bottle_1].top_of_bottle() != self.gamestate[bottle_2].top_of_bottle():
                return False
        
        return True
    
    
    def get_layout(self) -> list:
        layout = []
        for bottle in self.gamestate:
            layout.append(bottle.content)
        
        return layout
        
        
        

