from pygame.constants import GL_ACCELERATED_VISUAL
from player import joueur
from ennemi import ennemi
from coin import coin
import pygame
import pytmx
import pyscroll 

# Initialisation de pygame
fichier = 'musique.mp3'
pygame.init()
pygame.mixer.init()
pygame.mixer.music.load(fichier)
pygame.mixer.music.play(-1) # If the loops is -1 then the music will repeat indefinitely.
pygame.mixer.music.set_volume(0.05)

# class jeu
class Game:
    def __init__(self, map, score):
        # créer la fenetre du jeu
        self.dimension = (1920, 1080)
        self.screen = pygame.display.set_mode(self.dimension)
        pygame.display.set_caption("Ninja Raccoon 2")

        # Pour que le jeu se lance
        self.jeu = True

        # charger la carte
        tmx_data = pytmx.util_pygame.load_pygame(map) # spécification du fichier de la carte
        map_data = pyscroll.data.TiledMapData(tmx_data) # récupérer les données du tmx
        map_layer = pyscroll.orthographic.BufferedRenderer(map_data, self.screen.get_size()) # récupération des calques (des différents plans de la carte)
        map_layer.zoom = 2 # zoom sur une zone

        # generer un joueur
        position_joueur = tmx_data.get_object_by_name("Player")
        self.player = joueur(position_joueur.x, position_joueur.y)

        # generation des pieces
        self.list_coin = []
        position_coin = tmx_data.get_object_by_name("piece")
        global coin
        
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
            if obj.name == 'piece':
                self.list_coin.append(coin(obj.x, obj.y, 'img/coin/MonedaD.png', 'piece_or'))
            if obj.name == 'super_piece':
                self.list_coin.append(coin(obj.x, obj.y, 'img/coin/spr_coin_roj.png', 'rubis'))

        # dessiner le groupe de calques
        self.group = pyscroll.PyscrollGroup(map_layer=map_layer, default_layer = 1) # default_layer = emplacement du joueur au niveau des plans (arriere plan = 0)
        self.group.add(self.player) # ajout du joueur dans la carte
        for coin in self.list_coin:
            self.group.add(coin)


        # Score du joueur
        self.score = score
        

    # récupération des touches enfoncés 
    def recuperation_input(self):
        pressed = pygame.key.get_pressed()

        if pressed[pygame.K_ESCAPE]:
            pygame.quit()
        if pressed[pygame.K_a]:
            self.coin.remove()
            print()


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
                if abs(self.plateforme[i].bottom - self.player.rect.top) <= self.player.tolerance: # On soustrait les deux
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
        
        # Vérification collision coin et si il y a une collision on ajout des points
        for coin in self.list_coin:
            if self.player.rect.colliderect(coin):
                if coin.type == 'piece_or':
                    self.score += 10 # ajoute au score des points
                if coin.type == 'rubis':
                    self.score += 100 # ajoute au score des points
                coin.position[1] += 1000 # deplace la piece hors du champs

        for surface in self.bordure_suicide:
            if surface.colliderect(self.player.rect):
                self.jeu = False

    def graviter(self):
        # le joueur tombe continuellement si il peut
        if self.player.graviter:
            self.player.position[1] += self.player.vitesse_y
        # Plus le joueur tombe, plus il ira vite sans depasser 10
        if self.player.vitesse_y < 10 and self.player.graviter:
            if self.player.vitesse_x > 2:
                self.player.vitesse_x -= 0.1
            self.player.vitesse_y += 0.1
        


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
            print(self.score)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    jeu = False

            tickrate.tick(60) # Rafraichissement = 60 IPS

        pygame.quit()
