
# Shiny Frontend for CS4100 Running Route AI Project

# CS4100, Spring 2026

# Contributors



# imports
from shiny import App, reactive, render, ui
import main as main
import osmnx as ox
import sim_aneal as sa
from caching import get_and_set
import os
import time

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
                        ui.input_numeric(id="lat", value=42.3601, label="Latitude of starting point:"),
                        ui.input_numeric(id="lon", value=-71.0589, label="Longitude of starting point:"),
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
                        {"style": "text-align: center;"},
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
                        ui.p("Creating a good running route takes time. We can use Strava, " \
                        "an app that shares GPS data from users to plot a route to base our own routes off of, "
                        "or Google Maps to draw a route - but each come with their own problems. Strava doesn't have a " \
                        "good feature to search for a particular distances, and Google Maps forces the user to " \
                        "drag and drop markers to create a loop. Our research led us to an existing route creator " \
                        "called 'TrailRouter', but this program was optimized for plotting a route near green spaces (parks, etc.)"
                        " and would not always create a convenient running route. We introduce the idea of a looped route here, "
                        "as we can run on new paths for the entirety of the route rather than running on the same path twice "
                        "(out-and-back). This allows for greater exploration of the city, and an overall more enjoyable experience. We wanted to use AI methods to create an agent that could develop a looping route given a distance that the user wants to run, a city to create the route in, a starting location at which the route would also end at (thus closing the loop), and potential waypoints that the route could go through. These waypoints included public amenities and touristy spots, providing the runner with either resources (water, bathroom) or a nice view (scenery, or maybe some cool building). We hope that with this model, users will be able to cut down on time spent creating a running route and have a more enjoyable time outside.")
                    ),
                    ui.card(
                        ui.card_header("Methodology", style="background-color: #C2EBEF"),
                        ui.p("Street map data is pulled from OpenStreetMap using OSMnx, where intersections are represented as " \
                        "nodes and street segments as directed edges with distance weights. To bias the search toward runner-friendly " \
                        "paths, a contraction preprocessing step assigns each edge a rank based on its road type. For example, footways "
                        "and pedestrian paths receive a rank of 1, residential streets a rank of 2, and motorways and alleys a rank of 8. " \
                        "Edges exceeding a rank threshold of 5 are removed from the graph entirely, producing a reduced graph G' that " \
                        "filters out roads unsuitable for running. Candidate waypoints, including parks, fountains, monuments, and cafes, " \
                        "are queried from OSM's feature API and snapped to their nearest graph node. Routes are constructed by chaining A* " \
                        "shortest-path segments between consecutive waypoints into a closed loop returning to the origin, using an admissible" \
                        " Euclidean heuristic that converts degree differences in latitude and longitude to meters. The system then optimizes " \
                        "the set of waypoints using simulated annealing, beginning with a random sample of 3 POI waypoints and iteratively " \
                        "proposing neighbor states by adding, removing, or swapping a single waypoint, with the waypoint count capped at 6. " \
                        "Each candidate route is scored by penalizing waypoint distance from the nearest POI, edge repetition weighted at -500 " \
                        "per repeated edge, and normalized deviation from the target distance weighted at -1000. Transitions to worse states " \
                        "are accepted with probability P = e^{-Delta/T}, where T decays exponentially at alpha = 0.995$ per step over " \
                        "1,000 total iterations starting at T = 1000, using random restarts to reheat T by 200 after 100 consecutive " \
                        "steps without improvement. The main libraries used are OSMnx, NetworkX, Matplotlib, and Shiny for Python for the frontend. " \
                        "Some limitations of this system include its reliance on OpenStreetMap data being complete for the target city, and " \
                        "the fact that the returned route may deviate from the desired distance by a few meters, since the model returns the " \
                        "closest result found after 1,000 iterations. The system is also currently limited to walking networks, with no support "
                        "for cycling or driving routes.  ")
                    ),
                    ui.div(
                        ui.card(
                            ui.card_header("Contributors", style="background-color: #C2EBEF"),
                            ui.tags.ul(
                                ui.tags.li("Ife Adeyosoye"),
                                ui.tags.li("Noah Büttner"),
                                ui.tags.li("Mihika Chalasani"),
                                ui.tags.li("Kenichi Gomi")
                                ),
                            width="50%",
                            style="flex: 1;"
                        ),
                        ui.card(
                            ui.card_header("Links", style="background-color: #C2EBEF"),
                            ui.tags.ul(
                                ui.tags.li(ui.tags.a("Github", href="https://github.com/kenichigomi/CS4100-Group-Project"))
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
        PLACE = input.place()
        ORIGIN_LON = input.lon()
        ORIGIN_LAT = input.lat()
        TARGET_METERS = input.dist() * 1609

        G = get_and_set(PLACE,lambda: sa.init_graph(PLACE, "place"))
        origin_node = ox.nearest_nodes(G, ORIGIN_LON, ORIGIN_LAT)

        poi_nodes = get_and_set("pois"+PLACE, lambda: sa.get_pois_nodes(PLACE, G))

        best_route, best_waypoints, best_score = sa.simulated_annealing(
            G, origin_node, poi_nodes, TARGET_METERS
        )   
        final_length = sa.get_route_length(G, best_route)
        image, axes = sa.plot_route(G, best_route, origin_node, best_waypoints, poi_nodes)
        image.savefig("route.png")

        
        path = "route.png"
        return {"src": path, "height": "100%"}

 

app = App(app_ui, server)