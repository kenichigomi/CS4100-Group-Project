import matplotlib.pyplot as plt
from cache_example import get_and_set
import osmnx as ox 
import networkx as nx
import random 
import math

def init_graph(location, format):
    """ 
    Set up G given an initial location
    """
    if format == "place":
        G = ox.graph_from_place(location, network_type="walk")

    if format == "point":
        G = ox.graph_from_point(location, network_type="walk")

    return G

def get_pois(place: str) -> list:
    """
    Returns a list of points of interests in a given graph 
    Gets POI's from OSM and not from looking at the street graph 
    """
    pois = []
    tags = {
        "amenity": ["park", "drinking_water", "toilets", "cafe", "fountain"], 
        "tourism": ["attraction", "viewpoint", "monument"]
    }

    gdf = ox.features_from_place(place, tags=tags) # a table of feature name, amenity, and geometry as columns

    for _, row in gdf.iterrows():
        geometry = row.geometry
        pois.append((geometry.centroid.y, geometry.centroid.x)) # (latitude, longitude)
        # .centroid handles where the geometry is a polygon, and instead get its center point

    return pois

def get_pois_nodes(G, PLACE: str) -> list:
    all_pois = get_pois(PLACE)
    return [ox.nearest_nodes(G, lon, lat) for lat, lon in all_pois]

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
            dist_y = (wp_data["y"] - poi_data["y"]) * 110540

            # using pythagorean theorem to find the distance between the two points
            dist = (dist_x**2 + dist_y**2) ** 0.5

            if dist < min_dist:
                min_dist = dist
        
        score -= min_dist # only care about the poi that are closest to the waypoint 

    # how close the route is to the intended distance 
    len_error = abs(target_len - path_len) / path_len
    score -= len_error * 1000
    
    return score

# testing code above
# print("Starting....")
# G = init_graph("Boston, Massachusetts, USA", "place")
# origin_lat, origin_lon = 42.3601, -71.0589
# origin_node = ox.nearest_nodes(G, origin_lon, origin_lat)
# target_len = 6437.38 # in meters (approx. 4 miles)

# all_pois = get_pois("Boston, Massachusetts, USA")
# print("Number of Points of Interest:", len(all_pois))
# poi_nodes = [ox.nearest_nodes(G, lon, lat) for lat, lon in all_pois] # converting to long,lat
# waypoints = random.sample(poi_nodes, 3) 

# print("Building route.....")
# route = build_route(G, origin_node, waypoints)
# print("Route building finished!")

# # finding actual route length 
# print("Finding length of route....")
# actual_route_len = 0
# for u,v in zip(route[:-1], route[1:]):
#     actual_route_len += G[u][v][0]["length"]
# print("Route Length Found!")

# print("Calculating score....")
# score = score_route(waypoints, actual_route_len, target_len, poi_nodes, G)

# print("************************************")
# print("Finished! Metrics:")
# print("Route Score:", score)
# print("Desired Length:", target_len)
# print("Actual Length:", actual_route_len)

# # Buiding a visual for graph and route:

# # starting node is green 
# # poi are red (can add specific color for what kind of POI it is and add a key)
# # route line is blue 

# node_colors = []
# for node in G.nodes():
#     if node in poi_nodes and node in waypoints:
#         node_colors.append("red")
#     elif node == origin_node:
#         node_colors.append("green")
#     else:
#         node_colors.append("none")


# ox.plot_graph_route(
#     G, 
#     route,
#     route_color="blue",      
#     route_linewidth=4, 
#     node_color = node_colors,      
#     node_size=20,            
#     bgcolor="white"          
# )

# TODO: ignore points that are a certain distance (over half the target distance)
# TODO: When picking waypoints out of POI's, pick 2 way points that are closest to approx. 1/3 of the distance
# TODO: we may be calculating the length of the route incorrectly.....


# New idea:
# TODO: Heuristic is how far this state is from the goal distance 
# always add a node if we are under the distance we want, get rid of a node if we are over
# the distance we want
# First, we start by placing 1 poi, then we do what was mentioned above. We keep iterating
# the state using local search until we reach a distance that is "close enough" using a buffer

