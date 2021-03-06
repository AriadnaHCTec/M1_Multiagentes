"""
Visualizador del Juego de la Vida
Esta parte es completamente diferente a la que hizo Edgar pues el lo hace todo en Jupyter
Octubre 8, 2021
"""
from JuegoVida import *
from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer


def agent_portrayal(agent):
    portrayal = {"Shape": "circle",
                 "Filled": "true",
                 "Layer": 0,
                 "Color": "red",
                 "r": 0.5}
    if type(agent) is Robot:
        portrayal["scale"] = 0.9
        portrayal["Layer"] = 1

    elif type(agent) is Sucio:
        portrayal["Color"] = "grey"
        portrayal["Layer"] = 1
        portrayal["r"] = 0.1
    return portrayal

ancho = 20
alto = 20
N = 5
dirty = .50

"""
#Codigo como de jupyter notebook para obtener información recolectada
#no funcionó unu
model = GameLifeModel(ancho, alto)
for i in range(10):
    model.step()
all_grid = model.datacollector.get_model_vars_dataframe()
#all_grid.plot()
"""

grid = CanvasGrid(agent_portrayal, ancho, alto, 750, 750)
server = ModularServer(GameLifeModel,
                       [grid],
                       "Trafic Model",
                       {"width":ancho, "height":alto, "N":5, "dirty":.5, "NI":300})
server.port = 8521 # The default
server.launch()
