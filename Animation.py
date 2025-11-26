class Animation:
    def __init__(self,animation_name:str,animation_type:str,start_time:int,end_time:int,animation_attribute:any,animation_position:tuple,animation_screen,screen_dims:tuple):
        self.__name = animation_name 
        self.__type = animation_type
        self.__starttime = start_time
        self.__step = 0
        self.__endtime =  end_time
        self.attribute = animation_attribute
        self.__screen = animation_screen
        self.__position = animation_position
        self.__screen_dims = screen_dims
        
    def name(self) -> str:
        return self.__name
    def type(self) -> str:
        return self.__type
    def starttime(self) -> int:
        return self.__starttime
    def step(self):
        return self.__step
    def endtime(self) -> int:
        return self.__endtime
    def screen(self):
        return self.__screen
    def position(self) -> tuple:
        return self.__position
    def screendims(self) -> tuple:
        return self.__screen_dims
    def next_step(self) -> None:
        self.__step += 1
    
    def change_position(self,new_position) -> None:
        x1,y1 = self.__position
        x2,y2 = new_position
        self.__position = (x2,y2)
    
    def progress(self) -> float:        
        return self.__step / (self.__endtime - self.__starttime)
    
    def length(self) -> int:
        return (self.__endtime - self.__starttime)
        
    def finished(self) -> bool:
        if self.__starttime + self.__step > self.__endtime:
            return True
        else:
            return False

    