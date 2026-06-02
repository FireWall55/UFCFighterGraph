class Fighter:
    def __init__(self, name, nickname, height, weight):
        self.name = name
        self.nickname = nickname
        self.height = height
        self.weight = weight
    def __str__(self):
        return f"Fighter: {self.name}, nick: {self.nickname}, height: {self.height}, weight: {self.weight}"
    
    #def __hash__(self):
    #    return hash(self.name)

    #def __eq__(self, other):
    #    return isinstance(other, Fighter) and self.name == other.name