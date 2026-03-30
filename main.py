import osmnx as ox 
import networkx as nx
import random 

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
print("Starting....")
G = init_graph("Boston, Massachusetts, USA", "place")
origin_lat, origin_lon = 42.3601, -71.0589
origin_node = ox.nearest_nodes(G, origin_lon, origin_lat)
target_len = 6437.38 # in meters (approx. 4 miles)

all_pois = get_pois("Boston, Massachusetts, USA")
print("Number of Points of Interest:", len(all_pois))
poi_nodes = [ox.nearest_nodes(G, lon, lat) for lat, lon in all_pois] # converting to long,lat
waypoints = random.sample(poi_nodes, 2) 

print("Building route.....")
route = build_route(G, origin_node, waypoints)
print("Route building finished!")

# finding actual route length 
print("Finding length of route....")
actual_route_len = 0
for u,v in zip(route[:-1], route[1:]):
    actual_route_len += G[u][v][0]["length"]
print("Route Length Found!")

print("Calculating score....")
score = score_route(waypoints, actual_route_len, target_len, poi_nodes, G)

print("************************************")
print("Finished! Metrics:")
print("Route Score:", score)
print("Desired Length:", target_len)
print("Actual Length:", actual_route_len)

# Buiding a visual for graph and route:

# starting node is green 
# poi are red (can add specific color for what kind of POI it is and add a key)
# route line is blue 

node_colors = []
for node in G.nodes():
    if node in poi_nodes and node in waypoints:
        node_colors.append("red")
    elif node == origin_node:
        node_colors.append("green")
    else:
        node_colors.append("none")


ox.plot_graph_route(
    G, 
    route,
    route_color="blue",      
    route_linewidth=4, 
    node_color = node_colors,      
    node_size=20,            
    bgcolor="white"          
)

# TODO: ignore points that are a certain distance (over half the target distance)
# TODO: When picking waypoints out of POI's, pick 2 way points that are closest to approx. 1/3 of the distance
# TODO: we may be calculating the length of the route incorrectly.....