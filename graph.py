from fighter import Fighter
from fight import Fight
from edge import Edge
import csv
from datetime import datetime
from collections import deque
import json

class Graph:
    def __init__(self):
        self.adj_list = {} #map of object -> edges
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
                winner = row[9]
                weight = row[11]
                gender = row[12]


                fight = Fight(date, location, winner, weight, gender)
                #need to find if a current edge exists
                fighter1_o = self.fighters[fighter1]
                fighter2_o = self.fighters[fighter2]
                edge = Edge(fighter1, fighter2)
                rematch = False
                for edge_t in self.adj_list[fighter1_o]: #temporary edge
                    if (edge_t.fighter1==fighter1 and edge_t.fighter2==fighter2) or edge_t.fighter1==fighter2 and edge_t.fighter2==fighter1:
                        edge = edge_t
                        #print("adding to already existing edge (there is a rematch)")
                        rematch = True
                        
                edge.addFight(fight)
                if not rematch:
                    self.adj_list[fighter1_o].append(edge)
                    self.adj_list[fighter2_o].append(edge)
    def degree_centrality(self, fighter): #takes in the name
        fighter_o = self.fighters[fighter]
        edges = self.adj_list[fighter_o]
        count = 0
        for edge in edges:
            count+=1
        return count/(len(self.adj_list)-1) # 0 if connected to nobody, 1 if connected to everybody 
    def weighted_degree_centrality(self):
        """
        Weighted Degree Centrality: total number of fights (not just opponents).
        Fighters who fought more frequently rank higher even vs. the same opponents.
        """
        centrality = {}
        fighters = list(self.adj_list.keys())
        n = len(fighters)
        if n <= 1:
            return centrality

        max_fights = 0
        raw = {}
        for fighter, edges in self.adj_list.items():
            total_fights = sum(len(edge.fights) for edge in edges)
            raw[fighter.name] = total_fights
            if total_fights > max_fights:
                max_fights = total_fights

        for name, count in raw.items():
            centrality[name] = count / max_fights if max_fights > 0 else 0

        return centrality    
    def betweenness_centrality_single(self, fighter_name):
        if fighter_name not in self.fighters:
            return None

        fighters = list(self.adj_list.keys())
        n = len(fighters)

        # Build name -> neighbors lookup
        adj_by_name = {}
        for fighter, edges in self.adj_list.items():
            neighbors = []
            for edge in edges:
                neighbor = edge.fighter2 if edge.fighter1 == fighter.name else edge.fighter1
                neighbors.append(neighbor)
            adj_by_name[fighter.name] = neighbors

        score = 0.0

        for source in fighters:
            if source.name == fighter_name:
                continue

            # Brandes BFS from this source
            stack = []
            predecessors = {f.name: [] for f in fighters}
            sigma = {f.name: 0 for f in fighters}
            dist  = {f.name: -1 for f in fighters}

            sigma[source.name] = 1
            dist[source.name]  = 0
            queue = deque([source.name])

            while queue:
                v = queue.popleft()
                stack.append(v)
                for w in adj_by_name.get(v, []):
                    if dist[w] == -1:
                        queue.append(w)
                        dist[w] = dist[v] + 1
                    if dist[w] == dist[v] + 1:
                        sigma[w] += sigma[v]
                        predecessors[w].append(v)

            # Accumulate dependency, but only track fighter_name's score
            delta = {f.name: 0.0 for f in fighters}
            while stack:
                w = stack.pop()
                for v in predecessors[w]:
                    if sigma[w] != 0:
                        delta[v] += (sigma[v] / sigma[w]) * (1 + delta[w])
                if w != source.name and w == fighter_name:
                    score += delta[w]

        norm = (n - 1) * (n - 2)
        return score / norm if norm > 0 else 0.0
    def closeness_centrality(self, fighter_name):
        if fighter_name not in self.fighters:
            return None

        n = len(self.adj_list)
        total_dist = 0
        reachable = 0

        for target in self.fighters:
            if target == fighter_name:
                continue
            path = self.bfs(fighter_name, target)
            if path:
                total_dist += len(path) - 1  # edges = nodes - 1
                reachable += 1

        if reachable == 0:
            return 0.0

        # Wasserman-Faust normalization
        return (reachable / (n - 1)) * (reachable / total_dist)



    def bfs(self, start_name, target_name):
        if start_name not in self.fighters:
            return None

        pred = {start_name: None}
        queue = deque([start_name])
        visited = {start_name}

        while queue:
            curr = queue.popleft()
            curr_fighter = self.fighters[curr]
            for edge in self.adj_list[curr_fighter]:
                neighbor = edge.fighter2 if edge.fighter1 == curr else edge.fighter1

                if neighbor in visited:
                    continue

                visited.add(neighbor)
                queue.append(neighbor)
                pred[neighbor] = curr

                if neighbor == target_name:
                    # Build path
                    path = []
                    step = neighbor
                    while step is not None:
                        path.append(step)
                        step = pred[step]
                    path.reverse()
                    return path

        return []  # couldn't find target


    def export_json(self, path="fighters_data.json"):
        out = []
        i = 0
        for fighter, edges in self.adj_list.items():
            if(len(edges)==0):
                continue
            fights = []
            seen = set()
            for edge in edges:
                for fight in edge.fights:
                    key = (fight.date, edge.fighter1, edge.fighter2)
                    if key not in seen:
                        seen.add(key)
                        opponent = edge.fighter2 if edge.fighter1 == fighter.name else edge.fighter1
                        fights.append({
                            "opponent": opponent,
                            "date": fight.date,
                            "winner": fight.winner,
                            "corner": "red" if edge.fighter1 == fighter.name else "blue",
                            "weight_class": fight.weight_class,
                            "gender": fight.gender
                        })
            out.append({
                "name": fighter.name,
                "nickname": fighter.nickname,
                "height": fighter.height,
                "weight": fighter.weight,
                "fights": fights,
                "centrality": {
                    "degree": self.degree_centrality(fighter.name),
                    "weighted_degree": 0,   # plug in your methods
                    "closeness": self.closeness_centrality(fighter.name),
                    "betweenness": self.betweenness_centrality_single(fighter.name)
                }
            })
            i+=1
            print(f"number completed: {i}")
        with open(path, "w", encoding="utf-8") as f:
            json.dump(out, f, ensure_ascii=False)
    def find_rivals(self):
        rivals = []
        seen = set()
        for fighter, edges in self.adj_list.items():
            for edge in edges:
                key = tuple(sorted([edge.fighter1, edge.fighter2]))
                if len(edge.fights) > 1 and key not in seen:
                    seen.add(key)
                    rivals.append((edge.fighter1, edge.fighter2, len(edge.fights)))
        return rivals
                

#graph = Graph()
#graph.parse_fighter_data(fileName='ufc-fighters-statistics.csv')
#graph.parse_fights(fileName="ufc-master.csv")

#print(graph.fighters["Israel Adesanya"])
#print(graph.adj_list[graph.fighters["Israel Adesanya"]][0])
#print(graph.closeness_centrality("Khalid Taha"))
#print(graph.bfs("Khalid Taha", "Charles Johnson"))
#graph.export_json()

