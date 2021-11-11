import pygame
import game
from menu import Application

# Lancement du jeu quand le fichier py est exécuté
if __name__ == '__main__':
    pygame.init()
    app = Application()
    app.menu()