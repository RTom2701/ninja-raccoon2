from pygame.constants import GL_ACCELERATED_VISUAL
from player import joueur
from ennemi import ennemi
import pygame
import pytmx
import pyscroll 

# Initialisation de pygame
pygame.init()

# class jeu
class Game:
    def __init__(self):
        # créer la fenetre du jeu
        self.dimension = (800, 600)
        self.screen = pygame.display.set_mode(self.dimension)
        pygame.display.set_caption("Mon jeu x)")

        # Pour que le jeu se lance
        self.jeu = True

        # charger la carte
        tmx_data = pytmx.util_pygame.load_pygame('map/carte2.tmx') # spécification du fichier de la carte
        map_data = pyscroll.data.TiledMapData(tmx_data) # récupérer les données du tmx
        map_layer = pyscroll.orthographic.BufferedRenderer(map_data, self.screen.get_size()) # récupération des calques (des différents plans de la carte)
        map_layer.zoom = 2 # zoom sur une zone

        # generer un joueur
        position_joueur = tmx_data.get_object_by_name("Player")
        self.player = joueur(position_joueur.x, position_joueur.y)

        # generer un ennemi
        position_ennemi_test = tmx_data.get_object_by_name("ennemi")
        self.ennemi = ennemi(position_ennemi_test.x, position_ennemi_test.y, "img/projectiles.png", 13, 13)

        # définir une liste qui va stocket les retangles de collisions
        self.walls = []
        self.plateforme = []
        self.bordure_carte = []
        self.bordure_suicide = []

        for obj in tmx_data.objects: # récupération de tous les objets dans la carte
            if obj.type == 'collision':
                self.walls.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))
            if obj.type == 'plateforme':
                self.plateforme.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))
            if obj.type == 'bordure':
                self.bordure_carte.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))
            if obj.type == 'suicide':
                self.bordure_suicide.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))

        # dessiner le groupe de calques
        self.group = pyscroll.PyscrollGroup(map_layer=map_layer, default_layer = 1) # default_layer = emplacement du joueur au niveau des plans (arriere plan = 0)
        self.group.add(self.player) # ajout du joueur dans la carte
        

    # récupération des touches enfoncés 
    def recuperation_input(self):
        pressed = pygame.key.get_pressed()

        if pressed[pygame.K_ESCAPE]:
            pygame.quit()


    def update(self):
        self.group.update()
        
        # verification collision
        '''for sprite in self.group.sprites():
            if sprite.rect.collidelist(self.walls) > -1:
                self.player.saut_disponible = True               
                self.player.revenir()'''

        # collision bordure
        if self.player.rect.right >= self.bordure_carte[0].width: # côté droit
            self.player.deplacement_disponible[1] = False
        else:
            self.player.deplacement_disponible[1] = True

        if self.player.rect.left <= 0: # côte gauche
            self.player.deplacement_disponible[0] = False
        else:
            self.player.deplacement_disponible[0] = True

        if self.player.rect.bottom >=  self.bordure_carte[0].height: # bas
            self.player.deplacement_disponible[3] = False
        else:
            self.player.deplacement_disponible[3] = True

        if self.player.rect.top <= 0: # haut
            self.player.deplacement_disponible[2] = False
        else:
            self.player.deplacement_disponible[2] = True

        for i in range(len(self.plateforme)):
            if self.plateforme[i].colliderect(self.player.rect):

                # collision entre le haut de la plateforme et le bas du joueur
                if abs(self.plateforme[i].top - self.player.rect.bottom) <= self.player.tolerance:
                    self.player.deplacement_disponible[3] = False
                    self.player.graviter = False # empeche la gravité
                    self.player.saut_disponible = True
                    self.player.saut_bloque = False
                    self.player.puissance_saut = 40
                else:
                    self.player.deplacement_disponible[3] = True

                # collision entre le bas de la plateforme et le haut du joueur
                if abs(self.plateforme[i].bottom - self.player.rect.top) <= self.player.tolerance:
                    self.player.deplacement_disponible[2] = False
                    self.player.saut_bloque = True
                else:
                    self.player.deplacement_disponible[2] = True

                # collision entre le cote droit de la plateforme et le cote gauche du joueur
                if abs(self.plateforme[i].right - self.player.rect.left) <= self.player.tolerance:
                    self.player.deplacement_disponible[0] = False
                else:
                    self.player.deplacement_disponible[0] = True

                # collision entre le cote gauche de la plateforme et le cote droit du joueur
                if abs(self.plateforme[i].left - self.player.rect.right) <= self.player.tolerance:
                    self.player.deplacement_disponible[1] = False
                else:
                    self.player.deplacement_disponible[1] = True
            else:
                if self.player.deplacement_disponible[3] == True and self.player.chute_disponible:
                    self.player.graviter = True
                    self.player.saut_disponible = False
        self.graviter()

        for surface in self.bordure_suicide:
            if surface.colliderect(self.player.rect):
                self.jeu = False

    def graviter(self):
        if self.player.graviter:
            self.player.position[1] += self.player.vitesse_y
        if self.player.vitesse_y < 10 and self.player.graviter:
            if self.player.vitesse_x > 2:
                self.player.vitesse_x -= 0.1
            self.player.vitesse_y += 0.15
        


    def run(self):
        # tickrate
        tickrate = pygame.time.Clock()


        # boucle du jeu
        while self.jeu == True:
            '''print(self.player.chute_disponible, self.player.graviter)'''
            '''print(self.player.deplacement_disponible)'''
            self.player.sauvegarder_pos()
            self.recuperation_input()
            self.player.deplacer()
            self.update() # mise à jour du joueur
            self.group.center(self.player.rect)
            self.group.draw(self.screen) # affichage de la carte
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    jeu = False
            tickrate.tick(60) # Rafraichissement = 60 IPS

        pygame.quit()