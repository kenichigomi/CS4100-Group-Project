import osmnx as ox 
import networkx as nx
import random 

# used if we are doing local search 
def obj_fun(traffic_lights: int, busyness: float, lighting: float) -> float:
    """ Objective function that we want to maximize the overall value

    traffic_lights: the number of traffic lights on this path 
    busyness: average busyness of this path from scale of 0.0 -> 1.0
    lighting: how lit a path is of scale from 0.0 -> 1.0; ex. 0.0 is dark, 1.0 is fully lit 
    """

    value = 0.0
    value -= traffic_lights
    value -= busyness
    value += lighting 

    return value

G = ox.graph_from_place("Boston, Massachusetts, USA", network_type="walk")
origin_lat, origin_lon = 42.3601, -71.0589
origin_node = ox.nearest_nodes(G, origin_lon, origin_lat)

# used if doing random points of interest and finding shortest paths between intermediate points
# need to change this method to find waypoints within a certain distance 
def is_pois(data) -> bool:
    """
    Returns true of the point is a point of interest 
    """

    if data.get("highway") == "traffic_signals": # can create a list of other conditions like footway or residential 
        return False
    
    if data.get("amenity") in ["park", "drinking_water", "toilets", "cafe", "fountain"]:
        return True
    
    if data.get("tourism") in ["attraction", "viewpoint", "monument"]:
        return True

    return False


def get_pois(graph) -> list:
    """
    Returns a list of points of interests in a given graph 
    """
    pois = []

    for node, data in graph.nodes(data=True):
        if is_pois(data):
            pois.append(node)
    
    return pois


def build_route(G, origin, pois: list) -> list:
    """
    Builds a route that puts together shortest paths between nodes to create 
    a good route 
    """

    final_route = []
    intermediate_pts = [origin] + pois + [origin]

    for i in range(len(intermediate_pts) - 1):
        curr_node = intermediate_pts[i]
        next_node = intermediate_pts[i + 1]

        path = nx.shortest_path(G, curr_node, next_node, weight = "length")

        if len(final_route) > 0:
            path = path [1:] # a node will be duplicated so this takes that duplication out 

        final_route.extend(path)

    return final_route


# ifes part for scoring a route
def score_route(waypoints: list, path_len: float, target_len: float, all_pois: list, G) -> float:
    """
    waypoints: list of nodes choosen for the route
    path_len: the actual path length of the route
    target_len: the intended path length of the route 
    all_pois: all points of interests in the graph 
    G: the entire graph 
    """

    score = 0.0

    # how close we are to the waypoints 
    for wp in waypoints:
        wp_data = G.nodes[wp]

        min_dist = float("inf")
        for poi in all_pois:
            poi_data = G.nodes[poi]

            # need to convert degrees into meters
            dist_x = (wp_data["x"] - poi_data["x"]) * 111320 
            dist_y = (wp_data["y"] - poi_data["x"]) * 110540

            # using pythagorean theorem to find the distance between the two points
            dist = (dist_x**2 + dist_y**2) ** 0.5

            if dist < min_dist:
                min_dist = dist
        
        score -= min_dist # only care about the poi that are closest to the waypoint 

    # how close the route is to the intended distance 
    len_error = abs(target_len - path_len) / path_len
    score -= len_error * 1000
    
    return score



# tests 
print(obj_fun(10, 0.7, 0.1))
print(obj_fun(1, 0.1, 0.8))

print(obj_fun(3, 0.2, 0.9))  
print(obj_fun(10, 0.8, 0.1))