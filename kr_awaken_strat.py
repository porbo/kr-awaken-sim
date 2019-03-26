import numpy as np

class AwakenStrategy:
    """
    strategy is a dict.
    int keys represent
    """
    def __init__(self, strat = {0:[], 1:[], 2:[], 3:[1], 4:[2,1,1]}):
        self.strategy = strat.copy()

    def copy(self):
        return AwakenStrategy(self.strategy)

    def set_one_strat(self, star, strat):
        """
        update just the strategy for the given star level
        params:
            star:int
            strat:list (of stars of fodder to use before spamming 0-star fodders)
        """
        self.strategy[star] = strat

    def simulate(self, goal = 5, n_trials = 5000):
        """
        Creates an np array of costs to reach a goal star level
        params:
            goal:int target star level. Default 5
            n_trials:int number of simulation trials to conduct. Default 5000
        output:
            1D np array of costs
        """
        samples = [Item(self) for _ in range(n_trials)]
        return np.array([s.simulate(goal) for s in samples])


    def compare(self, other, goal = 5, n_trials = 5000):
        print("Strategy:", self.strategy)
        print("Competitor Strategy:", other.strategy)

        counts = self.simulate(goal, n_trials)
        competitor_counts = other.simulate(goal, n_trials)

        print('Wins:', (counts < competitor_counts).sum())
        print('Losses:', (counts > competitor_counts).sum())
        print('Draws:', (counts == competitor_counts).sum())

        return counts, competitor_counts
