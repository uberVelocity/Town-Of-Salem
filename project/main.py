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

    # Get current path of script
    path = os.getcwd() + "/results"
    with open(path, 'w') as out:
        winner = [0, 0]

        # Simulate `runs` number of games
        for i in range(runs):
        
            # Create model with 5 villagers and 3 mobsters
            model = TownModel(5, 3, interactions)

            # Run the model until the game is over
            while not model.game_over(winner):
                model.step()

            # Write results to file
            out.write("Villager wins: " + str(winner[0]) + "\n")
            out.write("Mafia wins: " + str(winner[1]) + "\n")
            
            # Print current run
            print("Current run: ", i + 1)

        # Print final number of wins per faction at the end
        print("Villager wins: " + str(winner[0]))
        print("Mafia wins: " + str(winner[1]))