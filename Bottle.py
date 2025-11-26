class Bottle:
    def __init__(self,capacity: int,content: list) -> None:
        self.capacity = capacity
        self.content = content
        if self.volume() > self.capacity:
            raise Exception('Exceeded capacity')
    
    def volume(self) -> int:
        return len(self.content)
    
    def is_full(self) -> bool:
        if self.volume() == self.capacity:
            return True
        return False 
    
    def is_empty(self) -> bool:
        return self.volume() == 0
    
    def space_left(self) -> int:
        return self.capacity - self.volume()
    
    def is_finished(self) -> bool:
        if not self.is_full():
            return False
        # asks if there is only 1 unique item in the list
        if len(set(self.content)) == 1:
            return True
        return False
    
    def top_of_bottle(self) -> str:
        return self.content[-1]
    
    def liquid_depth(self) -> int:
        top = self.top_of_bottle()
        i=0
        for i in range(1,self.volume()):
            if self.content[-1-i] != top:
                return i 
        return i + 1
    
    def add_content(self,item: str) -> None:
        if self.volume() >= self.capacity:
            raise Exception('Exceeded capacity')
        else:
            self.content.append(item)
    
    def remove_content(self) -> None:
        if self.is_empty():
            raise Exception('Bottle is empty, removal is impossible')
        else:
            self.content.pop(-1)
            