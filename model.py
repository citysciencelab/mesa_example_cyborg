from mesa import Model, DataCollector
from mesa.time import RandomActivation
from mesa.space import MultiGrid
from agents import Mangrove

# the class for the model that holds the entire simulation
# inherits all the standard properties from mesa.Model
class Cyborg(Model):
    # define all the properties of the class here
    # they can be either initialized with a value (height = 40)
    # or simply declared without value giving only their data type (height: int)
    # native data types => https://www.w3schools.com/python/python_datatypes.asp
    # a data type can also be something that you defined yourself, like a class (agent_class: Mangrove)
    height = 40
    width = 40
    mangrove_count = 0
    mangrove_fertility: float
    mangrove_density: float
    mangrove_life_expectancy: int

    # constructor for a new instance (run) of that model
    # all the params between the parathesis (except "self") can be passed when initialzing a new instance of a class
    # e.g. my_new_cyborg = Cyborg(mangrove_fertility=0.5, mangrove_life_expectancy=5)
    # default values can (but don't have to) be set, those don't have to be provided when calling the constructor
    # if a constructor is called without a parameter that has no default value, it will be "None"
    def __init__(
        self, 
        mangrove_fertility=0.6, 
        mangrove_life_expectancy=5,
        mangrove_density=0.3
    ) -> None:
        # call the __init__ function of the original mesa.Model class
        # add your custom code below
        # sometimes it might be necessary to run your custom code before
        # depends on the code
        super().__init__()
        # set model framework (grid and schedule)
        self.schedule = RandomActivation(self)
        self.grid = MultiGrid(self.width, self.height, True)

        # set model properties
        # all model properties that are not initialized with value as shown above need to be set in the init function
        # the left hand of the assignment is the property to be set
        # the right hand is the value assigned, it can be a variable (like here, coming from the parameters of the constructor)
        self.mangrove_fertility = mangrove_fertility
        self.mangrove_life_expectancy = mangrove_life_expectancy
        self.mangrove_density = mangrove_density


        # define which data should be collected every step
        # see https://mesa.readthedocs.io/en/stable/apis/datacollection.html#datacollection.DataCollector
        # model_reporters report a property of the model (Cyborg)
        self.datacollector = DataCollector(
            model_reporters={
                "Mangroves": "mangrove_count",
                "Avg. Mangrove Life Expectancy": "avg_mangrove_life_expectancy",
                "Avg. Mangrove Fertility": "avg_mangrove_fertility",
            }
        )

        # initialize a first population of mangroves
        # by calling the function defined below
        # 'ctrl' + click on the function name brings you to where it has been defined
        # if you want to use a function like that you have to declare it first
        # a function ("def") can either be part of a class like here
        # or it can be defined outside (as "stateless")
        # but it can't access other properties of "self" then
        self.init_mangroves()
        
        # start the simulation and collect the initial state of the model
        self.datacollector.collect(self)
        self.running = True

    # the function that runs every step of the simulation on the model
    # it does nothing but collect the current state and trigger the "step" function on all agents
    def step(self):
        self.schedule.step()
        self.datacollector.collect(self)

        # stop the simulation if all mangroves are dead
        if self.mangrove_count == 0:
            self.running = False

    # the function to initialize the first population of mangroves
    # it is called above in __init__
    # a function without a return can be called but doesn't yield any value as a result
    # it returns "None"
    def init_mangroves(self):
        # iterate over all cells of the grid
        # self.grid.coord_iter() returns a tuple with 3 values: (cell_content, x_pos, y_pos)
        # you see the return of a function by hovering over its name with the cursor
        # 
        for content, x, y in self.grid.coord_iter():
            # if random number between 0 and 1 is smaller than mangrove_density (e.g. 0.3) -> 30% chance
            if self.random.random() < self.mangrove_density:
                # initialize the new mangrove with the necessary params
                # casing is important "mangrove" is the new mangrove, "Mangrove" is the class definition for all mangroves
                mangrove = Mangrove(
                    unique_id=self.next_id(), # new unique id by just counting up
                    model=self, # link this model to the new mangrove
                    pos=(x,y), # pass the coords where the mangrove should be
                    life=self.mangrove_life_expectancy, # set life expectancy
                    age=self.random.randint(0, self.mangrove_life_expectancy), # give the mangroves a random age at the start
                    fertility=self.random.gauss(self.mangrove_fertility, 0.1) # give the mangroves a random fertility around the initial value
                )
                # add the mangrove to the model and the grid (by coordinate)
                self.grid.place_agent(mangrove, (x,y))
                self.schedule.add(mangrove)

                # update the mangrove count by adding 1
                self.mangrove_count += 1

    # properties of a class can also defined as a function by adding "@property" to a "def"
    # that means whenever you want to access "self.avg_mangrove_fertility" you can do it without calling it as a function by adding "()"
    # it will then compute the current value of the property by running the code below
    # tell the user and your fellow coders what data type will be the result of the function by adding "-> <DataType>"
    @property
    def avg_mangrove_fertility(self) -> float:
        # get all the mangroves and their average fertility
        mangroves_fertility = [agent.fertility for agent in self.schedule.agents if isinstance(agent, Mangrove)]
        # return 0 if all mangroves are dead
        if self.mangrove_count == 0: return 0
        else: return sum(mangroves_fertility) / self.mangrove_count

    @property
    def avg_mangrove_life_expectancy(self) -> float:
        # get all the mangroves and their average fertility
        mangroves_life_expectancy = [agent.life for agent in self.schedule.agents if isinstance(agent, Mangrove)]
        # return 0 if all mangroves are dead
        if self.mangrove_count == 0: return 0
        else: return sum(mangroves_life_expectancy) / self.mangrove_count
