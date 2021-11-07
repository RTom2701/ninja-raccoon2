from pygame.constants import GL_ACCELERATED_VISUAL
from player import joueur
from ennemi import ennemi
from coin import coin
import pygame
import pytmx
import pyscroll 


#Sélection du niveau(dans la console)

niveau = int(input("Niveau 1 ou 2?"))
if niveau == 2:
    niveau = 'map/2temple.tmx'
else: #Sélectionne le niveau 1 même si la réponse est incorrecte car c'est le niveau par défaut
    niveau =  'map/1forest.tmx' 

# Initialisation de pygame
pygame.init()
pygame.mixer.init() #initialiste la méthode de son de pygame
pygame.mixer.music.load('musique.mp3') #charge la musique
pygame.mixer.music.play(-1) # Répète la musique indéfiniment
pygame.mixer.music.set_volume(0.05) # Règle le volume

# class jeu
class Game:
    def __init__(self):
        # créer la fenetre du jeu
        self.dimension = (800, 600)
        self.screen = pygame.display.set_mode(self.dimension)
        pygame.display.set_caption("Ninja Raccoon 2")

        # Pour que le jeu se lance
        self.jeu = True
        

        # charger la carte
        tmx_data = pytmx.util_pygame.load_pygame(niveau) # spécification du fichier de la carte
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
        self.score = 0
        
        #Timer de la partie
        self.timer = 0
        self.compteur_timer = 0 #Sert à compter les 60 frames que compose une seconde

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
                    self.player.saut_disponible = True # le joueur touche le sol, il est donc possible de sauter à nouveau
                    self.player.saut_bloque = False
                    self.player.puissance_saut = 35 #règle la puissance du saut et réinitialise la variable
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
        

        for coin in self.list_coin:
            if self.player.rect.colliderect(coin):
                if coin.type == 'piece_or':
                    self.score += 10
                if coin.type == 'rubis':
                    self.score += 100
                coin.position[1] += 1000

        for surface in self.bordure_suicide:
            if surface.colliderect(self.player.rect):
                self.jeu = False

    def graviter(self):
        if self.player.graviter:
            self.player.position[1] += self.player.vitesse_y
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
            self.compteur_timer+=1
            
            #Affiche du timer et du score dans la console à chaque seconde
            if self.compteur_timer == 60: #Cela signifie qu'une seconde est passée car 60 frames du jeu sont passées
                self.compteur_timer = 0 #remise à zéro du compteur de secondes
                self.timer+=1
                print(f"Score:{self.score}    Timer:{self.timer}")
                

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    jeu = False

            tickrate.tick(60) # Rafraichissement = 60 IPS

        pygame.quit()
