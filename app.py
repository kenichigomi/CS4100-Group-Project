
# Shiny Frontend for CS4100 Running Route AI Project

# CS4100, Spring 2026

# Contributors
# - Ife Adeyosoye
# - Noah Büttner
# - Mihika Chalasani
# - Kenichi Gomi


# imports
from shiny import App, reactive, render, ui
#from main import *
import tqdm

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
                 )
    ), 

    # Page for discussing the project methodology 
    ui.nav_panel("About the Project",
                 ui.div(
                     ui.card(
                        ui.card_header("Background", style="background-color: #C2EBEF"),
                    ),
                    ui.card(
                        ui.card_header("Methodology", style="background-color: #C2EBEF")
                    ),
                    ui.card(
                        ui.card_header("Contributors", style="background-color: #C2EBEF"),
                        ui.tags.ul(
                            ui.tags.li("Ife Adeyosoye"),
                            ui.tags.li("Noah Büttner"),
                            ui.tags.li("Mihika Chalasani"),
                            ui.tags.li("Kenichi Gomi")
                            )
                    ),
                    ui.card(
                        ui.card_header("Links", style="background-color: #C2EBEF"),
                        ui.tags.ul(
                            ui.tags.li(ui.tags.a("Github", href="https://github.com/kenichigomi/CS4100-Group-Project")),
                            ui.tags.li("Insert link for PDF paper here when completed"),
                            ui.tags.li("Insert link for slideshow when completed")
                        )
                    )
                ),
    ),
    title="CS4100 Final Project - Running Route AI Creator",  
    id="page",
    bg="#A8CAD6",

)

# define/run functions from main here
def server(input, output, session):
    pass

app = App(app_ui, server)




