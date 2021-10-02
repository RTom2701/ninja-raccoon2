import pygame

class joueur(pygame.sprite.Sprite): # pygame.sprite.Sprite -> héritage d'une "super class" pour pouvoir gerer les sprites

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
        self.ancienne_position = self.position.copy()
        self.xvitesse = 3
        self.yvitesse = 0
    
    # changement animation
    def changer_animation(self, name):
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

