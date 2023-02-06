from mesa import Model, DataCollector
from mesa.time import RandomActivation
from mesa.space import MultiGrid
from agents import Mangrove

class Cyborg(Model):
    height = 40
    width = 40
    mangrove_count = 0
    mangrove_fertility = 0.6
    mangrove_life_expectancy = 5
    mangrove_density = 0.3

    def __init__(
        self, 
        mangrove_fertility, 
        mangrove_life_expectancy,
        mangrove_density
    ) -> None:
        super().__init__()
        # set model framework (grid and schedule)
        self.schedule = RandomActivation(self)
        self.grid = MultiGrid(self.width, self.height, True)

        # set model parameters
        self.mangrove_fertility = mangrove_fertility
        self.mangrove_life_expectancy = mangrove_life_expectancy
        self.mangrove_density = mangrove_density


        # define which data should be collected every step
        self.datacollector = DataCollector(
            model_reporters={
                "Mangroves": "mangrove_count",
                "Mangrove Life Expectancy": "avg_mangrove_life_expectancy",
                "Mangrove Fertility": "avg_mangrove_fertility",
            },
            agent_reporters={}
        )

        for content, x, y in self.grid.coord_iter():
            if self.random.random() < self.mangrove_density:
                mangrove = Mangrove(
                    unique_id=self.next_id(),
                    model=self, 
                    pos=(x,y),
                    life=self.mangrove_life_expectancy, # set life expectancy
                    age=self.random.randint(0, self.mangrove_life_expectancy), # give the mangroves a random age at the start
                    fertility=self.random.gauss(self.mangrove_fertility, 0.1) # give the mangroves a random fertility around the initial value
                )
                self.grid.place_agent(mangrove, (x,y))
                self.schedule.add(mangrove)
                self.mangrove_count += 1
        
        self.datacollector.collect(self)
        self.running = True

    def step(self):
        self.schedule.step()
        self.datacollector.collect(self)

    @property
    def avg_mangrove_fertility(self) -> float:
        # get all the mangroves and their average fertility
        mangroves_fertility = [agent.fertility for agent in self.schedule.agents if isinstance(agent, Mangrove)]
        # return 0 if all mangroves are dead
        if len(mangroves_fertility) == 0: return 0
        else: return sum(mangroves_fertility) / len(mangroves_fertility)

    @property
    def avg_mangrove_life_expectancy(self) -> float:
        # get all the mangroves and their average fertility
        mangroves_life_expectancy = [agent.life for agent in self.schedule.agents if isinstance(agent, Mangrove)]
        # return 0 if all mangroves are dead
        if len(mangroves_life_expectancy) == 0: return 0
        else: return sum(mangroves_life_expectancy) / len(mangroves_life_expectancy)
