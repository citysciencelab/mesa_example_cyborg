from mesa import Agent
import math

class Mangrove(Agent):
    life: int # maximal life expectancy
    age: int # steps lived
    fertility: float # likelihood of reproduction

    def __init__(self, unique_id, model, pos, life=5, age=0, fertility=0.6):
        super().__init__(unique_id, model)
        self.pos = pos

        # max. life expectancy based on gauss normal distribution
        # so life = 5 leads to a value somewhere around 5
        self.life = self.random.gauss(life, 1)
        # set initial age (not all mangroves are new born at the start)
        self.age = age
        self.fertility = abs(fertility) # make sure it's positive

    def step(self):
        self.age += 1

        rand = self.random.random() # random number between 0 and 1
        # if random number is bigger than health, the mangrove dies
        if rand > self.health: # 
            self.model.grid.remove_agent(self)
            self.model.schedule.remove(self)
            self.model.mangrove_count -= 1
        else:
            # chance of reproduction
            if self.random.random() < self.fertility:
                empty_cells = []
                neighbor_cells = self.model.grid.iter_neighborhood(self.pos, True)

                # that got a bit complicated
                # we have to look through all the neighboring cells
                # to check if there is already a mangrove growing there
                # can be used for other agents like trash too
                # if the cell has no mangroves, we add it to the list of empty cells
                for cell in neighbor_cells:
                    cell_content = self.model.grid.get_cell_list_contents([cell])
                    mangroves_in_cell = [agent for agent in cell_content if isinstance(agent, Mangrove)]
                    if len(mangroves_in_cell) == 0:
                        empty_cells.append(cell)

                # if there is any empty cell,
                # pick a random empty cell
                if (len(empty_cells) > 0):
                    new_pos = self.random.choice(empty_cells)
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

    @property
    def health (self) -> float:
        # value between 0 and 1
        # use math.pow (x²) to have health decrease faster when older
        # is 1 when new born and is 0 when max life expectancy is reached
        return 1 - math.pow((self.age / self.life), 2)