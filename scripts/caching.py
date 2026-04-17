import os
import pickle

import networkx as nx
import osmnx as ox
import matplotlib as plt


def set_cache(key, data):
    # Pickling (serializing) the data to a file
    with open(f"/caches/{key}.pkl", "wb") as file:
        pickle.dump(data, file)


def get_cache(key):
    if not os.path.exists(f"/caches/{key}.pkl"):
        return None
    with open(f"/caches/{key}.pkl", "rb") as file:
        return pickle.load(file)


def get_and_set(key, callback):
    value = get_cache(key)
    if value is None:
        value = callback()
        set_cache(key, value)
    return value

