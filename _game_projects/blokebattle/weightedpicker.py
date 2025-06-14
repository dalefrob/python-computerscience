import random

class WeightedPicker():
    def __init__(self):
        self.items = [("item", 5), ("item2", 3)] # list of tuples
    

    def get_max_weight(self):
        max_weight = sum(weight for item, weight in self.items)
        return max_weight  # Don't forget to return it


    def get_item(self):
        total_weight = self.get_max_weight()
        rand = random.uniform(0, total_weight)
        cumulative_weight = 0

        for item, weight in self.items:
            cumulative_weight += weight
            if rand < cumulative_weight:
                return item


"""
A function to get weighted random items easily.
"""
def get_weighted_random(list_of_tuples):
    total_weight = sum(weight for item, weight in list_of_tuples)
    rand = random.uniform(0, total_weight)
    cumulative_weight = 0

    for item, weight in list_of_tuples:
        cumulative_weight += weight
        if rand < cumulative_weight:
            return item