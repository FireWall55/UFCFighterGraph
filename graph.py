from fighter import Fighter
import csv
from datetime import datetime

class Graph:
    def __init__(self):
        self.adj_list = {}
        self.fighters = {} #map of name -> Fighter object
        self.adj_matrix = []
        self.edges = []


    def add_fighter(self, fighter):
        if fighter in self.adj_list:
            return
        self.adj_list[fighter] = []

        self.fighters[fighter.name] = fighter #maps fighter's name -> fighter object

    def parse_fighter_data(self, fileName):
        startTime = datetime.now()
        with open(fileName, mode='r', newline='', encoding="utf-8") as file:
            csv_reader = csv.reader(file)
            header = next(csv_reader)

            for i, row in enumerate(csv_reader):
                
                name = row[0]
                nickname = row[1]
                height = row[5]  
                weight = row[6]
                fighter = Fighter(name, nickname, height, weight)
                self.add_fighter(fighter)
                

                #add in everyone from ufc-fighters-statistics and skip over the data in ufc-master if the person does not exist in the dataset
        endTime = datetime.now()
        totalTime = endTime - startTime
        print(f"Time to compile all fighters: {totalTime}")
    def parse_fights(self, fileName):
        with open(fileName, mode='r', newline='', encoding="utf-8") as file:
            csv_reader = csv.reader(file)
            header = next(csv_reader)

            for row in csv_reader:
                fighter1 = row[0]
                fighter2 = row[1]
                if((not fighter1 in self.fighters) or (not fighter2 in self.fighters)):
                    continue
                date = row[6]
                location = row[7]
                winner = ""
                if(row[10]=="Red"):
                    winner = fighter1.name
                else:
                    winner = fighter2.name
                winner = row[10]
                

graph = Graph()
graph.parse_fighter_data(fileName='ufc-fighters-statistics.csv')
graph.parse_fights(fileName="ufc-master.csv")
#for key,value in graph.fighters.items():
#    print(f"name: {key}, object: {value}\n")