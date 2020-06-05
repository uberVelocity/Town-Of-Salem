from model.model import TownModel
import sys

if __name__ == "__main__":
    interactions = False

    # Potentially get interactions argument
    if len(sys.argv) > 1:
        interactions = True

    # Create model with 5 villagers and 3 mobsters
    model = TownModel(5, 3, interactions)
    while not model.game_over():
        model.step()
