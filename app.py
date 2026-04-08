
# Shiny Frontend for CS4100 Running Route AI Project

# CS4100, Spring 2026

# Contributors



# imports
from shiny import App, reactive, render, ui
import main as main
import osmnx as ox
import os

# This is code for what the app will look like
app_ui = ui.page_navbar(
    ui.nav_panel("App",
                ui.div(
                    ui.card(
                        ui.card_header("Instructions", style="background-color: #C2EBEF"),
                        ui.tags.ol(
                            ui.tags.li("Input the city or location you want the running route to be in"),
                            ui.tags.li("Input the starting point for your run in a (latitude, longitude) format"),
                            ui.tags.li("Change the number of miles you want to run (default is 5)"),
                            ui.tags.li("Hit run, and see your route be generated below!")
                            ),
                        ui.div(
                            ui.input_action_button(id="run_ai", label="Run!!", width="50%"),
                            style="display: flex; justify-content: center;"
                        ),
                        width="50%",
                        style="flex: 1;"
                    ),
                    ui.card(
                        ui.card_header("Inputs", style="background-color: #C2EBEF"),
                        ui.input_text(id="place", value="Boston, Massachusetts, USA", label="City/Location you want to run in:"),
                        ui.input_text(id="latlon", value="(42.3601, -71.0589)", label="Coordinates of starting point:"),
                        ui.input_numeric(id="dist", value=5, label="Number of Miles you want to run:"),
                        width="50%",
                        style="flex: 1;"
                    ),
                    # would be cool to have progress bar while training/evaluating
                    # another card for map
                style="display: flex; gap: 10px;"
                ),
                ui.div(
                    ui.card(
                        ui.card_header("Route", style="background-color: #C2EBEF"),
                        ui.output_image("ai_route")
                    )
                )
    ), 

    # Page for discussing the project methodology 
    ui.nav_panel("About the Project",
                ui.div(
                    ui.card(
                        ui.card_header("Background", style="background-color: #C2EBEF"),
                        ui.p("Mapping technology is very good at making routes from point A to point B. However for runners, " \
                        "usually the goal is to start and end a run at the same point. We found that there were not many resources " \
                        "that would make a route this way in a loop, so we decided to make an AI agent that would solve this problem. " \
                        "Running in cities can also be very hectic, so we wanted our agent to avoid as many crosswalks or interruptions " \
                        "during the run as possible, but also allowing the agent to explore places of interest such as monuments or water " \
                        "fountains.")
                    ),
                    ui.card(
                        ui.card_header("Methodology", style="background-color: #C2EBEF"),
                        ui.p()
                    ),
                    ui.div(
                        ui.card(
                            ui.card_header("Contributors", style="background-color: #C2EBEF"),
                            ui.tags.ul(
                                
                                ),
                            width="50%",
                            style="flex: 1;"
                        ),
                        ui.card(
                            ui.card_header("Links", style="background-color: #C2EBEF"),
                            ui.tags.ul(
                                ui.tags.li(ui.tags.a("Github", href="https://github.com/kenichigomi/CS4100-Group-Project")),
                                ui.tags.li("Insert link for PDF paper here when completed"),
                                ui.tags.li("Insert link for slideshow when completed")
                            ),
                            width="50%",
                            style="flex: 1;"
                        ),
                        style="display: flex; gap: 10px;"
                    )
                ),
    ),
    title="CS4100 Final Project - Running Route AI Creator",  
    id="page",
    bg="#A8CAD6",

)

# define/run functions from main here
def server(input, output, session):
    
    @render.image
    @reactive.event(input.run_ai, ignore_none=True)
    def ai_route():

        place = input.place()
        latlon_str = input.latlon()
        lat, lon = eval(latlon_str)
        dist = input.dist()

        main.main(place, lat, lon, dist)

        path = "best route.png"
        return {"src": path, "width": "100%"}

 

app = App(app_ui, server)




