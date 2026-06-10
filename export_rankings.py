from graph import Graph
import json
from datetime import datetime

print("Loading graph...")
graph = Graph()
graph.parse_fighter_data(fileName='ufc-fighters-statistics.csv')
graph.parse_fights(fileName='ufc-master.csv')

# Filter to only fighters with at least one fight
active_fighters = [
    fighter for fighter, edges in graph.adj_list.items()
    if len(edges) > 0
]
total = len(active_fighters)
print(f"Computing centrality for {total} active fighters (skipping {len(graph.adj_list) - total} with 0 edges)...")

rankings = []
for i, fighter in enumerate(active_fighters):
    print(f"  [{i+1}/{total}] {fighter.name}...")
    degree    = graph.degree_centrality(fighter.name)
    closeness = graph.closeness_centrality(fighter.name)
    rankings.append({
        'name':      fighter.name,
        'nickname':  fighter.nickname,
        'degree':    degree,
        'closeness': closeness,
    })

with open('rankings.json', 'w', encoding='utf-8') as f:
    json.dump(rankings, f, ensure_ascii=False)

print(f"\nDone. rankings.json written with {len(rankings)} fighters.")