# CS4100 Spring 2026 Final Project - AI Running Route Generator

### Group Members
- Ife Adeyosoye
- Noah Büttner
- Mihika Chalasani
- Kenichi Gomi

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

## Conclusion/Future Work
- Reheating methods could be improved (variation in # of steps, how much to reheat)
- Try using different models such as Neural Networks
- Increase computation performance to speed up front end (user interaction)
- Assign values to osmnx paths and modify scoring to promote usage of specific paths over others (contraction.py)


## Appendix
- Files
  - Main script: main.py
    - Pulls functions from relevant scripts to generate a route given inputs 
  - AI methods and helper functions: sim_aneal.py
    - Contains simulated annealing and relevant functions (such as scoring)
  - Front end: app.py
    - Calling "shiny run app.py" in terminal will launch Shiny app
