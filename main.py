import matplotlib.pyplot as plt
from cache_example import get_and_set
import osmnx as ox 
import networkx as nx
import random 
import math
import sim_aneal as sa
import contraction as con
import time 

# main command
if __name__ == "__main__":
    start_time_G = time.time()
    PLACE = "Boston, Massachusetts, USA"
    ORIGIN_LAT, ORIGIN_LON = 42.3601, -71.0589
    TARGET_MILES = 4
    TARGET_METERS = TARGET_MILES * 1609.34
 
    # load the street map
    G = get_and_set(PLACE,lambda: sa.init_graph(PLACE, "place"))
    print("map loaded")
    print("contraction started...")
    G_prime = con.apply_contraction(G, max_rank=5)

    # find the nearest graph node to our starting coordinates
    origin_node = ox.nearest_nodes(G, ORIGIN_LON, ORIGIN_LAT)
    
    # get all POIs and snap them to graph nodes
    poi_nodes = get_and_set("pois"+PLACE, lambda: sa.get_pois_nodes(PLACE, G))
    print(f"found {len(set(poi_nodes))} unique pois nodes")
    
    # run simulated annealing to find a good route
    print("trying to optimize route with simulated annealing...")
    best_route, best_waypoints, best_score = sa.simulated_annealing(
        G, origin_node, poi_nodes, TARGET_METERS
    )
 
    # print results
    final_length = sa.get_route_length(G, best_route)
    print()
    print("route found")
    print(f"target:  {TARGET_METERS:.0f} m  ({TARGET_MILES} miles)")
    print(f"actual:  {final_length:.0f} m  ({final_length/1609.34:.2f} miles)")
    print(f"error:   {abs(final_length - TARGET_METERS):.0f} m")
    print(f"stops:   {len(best_waypoints)} waypoints")
    print(f"score:   {best_score:.1f}")
    
    # show the route on a map
    image, axes = sa.plot_route(G, best_route, origin_node, best_waypoints, poi_nodes)
    end_time_G = time.time() 
    image.savefig("route.png")

    # Now trying with contraction Heirchies

     # find the nearest graph node to our starting coordinates
    origin_node = ox.nearest_nodes(G_prime, ORIGIN_LON, ORIGIN_LAT)
    start_time_G_prime = time.time()
 
    # get all POIs and snap them to graph nodes
    all_pois = sa.get_pois(PLACE)
    
    poi_nodes = [
    ox.nearest_nodes(G_prime, lon, lat) 
    for lat, lon in all_pois
    if ox.nearest_nodes(G_prime, lon, lat) in G_prime.nodes()
    ]

    # also make sure they are reachable from origin
    poi_nodes = [
        p for p in poi_nodes 
        if nx.has_path(G_prime, origin_node, p)
    ]

    print(f"reachable POIs in contracted graph: {len(poi_nodes)}")

    # run simulated annealing to find a good route
    print("trying to optimize route with simulated annealing...")
    best_route, best_waypoints, best_score = sa.simulated_annealing(
        G_prime, origin_node, poi_nodes, TARGET_METERS
    )
 
    # print results
    final_length = sa.get_route_length(G_prime, best_route)
    print()
    print("route found")
    print(f"target: {TARGET_METERS:.0f}m ({TARGET_MILES} miles)")
    print(f"actual: {final_length:.0f}m ({final_length/1609.34:.2f} miles)")
    print(f"error:  {abs(final_length - TARGET_METERS):.0f}m")
    print(f"stops:  {len(best_waypoints)} waypoints")
    print(f"score:  {best_score:.1f}")
 
    # show the route on a map
    sa.plot_route(G_prime, best_route, origin_node, best_waypoints, poi_nodes)
    end_time_G_prime = time.time()

    print("Time for G:", end_time_G - start_time_G, "seconds")
    print("Time for G':", end_time_G_prime - start_time_G_prime, "seconds")

 