def heuristic(G, u, v):
    """straight-line distance between two nodes in meters.
 
    A* heuristic: admissible bc the straight-line distance is always <= the actual walking distance, 
    so A* will find the true shortest path.
    """
    dx = (G.nodes[u]["x"] - G.nodes[v]["x"]) * 111_320  
    dy = (G.nodes[u]["y"] - G.nodes[v]["y"]) * 110_540 
    return math.sqrt(dx**2 + dy**2)
 
 
def build_route_astar(G, origin, waypoints: list) -> list:
    """uses A* with our heuristic 
 
    A* uses f(n) = g(n) + h(n) where g is cost so far and h is our
    Euclidean heuristic. 
    since h is admissible, this finds the optimal path.
    """
    final_route = []
    intermediate_pts = [origin] + waypoints + [origin]
 
    for i in range(len(intermediate_pts) - 1):
        curr_node = intermediate_pts[i]
        next_node = intermediate_pts[i + 1]
 
        try:
            path = nx.astar_path(
                G, curr_node, next_node,
                heuristic=lambda u, v: heuristic(G, u, v),
                weight="length"
            )
        except nx.NetworkXNoPath:
            return None  # no path exists, skip this route
 
        if len(final_route) > 0:
            path = path[1:]
 
        final_route.extend(path)
 
    return final_route
 
 
def get_route_length(G, route: list) -> float:
    """add up the length of every edge in the route (in meters)"""
    total = 0
    for u, v in zip(route[:-1], route[1:]):
        total += G[u][v][0]["length"]
    return total
 
 
def get_neighbor(waypoints, all_pois):
    """generate a neighboring state by making one small change
 
    randomly chooses a move:
      - add a new POI to the route
      - remove a POI from the route
      - or swap one POI for a different one
    """
    neighbor = list(waypoints)  # copy so we don't change the original
    unused_pois = [p for p in all_pois if p not in neighbor]
 
    # figure out which moves are possible right now
    moves = []
    if len(neighbor) < 6 and unused_pois:
        moves.append("add")
    if len(neighbor) > 1:
        moves.append("remove")
        moves.append("swap_two")
    if neighbor and unused_pois:
        moves.append("swap_with_new")
 
    move = random.choice(moves)
 
    if move == "add":
        neighbor.append(random.choice(unused_pois))
 
    elif move == "remove":
        neighbor.pop(random.randrange(len(neighbor)))
    elif move == "swap_two":
        first_idx = random.randrange(len(neighbor))
        second_idx = random.randrange(len(neighbor))
        neighbor[first_idx], neighbor[second_idx] = neighbor[second_idx], neighbor[first_idx]

    elif move == "swap_with_new":
        i = random.randrange(len(neighbor))
        neighbor[i] = random.choice(unused_pois)
    print('chose move', move)
    return neighbor
 
 
