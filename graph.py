from fighter import Fighter
from fight import Fight
from edge import Edge
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
                    continue #if one of the fighters isn't listed in the database
                date = row[6]
                location = row[7]
                winner = row[10]
                weight = row[12]
                gender = row[13]


                fight = Fight(date, location, winner, weight, gender)
                #need to find if a current edge exists
                fighter1_o = self.fighters[fighter1]
                fighter2_o = self.fighters[fighter2]
                edge = Edge(fighter1, fighter2)
                for edge_t in self.adj_list[fighter1_o]: #temporary edge
                    if edge_t.fighter1==fighter1 or edge_t.fighter2==fighter2:
                        edge = edge_t
                        
                edge.addFight(fight)
                
                self.adj_list[fighter1_o].append(edge)
                self.adj_list[fighter2_o].append(edge)

                
                

graph = Graph()
graph.parse_fighter_data(fileName='ufc-fighters-statistics.csv')
graph.parse_fights(fileName="ufc-master.csv")
for key,value in graph.adj_list.items():
    if len(value) > 0:
        print(f"{key}: {value} : {value[0]}")
#for key,value in graph.fighters.items():
#    print(f"name: {key}, object: {value}\n")