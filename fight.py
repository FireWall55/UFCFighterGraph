class Fight:
    def __init__(self, date, location, winner, weight_class, gender):
        self.date = date
        self.location = location
        self.winner = winner
        self.weight_class = weight_class
        self.gender = gender
    
    def __str__(self):
        return f"{self.date}, {self.location}, {self.winner}, {self.weight_class}, {self.gender}"