def simulated_annealing(G, start_node, all_poi_nodes, target_distance):
    """use simulated annealing to find a route close to the target distance
 
    start with a random set of waypoints and at, each step, make a small 
    change (add/remove/swap a waypoint)
    if the new route is better, keep it
    if worse, keep it anyway with probability e^(-delta/T)
    - when T is high, we accept bad moves often and model explores widely
    - When T is low, we only accept improvements
    """
    # SA parameters
    temperature = 1000.0   
    decay = 0.995          
    max_steps = 1000
    score_list = list()
    route_list = list()
 
    # start with 3 random POI waypoints
    current_waypoints = random.sample(all_poi_nodes, min(3, len(all_poi_nodes)))
    current_route = build_route_astar(G, start_node, current_waypoints)
 
    if current_route is None:
        raise RuntimeError("Could not build an initial route.")
 
    current_len = get_route_length(G, current_route)
    current_score = score_route(current_waypoints, current_len,
                                target_distance, all_poi_nodes, G)
 
    # keep track of the best route we've ever seen
    best_waypoints = list(current_waypoints)
    best_route = list(current_route)
    best_score = current_score
    scores = []
 
    for step in range(max_steps):
 
        # generate a neighbor by tweaking the waypoints
        new_waypoints = get_neighbor(current_waypoints, all_poi_nodes)
        new_route = build_route_astar(G, start_node, new_waypoints)
 
        if new_route is None:
            continue  # bad route, try again
 
        new_len = get_route_length(G, new_route)
        new_score = score_route(new_waypoints, new_len,
                                target_distance, all_poi_nodes, G)
        
        # save route and score at current step
        score_list.append(new_score)
        route_list.append(new_route)
 
        # decide whether to accept the new route
        # score_route returns higher = better, so flip the sign for SA
        delta = current_score - new_score  # positive means new is worse
 
        if delta <= 0:
            # new route scored higher so always accept
            accept = True
        else:
            probability = math.exp(-delta / temperature)
            accept = random.random() < probability
            print('new route is worse — accept with decreasing probability', probability, accept)
 
        if accept:
            current_waypoints = new_waypoints
            current_route = new_route
            current_score = new_score
 
        # update best if this is the highest score we've seen
        if current_score > best_score:
            best_waypoints = list(current_waypoints)
            best_route = list(current_route)
            best_score = current_score
 
        # cool down the temperature
        temperature *= decay
        scores.append(current_score)
 
        if step % 50 == 0:
            print(f"step {step}: T={temperature:.1f}, "
                  f"route={new_len:.0f}m, score={current_score:.1f}")
            print(f'{step=} plotting...')
            plot_route(G, best_route, start_node, best_waypoints, all_poi_nodes, "route.png")
            plt.plot(scores)
            plt.savefig('scores.png')
            plt.close()
    return best_route, best_waypoints, best_score
 
 

# visualizing the graph 
def plot_route(G, route, origin_node, waypoint_nodes, poi_nodes, name,show=False):
    """Plot the route on the map.
    Green = start, red = visited POIs, blue = route path.
    """
    node_colors = []
    node_sizes = []
    for node in G.nodes():
        if node == origin_node:
            node_colors.append("green")
            node_sizes.append(25)
        elif node in poi_nodes and node in waypoint_nodes:
            node_colors.append("red")
            node_sizes.append(20)
        elif node in poi_nodes:
            node_colors.append("red")
            node_sizes.append(1)
        else:
            node_colors.append("none")
            node_sizes.append(20)
 
    ox.plot_graph_route(
        G, route,
        route_color="blue",
        route_linewidth=4,
        node_color=node_colors,
        node_size=node_sizes,
        bgcolor="white",
        close=True,
        filepath=name, 
        save=True, show=show
    )


def main(place, origin_lat, origin_lng, target_miles):
    target_meters = target_miles * 1609.34
    # load the street map
    G = get_and_set(place, lambda: init_graph(place, "place"))
    print("map loaded")

 
    # find the nearest graph node to our starting coordinates
    origin_node = ox.nearest_nodes(G, origin_lng, origin_lat)
 
    # get all POIs and snap them to graph nodes
    poi_nodes = get_and_set(f'pois{place}',lambda: get_pois_nodes(G, place))
    print(f"found {len(set(poi_nodes))} unique POIS nodes")
 
    # run simulated annealing to find a good route
    print("trying to optimize route with simulated annealing")
    best_route, best_waypoints, best_score = simulated_annealing(
        G, origin_node, poi_nodes, target_meters
    )
 
    # print results
    final_length = get_route_length(G, best_route)
    print()
    print("route found")
    print(f"target: {target_meters:.0f}m ({TARGET_MILES} miles)")
    print(f"actual: {final_length:.0f}m ({final_length/1609.34:.2f} miles)")
    print(f"error:  {abs(final_length - target_meters):.0f}m")
    print(f"stops:  {len(best_waypoints)} waypoints")
    print(f"score:  {best_score:.1f}")
 
    # show the route on a map
    plot_route(G, best_route, origin_node, best_waypoints, poi_nodes, f"best route.png")
 

# main command
if __name__ == "__main__":
 
    PLACE = "Boston, Massachusetts, USA"
    ORIGIN_LAT, ORIGIN_LON = 42.3601, -71.0589
    ORIGIN_LAT, ORIGIN_LON = 42.338926939992874, -71.08678413327202
    TARGET_MILES = 4
    main(PLACE, ORIGIN_LAT, ORIGIN_LON, TARGET_MILES)

