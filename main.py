import pygame
from core.engine import Engine


def main():
    pygame.init()
    pygame.display.set_caption("Fuego")
    engine = Engine()
    engine.run()
    pygame.quit()
    
if __name__ == "__main__":
    main()