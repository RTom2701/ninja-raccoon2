import pygame

class Projectile(pygame.sprite.Sprite):

    def __init__(self, x, y):
        super().__init__()
        self.sprite_sheet = pygame.image.load("img/shuriken.png")
        self.image = self.recuperer_sprite(0, 0)
        self.image.set_colorkey([0, 0, 0])
        self.rect = self.image.get_rect()
        self.position = [x+10, y+10]
        # animation joueur
        self.animation_piece_or = {
            1 : self.recuperer_sprite(0, 0), # phase 1 
            1.25 : self.recuperer_sprite(0, 0), # phase 1 
            1.5 : self.recuperer_sprite(0, 0), # phase 1 
            1.75 : self.recuperer_sprite(0, 0), # phase 1

            2 : self.recuperer_sprite(0, 0), # phase 1 
            2.25 : self.recuperer_sprite(0, 0), # phase 1 
            2.5 : self.recuperer_sprite(0, 0), # phase 1 
            2.75 : self.recuperer_sprite(0, 0), # phase 1 

            3 : self.recuperer_sprite(16, 0), # phase 2
            3.25 : self.recuperer_sprite(16, 0), # phase 2
            3.5 : self.recuperer_sprite(16, 0), # phase 2
            3.75 : self.recuperer_sprite(16, 0), # phase 2

            4 : self.recuperer_sprite(16, 0), # phase 2
            4.25 : self.recuperer_sprite(16, 0), # phase 2
            4.5 : self.recuperer_sprite(16, 0), # phase 2
            4.75 : self.recuperer_sprite(16, 0), # phase 2
        }
        self.etape = 1
        self.ancienne_position = self.position.copy()

        # changement animation
    def changer_animation(self,name):
        self.image = self.animation_piece_or[name]
        self.image.set_colorkey((0, 0, 0))

    # Mise à jour de la position du joueur
    def update(self):
        self.rect.topleft = self.position # Prendre la position du joueur
        self.changer_animation(self.etape)
        if self.etape < 4.75:
            self.etape += 0.25
        else:
            self.etape = 1
        self.position[0] += 3
        
    # sauvegarde de la position du joueur
    def sauvegarder_pos(self):
        self.ancienne_position = self.position.copy()

    # permet de revenir à l'ancienne position 
    def revenir(self):
        self.position = self.ancienne_position.copy() # revenir à l'ancienne 
        self.rect.center = self.position # Prendre la position du joueur

    def recuperer_sprite(self, x, y):
        image = pygame.Surface([11, 11]) # extraction image
        image.blit(self.sprite_sheet, (0, 0), (x, y, 11, 11)) # extraction d'un morceau de l'image 
        return image