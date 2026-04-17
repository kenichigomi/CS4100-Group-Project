# CS4100 Spring 2026 Final Project - AI Running Route Generator

### Group Members
- Ife Adeyosoye
- Noah Büttner
- Mihika Chalasani
- Kenichi Gomi

# How to run the project
## 1.) Make sure to clone repository
```
git clone [repo_name]
cd [repo_name]
```
## 2.) Make sure python 3.14 is installed.

## 3.) Install libraries/dependencies.
```
pip install [library_name]

osmnx
networkx
matplotlib
random
math
time
shiny
sys
os
```

## 4.) You can either run the Shiny app, or simply run main.py.

If running the Shiny app, type in terminal:
```
shiny run app.py
```
Else run main.py after modifying the variables.
```
PLACE (string): City, State, Country of interest (ex. Boston, Massachusetts, USA)
ORIGIN_LAT, ORIGIN_LON (float, float): Latitude and Longitude of starting location in above PLACE
TARGET_MILES (float): Number of miles user wants to run
TARGET_METERS (float): This script is based on meters. If MILES is the measurement of choice
                       then input MILES * 1609. Otherwise input meters.
```

```
python main.py
```

# Directory
```
/misc
  kenichi_osm_test.ipynb     # osmnx/networkx playground
/scripts
  /caches                    # contains caches to speed up graphing
  /outputs                   # contains output images from main.py
  app.py                     # Shiny application
  caching.py                 # helper functions to cache graph data
  contraction.py            
  main.py                    # runs model
  sim_aneal.py               # contains sim aneal function and associated helper functions
```

# Report
## Problem Statement/Motivation
- Running routes can be a bit difficult to make manually
- Apps like Google Maps tend to make out-and-back routes instead of loops
- Looped routes are nice because you get to explore more, see different things
- Want to use AI methods to generate a looping route given a user's preferred distance
  - Route through waypoints such as public amenities or touristy spots to help with looping

## Approach
- Used osmnx library to interact with OpenStreetMaps to get path data and plot routes
  - Was able to filter to only pedestrian paths such as sidewalks
- Simulated Annealing using A* Search
  - Scored based on distance to waypoints, total distance, and # of repeated edges
  - Reheating as an equivalent method to random restarts
    - Apply if no improvements observed after 100 steps
 
## Results
- Model consistently (and successfully) made looped routes
- Tended to use 2~3 waypoints on average
- Score was converging towards 0 after being heavily penalized in its initial steps (improvement)

<img src="https://i.ibb.co/SX7Yf1Th/d2097e36-fe30-4e51-8f73-9bd97701c794.png" width="400">
Sample 10km Route in Boston, Massachusetts

## Conclusion/Future Work
- Reheating methods could be improved (variation in # of steps, how much to reheat)
- Try using different models such as Neural Networks
- Increase computation performance to speed up front end (user interaction)
- Assign values to osmnx paths and modify scoring to promote usage of specific paths over others (contraction.py)
