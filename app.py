
# Shiny Frontend for CS4100 Running Route AI Project

# CS4100, Spring 2026

# Contributors
# - Ife Adeyosoye
# - Noah Büttner
# - Mihika Chalasani
# - Kenichi Gomi


# imports
from shiny.express import input, render, ui
#from main import *


with ui.sidebar(position="left", 
                bg="#846FBD",
                title="CS4100 Project"):  
    ui.input_text("place", "What city do you want to run in?", "(text)")
    ui.input_text("lat", "Where is your origin latitude?", "(float)")
    ui.input_text("lon", "Where is your origin longitude?", "(float)")

    


