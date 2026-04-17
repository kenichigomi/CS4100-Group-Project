# CS4100 Final Project - AI Running Route Generator

### Group Members
- Ife Adeyosoye
- Noah Büttner
- Mihika Chalasani
- Kenichi Gomi

## Problem Statement/Motivation
- Running routes can be a bit difficult to make manually
- Apps like Google Maps tend to make out-and-back routes instead of loops
- Want to use AI methods to generate a looping route given a user's preferred distance

## Approach
- Simulated Annealing
  - Reheating as an equivalent method to random restarts
  - Scored based on distance to waypoints, total distance, and # of repeated edges


## Appendix
- Files
  - Main script: main.py
    - Pulls functions from relevant scripts to generate a route given inputs 
  - Simulated Annealing: sim_aneal.py
  - Front-end: app.py
    - By calling "shiny run app.py" in terminal the Shiny app will launch
