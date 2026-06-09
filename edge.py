class Edge:
    def __init__(self, fighter1, fighter2):
        self.fighter1 = fighter1 #name not object
        self.fighter2 = fighter2
        self.fights = []
        
    def addFight(self, fight):
        self.fights.append(fight)

    def __str__(self):
        return f"{self.fights}"