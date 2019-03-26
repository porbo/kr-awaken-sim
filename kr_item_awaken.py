import random
import numpy as np
from kr_awaken_strat import AwakenStrategy

class Item:
    """
    represents a Kings Raid item that we're trying to awaken.
    constructor:
        Item(strategy = {0:[], 1:[], 2:[], 3:[1], 4:[2,1,1]})
            Constructs the item with a given strategy.
            Strategy is a dictionary with int keys (representing star level) and list values (representing stars of fodder)
                Ex: default, {0:[], 1:[], 2:[], 3:[1], 4:[2,1,1]} means that for a 3 star item, we use a one star fodder before spamming zero star fodder

    methods:
        set_one_strat(star, strat)
        awaken(fodder)
        sim_one()
        simulate(goal)

    attributes:
        bonus: current total bonus to success rate, as a result of failing awakenings
        star: current star level
        chances: stores chance to succeed an awakening
        strategy: strategy to use for awakening
        cost: number of items in the current item (1 + fodders used on it)
    """
    def __init__(self, strategy = AwakenStrategy()):
        """
        params:
            strategy:dict
            strategy is a dictionary with int keys (representing star level) and list values (representing stars of fodder)
                Ex: default, {0:[], 1:[], 2:[], 3:[1], 4:[2,1,1]} means that for a 3 star item, we use a one star fodder before spamming zero star fodder
        """
        self.bonus = 0.0
        self.star = 0
        self.chances = {0:(1,0), 1:(.5,.16), 2:(.25,.08), 3:(.1, .03), 4:(.01, 0)}
        self.strategy = strategy
        self.cost = 1
        self.fodders_used = []

    def reset(self):
        """
        undoes simulations and returns to the start
        no params, no output
        """
        self.bonus = 0.0
        self.star = 0
        self.chances = {0:(1,0), 1:(.5,.16), 2:(.25,.08), 3:(.1, .03), 4:(.01, 0)}
        self.strategy = AwakenStrategy()
        self.cost = 1
        self.fodders_used = []

    def set_one_strat(self, star, strat):
        """
        update just the strategy for the given star level
        params:
            star:int
            strat:list (of stars of fodder to use before spamming 0-star fodders)
        """
        self.strategy.set_one_strat(star,strat)

    def create_fodder(self, f_goal):
        """
        create and return an Item object at the given star level
        params:
            f_goal:int the desired star level of the fodder Item
        return:
            Item: fodder object
        """
        fodder = Item(self.strategy)
        fodder.simulate(f_goal)
        return fodder

    def awaken(self, f_star):
        """
        attempt to awaken
        params:
            f_star: star level of the fodder object
        return:
            bool: whether or not the awakening succeeded
        """
        r = random.random()
        self.fodders_used.append(f_star)
        chance, fail_bonus = self.chances[max(self.star - f_star,0)]
        if r <= chance + self.bonus:
            self.star += 1
            self.bonus = 0.0
            return True
        else:
            self.bonus += fail_bonus
            return False

    def _sim_one(self):
        """
        attempt to awaken until the item's star level rises once.
        """
        current_strat = self.strategy.strategy[self.star]
        #create the fodder items

        i = 0
        complete = False
        while not complete:
            f_star = current_strat[i] if i < len(current_strat) else 0
            f_cost = self.create_fodder(f_star).cost

            complete = self.awaken(f_star)
            self.cost += f_cost
            i += 1

    def simulate(self, goal):
        """
        awaken to a desired star level, returning the cost
        params:
            goal:int desired star level
        output:
            int: total items used to get to that level
        """
        while self.star < goal:
            self._sim_one()

        return self.cost
