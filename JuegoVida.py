"""
Modifico el juego de la vida que programó Edgar Covantes de Mty
Él lo hizo todo para Jupyter usando GColab y tomando datos usando el DataCollector
Nos dio el código en un GDrive
Octubre 8, 2021
"""

# La clase `Model` se hace cargo de los atributos a nivel del modelo, maneja los agentes. 
# Cada modelo puede contener múltiples agentes y todos ellos son instancias de la clase `Agent`.
from mesa import Agent, Model, model 

# Debido a que necesitamos un solo agente por celda elegimos `SingleGrid` que fuerza un solo objeto por celda.
from mesa.space import MultiGrid

# Con `SimultaneousActivation` hacemos que todos los agentes se activen de manera simultanea.
from mesa.time import SimultaneousActivation
import numpy as np

from mesa.datacollection import DataCollector
import pandas as pd

class Sucio(Agent):
    '''
    Representa a un agente o una celda con estado vivo (1) o muerto (0)
    '''
    def __init__(self, unique_id, model):
        '''
        Crea un agente con estado inicial aleatorio de 0 o 1, también se le asigna un identificador 
        formado por una tupla (x,y). También se define un nuevo estado cuyo valor será definido por las 
        reglas mencionadas arriba.
        '''
        super().__init__(unique_id, model)
        self.live = 1
    
    def kill(self):
        self.live = 0


    
class Robot(Agent):
    '''
    Representa a un agente o una celda con estado vivo (1) o muerto (0)
    '''
    def __init__(self, unique_id, model):
        '''
        Crea un agente con estado inicial aleatorio de 0 o 1, también se le asigna un identificador 
        formado por una tupla (x,y). También se define un nuevo estado cuyo valor será definido por las 
        reglas mencionadas arriba.
        '''
        super().__init__(unique_id, model)
    
    def step(self):
        '''
        Este método es el que calcula si la celda vivirá o morirá dependiendo el estado de sus vecinos.
        El estado live de la siguiente generación no se cambia aquí se almacena en self.next_state. La idea 
        es esperar a que todos los agentes calculen su estado y una vez hecho eso, ya hacer el cambio.
        '''
        cellmates = self.model.grid.get_cell_list_contents([self.pos])         
        algoSucio = False
        for cellmate in cellmates:
            if type(cellmate) is Sucio:
                print(cellmate)
                print("pos")
                print(cellmate.pos)
                self.model.grid._remove_agent(self.pos, cellmate) 
                algoSucio = True
                self.model.num_dirty -= 1 #se elimino uno unu $$$
                #print(self.model.num_dirty)#imprime cuantos hay actualmente $$$
            self.model.listaSucios.append(self.model.num_dirty) # esta lista nos puede servir 
                                                          #para graficar cuantos sucios hay en cada step $$$
            print(self.model.listaSucios) #imprime la lista para ver que funciona(se puede comentar)$$$
        if not algoSucio:
            self.move()

    #agrege la función
    def move(self):
        possible_steps = self.model.grid.get_neighborhood(
            self.pos,
            moore=True,
            include_center=False
        )
        new_position = self.random.choice(possible_steps)
        self.model.grid.move_agent(self, new_position)  


def obtain_info(model):#Esta funcion es para guardar el grid en cada step pero no me jalo con datacollector
    """Sirve para obtener información y regresarla para guardarla."""
    grid = np.zeros((model.grid.width, model.grid.height))
    for cell in model.grid.coord_iter():
        cell_content, x, y = cell
        grid[x][y] = cell_content.live
    return grid

class GameLifeModel(Model):
    '''
    Define el modelo del juego de la vida.
    '''
    def __init__(self, width, height, N = 5, dirty = .50):
        self.num_agents = width * height
        self.grid = MultiGrid(width, height, True)
        self.schedule = SimultaneousActivation(self)
        #self.schedule = RandomActivation(self) ? 
        self.running = True #Para la visualizacion usando navegador
        
        
        self.listaSucios = []#lista para graficar cunatos sucios habia en cada step$$$
        self.numberOfIterations = 100#numero de veces que se va a correr el programa (steps) $$$
        self.num_dirty = 0#numero e sucios en el ambiente$$$
        #Guardar info
        #self.datacollector = DataCollector({"info": obtain_info})

        for (contents, x, y) in self.grid.coord_iter():
            if self.random.random() < dirty:
                # Create a tree
                new_Sucio = Sucio((x, y), self)
                self.grid._place_agent((x, y), new_Sucio)
                self.schedule.add(new_Sucio)
                self.num_dirty += 1 #cuantos Sucios se crearon $$$
        self.listaSucios.append(self.num_dirty)
        for i in range (N):
            a = Robot(i, self)
            self.grid.place_agent(a, (1, 1))
            self.schedule.add(a)        
        
    
    def step(self):
        #Guardar info
        # self.datacollector.collect(self)
        self.numberOfIterations -= 1#se resta para que llegue a cero$$$
        if self.numberOfIterations > 0:#si no es cero sigue corriendo$$$
            self.schedule.step()
        else:#llego a cero, se para el programa$$$
            self.stop()#no se como parar el modelo desde la clase $$$
            print(self.num_dirty/self.num_agents)#porcentaje de casillas sucias en el ambiente $$$


