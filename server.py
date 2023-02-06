import mesa
from model import Cyborg

def draw(agent):
    if agent is None:
        return

    portrayal = {
        # "green" in RGBA -> rgba(0, 128, 0, 1)
        # values have to be between 0 and 255, transparency 0 to 1
        # make the color green, but more transparent when health decreases
        # use "abs" and "round" to make sure the number is positive and one digit decimal
        "Color": "rgba(0, 128, 0, {})".format(abs(round(agent.health, 1))),
        "Shape": "rect",
        "Layer": 0,
        "Filled": "true",
        "w": 1,
        "h": 1
    }
    return portrayal

canvas = mesa.visualization.CanvasGrid(draw, 40, 40, 600, 600)
pop_charts = mesa.visualization.ChartModule([
    {"Label": "Mangroves", "Color": "green"}
])
fertility_charts = mesa.visualization.ChartModule([
    {"Label": "Mangrove Life Expectancy", "Color": "purple"}
])
life_expectancy_charts = mesa.visualization.ChartModule([
    {"Label": "Mangrove Fertility", "Color": "blue"}
])

# Sliders for modifiying parameters
model_params = {
    "mangrove_fertility": mesa.visualization.Slider("Mangrove fertility", 0.6, 0, 1, 0.1),
    "mangrove_life_expectancy": mesa.visualization.Slider("Mangrove Life Expectancy", 5, 0, 20, 1),
    "mangrove_density": mesa.visualization.Slider("Mangrove Density", 0.3, 0, 1, 0.05)
}

server = mesa.visualization.ModularServer(
    model_cls=Cyborg,
    visualization_elements=[canvas, pop_charts, fertility_charts, life_expectancy_charts],
    name="Cyborg Jakarta",
    model_params=model_params
)
