import mesa
from model import Cyborg
from agents import Mangrove

# function that is called every step for every field and every agent to decide how it should be displayed
def draw(agent):
    # if there is no agent on a field
    # return nothing
    if agent is None:
        return

    # else create a "portrayal" object (dictionary) with the needed parameters
    # casing (lower or upper case letters are always important!)
    # we define a standard portrayal that is used by default for all agents
    # in a dictionary every "key" has a "value" ({"key": "value"})
    # an individual value of a dictionary can be accessed by specifiying the "key" you want to read the "value" for
    # portrayal["Color"] -> "blue"
    # see https://www.w3schools.com/python/python_dictionaries.asp
    portrayal = {
        "Color": "blue",
        "Shape": "circle",
        "Layer": 0,
        "Filled": "true", # here the boolean (True, False) value is given as a string (text), this is not the default in Python!
        "r": 0.5 # radius of the circle
    }

    # if the agent is a mangrove though, we overwrite the variable portrayal
    # so far all agents are Mangroves, so the default will never be used
    if isinstance(agent, Mangrove):
        portrayal = {
            # "green" in RGBA looks like that: "rgba(0, 128, 0, 1)""
            # values have to be between 0 and 255, transparency 0 to 1
            # make the color green, but more transparent when health decreases
            # use "abs" (absolute value) and "round" to make sure the number is positive and one digit decimal
            "Color": "rgba(0, 128, 0, {})".format(abs(round(agent.health, 1))),
            "Shape": "rect",
            "Layer": 0,
            "Filled": "true",
            "w": 1, # height of the field
            "h": 1 # 
        }
    # use another "if" or "elif" (else if) to check another agent type, or any other property
    # e.g.: elif isinstance(agent, Trash): ...
    # instead of defining the default portrayal above,
    # you can also use "else" in the end to set the portrayal if no condition before was met

    # return the portrayal that has been set
    return portrayal

# initialize the canvas to draw on with a size in fields and pixels
canvas = mesa.visualization.CanvasGrid(draw, 40, 40, 600, 600)

# set charts to visualize the development of the model
# "Label" must correspond to a model_reporter set in model.py
pop_charts = mesa.visualization.ChartModule([
    {"Label": "Mangroves", "Color": "green"}
])
fertility_charts = mesa.visualization.ChartModule([
    {"Label": "Avg. Mangrove Fertility", "Color": "purple"}
])
life_expectancy_charts = mesa.visualization.ChartModule([
    {"Label": "Avg. Mangrove Life Expectancy", "Color": "blue"}
])

# Sliders for modifiying parameters going into the model
# parameters must be defined in the constructor of the model
# those will overwrite the defaults set in the model constructor
# read what the numbers mean by hovering with the cursor above the "Slider"
model_params = {
    "mangrove_fertility": mesa.visualization.Slider("Mangrove fertility", 0.1, 0, 1, 0.05),
    "mangrove_life_expectancy": mesa.visualization.Slider("Mangrove Life Expectancy", 10, 0, 20, 1),
    "mangrove_density": mesa.visualization.Slider("Mangrove Density", 0.15, 0, 1, 0.05)
}

# initialize the server with the model, parameters and visualization elements set above
# give it a name of your choosing
server = mesa.visualization.ModularServer(
    model_cls=Cyborg,
    visualization_elements=[canvas, pop_charts, fertility_charts, life_expectancy_charts],
    name="Cyborg Jakarta",
    model_params=model_params
)
