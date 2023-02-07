from mesa import Agent
import math

# helper function to limit a decimal value between lower and upper bounds
# values in a tuple or list (list = [x,y,z], tuple=(x,y,z)) can be accessed by their index, starting at 0
# list[0] -> x, list[1] -> y, list[2] -> z
# see https://www.w3schools.com/python/python_lists.asp
def clamp(value, bounds=(0,1)) -> float:
    if value < bounds[0]: return bounds[0]
    elif value > bounds[1]: return bounds[1]
    else: return value

# the class for all agents that are mangroves
# inherits all the standard properties from mesa.Agent
class Mangrove(Agent):
    # read about the usage of class properties in model.py
    life: int # maximal life expectancy
    age: int # steps lived
    fertility: float # likelihood of reproduction

    # constructor for a new mangrove
    def __init__(self, unique_id, model, pos, life=5, age=0, fertility=0.6):
        # call the __init__ function of the original mesa.Agent class first
        # add your custom code below
        # sometimes it might be necessary to run your custom code before
        # depends on the code
        super().__init__(unique_id, model)

        # set the position of the new mangrove
        # if an agent should be able to move use self.model.grid.move_agent(agent, new_pos)
        # the pos will update automatically
        self.pos = pos
        # max. life expectancy mutation based on gauss normal distribution
        # so life = 5 leads to a value somewhere around 5
        self.life = self.random.gauss(life, 1)
        # same for fertility some random mutation with standard deviation of 0.05
        # make sure the value stays between 0 and 1 using a simple helper function
        self.fertility = clamp(self.random.gauss(fertility, 0.05))
        # set initial age (not all mangroves are new born at the start)
        self.age = age
    # runs every step of the simulation for every agent of that class
    def step(self):
        # let the mangrove age by 1
        self.age += 1

        # if random number between 0 and 1 is bigger than its health, the mangrove dies
        if self.random.random() > self.health:
            self.model.grid.remove_agent(self)
            self.model.schedule.remove(self)
            # reduce the number of living mangroves by 1
            self.model.mangrove_count -= 1
        else:
            # if the mangrove stays alive
            # it has a chance of reproduction
            if self.random.random() < self.fertility:
                empty_cells = []
                neighbor_cells = self.model.grid.iter_neighborhood(self.pos, True)

                # that got a bit complicated
                # we have to look through all the neighboring cells
                # to check if there is already a mangrove growing there
                # can be used for other agents like trash too
                # if the neighbor cell has no mangroves, we add it to the list of empty cells
                for cell in neighbor_cells:
                    cell_content = self.model.grid.get_cell_list_contents([cell])
                    mangroves_in_cell = [agent for agent in cell_content if isinstance(agent, Mangrove)]
                    if len(mangroves_in_cell) == 0:
                        empty_cells.append(cell)

                # if there is any empty cell,
                # pick a random empty cell
                if (len(empty_cells) > 0):
                    new_pos = self.random.choice(empty_cells)
                    # plant a new mangrove
                    # see the init_mangroves function of the model
                    new_mangrove = Mangrove(
                        unique_id=self.model.next_id(),
                        model=self.model,
                        pos=new_pos,
                        life=self.life * math.sqrt(self.health),  # inherit life expectancy - some penalty for age
                        fertility=self.fertility # inherit fertility
                    )
                    self.model.grid.place_agent(new_mangrove, new_pos)
                    self.model.schedule.add(new_mangrove)
                    self.model.mangrove_count += 1

    # for functions as properties see model.py
    @property
    def health (self) -> float:
        # value between 0 and 1
        # use math.pow (x²) to have health decrease faster when older
        # is 1 when new born and is 0 when max life expectancy is reached
        return 1 - math.pow((self.age / self.life), 2)