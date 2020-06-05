from model.model import TownModel
import sys, os

def is_num(string):
    return string.isnumeric()

def set_runs(num):
    if is_num(num):
        runs = int(sys.argv[1])
        return runs
    else:
        exit("Please insert valid number of runs (1..n)")
    

if __name__ == "__main__":
    interactions = False
    runs = 1

    # Get the number of runs (1 by default)
    if len(sys.argv) == 2:
        runs = set_runs(sys.argv[1])
    # Potentially get interactions argument
    elif len(sys.argv) == 3:
        interactions = True
        runs = set_runs(sys.argv[1])

    path = os.getcwd() + "/results"
    with open(path, 'a') as out:
        winner = None
        # Create model with 5 villagers and 3 mobsters
        for i in range(runs):
            model = TownModel(5, 3, interactions)
            while not model.game_over(winner):
                model.step()
            print(winner)
            print(i)