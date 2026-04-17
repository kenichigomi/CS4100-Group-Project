# Our approach that still uses A* and local search with sim annealing but tries to use Contraction Heirchies 
# tries to avoid roads that are not the best running paths and avoiding traffic lights 
import osmnx as ox 
import networkx as nx
import random 
import math
import sim_aneal as sa



road_importance_levels = {
    # best for running (preferred)
    "track": 1, # like a pathway in a park for example
    "path": 1, 
    "footway": 1, 
    "cycleway": 2, # runners can still run on this, but not the best 
    "living_street": 2, 
    "pedestrian": 2, 
    "residential": 2, 
    "unclassified": 3, # looking at the pictures 

    "tertiary": 4, 
    "secondary": 5, 

    # avoid for running (avoided)
    "primary":        6,
    "trunk":          7,  
    "motorway":       8,  
    "service":        8,  
    "alley":          8 
}

def get_road_rank(edge_data) -> int:
    """
    A method that gets the ranking of a road for a runner
    If the road/edge does not have a label/ranking, we will assume it is the worst case option
    """
    road_type = edge_data.get("highway", "alley") # assume it is an alley in the worst case if it isn't labeled
    if isinstance(road_type, list): 
        road_type = road_type[0]
    return road_importance_levels.get(road_type, 8) # default to 4 if it is something we havent seen before 

def apply_contraction(G, max_rank=5): 
    """
    
    """
    edges_to_remove = []

    for u, v, data in G.edges(data=True):
        if get_road_rank(data) > max_rank:
            edges_to_remove.append((u, v))
    
    G.remove_edges_from(edges_to_remove)
    return G



