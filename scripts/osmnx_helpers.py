import osmnx as ox
import networkx as nx

import matplotlib.pyplot as plt


def init_graph(location, format):
    """ 
    Set up G given an initial location
    """
    if format == "place":
        G = ox.graph_from_place(location, network_type="walk")

    if format == "point":
        G = ox.graph_from_point(location, network_type="walk")

    return G

def draw_path(start_node, end_node):
    """
    Create a route given a start and end node 
    """
    return

def get_distance(route):
    """ 
    Get the distance of a specific route
    """
    return

def get_metrics(route):
    """
    Get information of a route given its geodataframe, such as whether there are crossings on the path or not 
    """
    return 