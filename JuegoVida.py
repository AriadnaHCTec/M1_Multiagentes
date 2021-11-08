"""
Modifico el juego de la vida que programó Edgar Covantes de Mty
Él lo hizo todo para Jupyter usando GColab y tomando datos usando el DataCollector
Nos dio el código en un GDrive
Octubre 8, 2021
"""

# La clase `Model` se hace cargo de los atributos a nivel del modelo, maneja los agentes. 
# Cada modelo puede contener múltiples agentes y todos ellos son instancias de la clase `Agent`.
from mesa import Agent, Model 

# Debido a que necesitamos un solo agente por celda elegimos `SingleGrid` que fuerza un solo objeto por celda.
from mesa.space import MultiGrid

# Con `SimultaneousActivation` hacemos que todos los agentes se activen de manera simultanea.
from mesa.time import SimultaneousActivation
import numpy as np


class GameLifeAgent(Agent):
    '''
    Representa a un agente o una celda con estado vivo (1) o muerto (0)
    '''
    def __init__(self, unique_id, model, x, y):
        '''
        Crea un agente con estado inicial aleatorio de 0 o 1, también se le asigna un identificador 
        formado por una tupla (x,y). También se define un nuevo estado cuyo valor será definido por las 
        reglas mencionadas arriba.
        '''
        super().__init__(unique_id, model)
        self.live = np.random.choice([0,1])
        self.next_state = None
        self.x = x
        self.y = y
        
    
    def step(self):
        '''
        Este método es el que calcula si la celda vivirá o morirá dependiendo el estado de sus vecinos.
        El estado live de la siguiente generación no se cambia aquí se almacena en self.next_state. La idea 
        es esperar a que todos los agentes calculen su estado y una vez hecho eso, ya hacer el cambio.
        '''
        
        neighbours = self.model.grid.get_neighbors(
            self.pos,
            moore=True,
            include_center=False)
        
        #pos = np.random.choice(neighbours)
        #print(pos)
    
    #agregie la función
     def move(self):
        possible_steps = self.model.grid.get_neighborhood(
            self.pos,
            moore=True,
            include_center=False
        )
        new_position = self.random.choice(possible_steps)
        self.model.grid.move_agent(self, new_position)
            
class GameLifeModel(Model):
    '''
    Define el modelo del juego de la vida.
    '''
    def __init__(self, width, height):
        self.num_agents = width * height
        self.grid = MultiGrid(width, height, True)
        self.schedule = SimultaneousActivation(self)
        self.running = True #Para la visualizacion usando navegador
        
        i = 0
        for (content, x, y) in self.grid.coord_iter():
            a = GameLifeAgent(i, self,x,y)
            self.grid.place_agent(a, (1, 1))
            self.schedule.add(a)
            i+=1
        
    
    def step(self):
        self.schedule.step()
