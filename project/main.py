from model.model import TownModel

if __name__ == "__main__":
    # Create model with 5 villagers and 3 mobsters
    model = TownModel(5, 3)
    
    while not model.game_over():
        model.step()