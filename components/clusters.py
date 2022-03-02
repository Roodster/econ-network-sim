from audioop import avg
from mimetypes import init
from tokenize import group
import numpy as np

from agents import Agent
import brownian as b
import random
import math



class Cluster:

    TAU = 0.8

    def __init__(self, initial_value: float, group_id: str, brownian_s0: float):
        self.cluster = np.empty(shape=0)
        self.cluster_value = initial_value
        self.group_id = group_id
        self.brownian = b.Brownian().economic_growth(s0=brownian_s0, mu=0.2, sigma=0.6)
        self.iterator = 0

    def __repr__(self):
        return f"Cluster {self.group_id} (size={self.get_cluster_size()}) has a value of {self.cluster_value}"

    def add_agent_to_cluster(self):
        np.append(self.cluster, Agent(group=self.group_id, id=self._get_agent_id()))

    def remove_agent_from_cluster(self, id):

        index = 0
        for i, agent in np.ndenumerate(self.cluster):
            if agent.id == id:
                index = i

        self.cluster = np.delete(self.cluster, index)
        
    def create_cluster(self, size: int):
        if self.get_cluster_size() == 0:
            self.cluster = np.array([Agent(group=self.group_id, id=self._get_agent_id(init_id=x), value=self.cluster_value/size) for x in range(size)])

    def step(self):
        # print(self.brownian)
        self.iterator +=1 
        first, self.brownian = self.brownian[0], self.brownian[1:]
        self.cluster_value = first

    def recalculate_value(self):
        '''
            refactor pls     
        '''
        # print('c size', self.get_cluster_size())
        values = list(np.random.dirichlet(np.ones(self.get_cluster_size()),size=1)[0])
        # print(values)
        for agent in self.cluster:
            agent.set_value(values.pop() * self.cluster_value)

    def get_historical_record(self):
        return self.brownian[0:self.iterator]

    def get_cluster_size(self):
        return len(self.cluster)

    def get_cluster_value(self):
        return self.cluster_value

    def get_historical_average(self):
        return (min(self.get_historical_record()) + max(self.get_historical_record()))/2

    def _get_agent_id(self, init_id: int=None):
        return f'{self.group_id[0]}{self.get_cluster_size() if init_id == None else init_id}'



if __name__ == "__main__":

    group_ids = [
        'YELLOW',
        'RED',
        'BLUE',
        'GREEN',
        'ORANGE',
        'PINK',
        'PURPLE',
    ]

    c = Cluster(initial_value=10, group_id=group_ids.pop(), brownian_s0=10)
    c.create_cluster(size=5)
    print(c.cluster)

    for i in range(0, 100):
        c.step()
        print(c.get_cluster_value())
    print('average: ', c.get_historical_average())

    c.recalculate_value()
