import random


class BaseAgent:

    def __init__(self, group: str, id:str, value:float):

        self.id = id
        self.group = group

        if value != None:
            self.value = value

    def __repr__(self):
        return f"Agent {self.id} from group {self.group} has a value of {self.value}.\n"

    def set_value(self, value):
        self.value = value

    def does_defect(self):
        
        prob = random.random() + self.defection_score

        if prob < self.lower_bound:
            return True

        return False
        

        

class Agent(BaseAgent):
    pass