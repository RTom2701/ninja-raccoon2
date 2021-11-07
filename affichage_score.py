import pygame

class affichage_score(pygame.sprite.Sprite): # pygame.sprite.Sprite -> héritage d'une "super class" pour pouvoir gerer les sprites

    def __init__(self, x, y):
        super().__init__()
        self.sprite_sheet = pygame.image.load('img/player.png')
        self.image = self.recuperer_sprite(0, 0)
        self.image.set_colorkey([0, 0, 0])
        self.rect = self.image.get_rect()
        self.position = [x, y]
        # animation joueur
        self.images = {
            'gauche': self.recuperer_sprite(0, 32), # face droite 
            'droite': self.recuperer_sprite(0, 64) # face gauche

        }
        self.ancienne_position = self.position.copy() # récupération de la position du joueur
        self.vitesse_x = 3 # Ne doit pas depasser 10
        self.vitesse_y = 0 # Ne doit pas depasser 10
        self.deplacement_disponible = [True, True, True, True] # Gauche, Droite, Haut, Bas
        self.tolerance = 10 # tolerance pour la collision
        self.saut_disponible = True # savoir si le saut est possible
        self.graviter = True # graviter dispobible ou non
        self.saut_bloque = False
        self.puissance_saut = 0 
    
    # changement animation
    def changer_animation(self, name):
        # On charge une "nouvelle" image
        self.image = self.images[name]
        self.image.set_colorkey((0, 0, 0))

    # Mise à jour de la position du joueur
    def update(self):
        self.rect.topleft = self.position # Prendre la position du joueur

    # sauvegarde de la position du joueur
    def sauvegarder_pos(self):
        self.ancienne_position = self.position.copy()

    # permet de revenir à l'ancienne position 
    def revenir(self):
        self.position = self.ancienne_position.copy() # revenir à l'ancienne 
        self.rect.topleft = self.position # Prendre la position du joueur

    def recuperer_sprite(self, x, y):
        image = pygame.Surface([32, 32]) # extraction image
        image.blit(self.sprite_sheet, (0, 0), (x, y, 32, 32)) # extraction d'un morceau de l'image 
        return image
    
    def deplacer(self):
        pressed = pygame.key.get_pressed() # recuperation des inputs

        # Déplacment joueur
        if pressed[pygame.K_LEFT] and self.deplacement_disponible[0]:
            self.changer_animation('gauche') # changement d'animation
            self.position[0] -= self.vitesse_x # déplacement du joueur
            # accélération du joueur
            if self.vitesse_x < 5:
                self.vitesse_x += 0.05


        if pressed[pygame.K_RIGHT] and self.deplacement_disponible[1]:
            self.changer_animation('droite') # changement d'animation
            self.position[0] += self.vitesse_x # déplacement du joueur

            # accélération du joueur
            if self.vitesse_x < 5:
                self.vitesse_x += 0.05

        # quand le joueur n'appuie plus sur la touche la vitesse reviens à la normale
        if not pressed[pygame.K_RIGHT] and not pressed[pygame.K_LEFT]:
            self.vitesse_x = 3
        
        if not pressed[pygame.K_UP]:
            self.puissance_saut = 0
        
        if pressed[pygame.K_UP] and  self.puissance_saut > 0:
            if self.saut_bloque: #si un mur est présent au dessus (= saut bloqué) le saut s'annule directement
                self.puissance_saut = 0
            self.vitesse_y = -1*(self.puissance_saut/12) #réglage du saut en fonction d'un diviseur
            self.puissance_saut -= 1 #la puissance du saut diminue à chaque itération
            self.position[1] += self.vitesse_y #actualise la position en fonction de la vitesse
            self.saut_disponible = False #le saut est effectué, il est impossible de sauter à nouveau sans toucher le sol
            if self.vitesse_x > 3: #la vitesse diminue jusqu'à un minimum une fois en l'air pour éviter de sauter trop loin
                self.vitesse_x -= 1
        if pressed[pygame.K_UP] and  self.puissance_saut <= 0: #évite un blocage où il n'est plus possible de sauter
            self.saut_disponible == True
            


