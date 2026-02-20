import pygame
from core.engine import Engine


def main():
    pygame.init()
    engine = Engine()
    engine.run()
    pygame.quit()
    
if __name__ == "__main__":
    main()