from player import joueur
import pygame
import pytmx
import pyscroll 

# Initialisation de pygame
pygame.init()

# class jeu
class Game:
    def __init__(self):
        # créer la fenetre du jeu
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Mon jeu x)")

        # charger la carte
        tmx_data = pytmx.util_pygame.load_pygame('map/carte.tmx') # spécification du fichier de la carte
        map_data = pyscroll.data.TiledMapData(tmx_data) # récupérer les données du tmx
        map_layer = pyscroll.orthographic.BufferedRenderer(map_data, self.screen.get_size()) # récupération des calques (des différents plans de la carte)
        map_layer.zoom = 2 # zoom sur une zone

        # generer un joueur
        position_joueur = tmx_data.get_object_by_name("Player")
        self.player = joueur(position_joueur.x, position_joueur.y)

        # définir une liste qui va stocket les retangles de collisions
        self.walls = []

        for obj in tmx_data.objects: # récupération de tous les objets dans la carte
            if obj.type == 'collision':
                self.walls.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))
                print("je suis la")
                print(self.walls)


        # dessiner le groupe de calques
        self.group = pyscroll.PyscrollGroup(map_layer=map_layer, default_layer = 1) # default_layer = emplacement du joueur au niveau des plans (arriere plan = 0)
        self.group.add(self.player) # ajout du joueur dans la carte

    # récupération des touches enfoncés 
    def recuperation_input(self):
        pressed = pygame.key.get_pressed()

        # Déplacment joueur
        if pressed[pygame.K_LEFT]:
            self.player.changer_animation('gauche')
            self.player.position[0] -= self.player.vitesse
     
        elif pressed[pygame.K_RIGHT]:
            self.player.changer_animation('droite')
            self.player.position[0] += self.player.vitesse

        elif pressed[pygame.K_ESCAPE]:
            pygame.quit()


    def update(self):
        self.group.update()

        # verification collision
        for sprite in self.group.sprites():
            if sprite.rect.collidelist(self.walls) > -1:
                self.player.revenir()


    def run(self):
        # tickrate
        tickrate = pygame.time.Clock()


        # boucle du jeu
        jeu = True

        while jeu == True:
            
            self.player.sauvegarder_pos()
            self.recuperation_input()
            self.update() # mise à jour du joueur
            self.group.center(self.player.rect)
            self.group.draw(self.screen) # affichage de la carte
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    jeu = False
            tickrate.tick(60) # Rafraichissement = 60 IPS

        pygame.quit()


        