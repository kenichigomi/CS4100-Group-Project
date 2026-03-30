import os
import pickle

import networkx as nx
import osmnx as ox
import matplotlib as plt


def set_cache(key, data):
    # Pickling (serializing) the data to a file
    with open(f"{key}.pkl", "wb") as file:
        pickle.dump(data, file)


def get_cache(key):
    if not os.path.exists(f"{key}.pkl"):
        return None
    with open(f"{key}.pkl", "rb") as file:
        return pickle.load(file)


def get_and_set(key, callback):
    key = "boston cache"
    value = get_cache(key)
    if value is None:
        value = callback()
        set_cache(key, value)
    return value


G = get_and_set(
    "boston",
    lambda: ox.graph.graph_from_place(
        "Boston, Massachusetts, USA", network_type="walk"
    ),
)
print(G)
fig, ax = ox.plot.plot_graph(G)
