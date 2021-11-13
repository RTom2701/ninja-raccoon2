import pygame

class checkpoint(pygame.sprite.Sprite): # pygame.sprite.Sprite -> héritage d'une "super class" pour pouvoir gerer les sprites

    def __init__(self, x, y, image, type):
        super().__init__()
        self.sprite_sheet = pygame.image.load(image)
        self.type = type
        self.image = self.recuperer_sprite(0, 0)
        self.image.set_colorkey([0, 0, 0])
        self.rect = self.image.get_rect()
        self.position = [x, y]
        self.position_initial = (x, y)
        self.checkpoint = pygame.sprite.Group() # Création d'un nouveau groupe de sprite
        # animation de l'ennemis
        self.checkpoint = {
            1 : self.recuperer_sprite(0, 0), # phase 1 
            2 : self.recuperer_sprite(24, 0)
        }
        self.etape = [1]
        self.ancienne_position = self.position.copy()
        self.vitesse_y = 1

    def changer_animation(self,name):
        self.image = self.checkpoint[name]
        self.image.set_colorkey((0, 0, 0))

    def update(self):
        self.rect.topleft = self.position # Prendre la position
        self.changer_animation(self.etape[0])
        print(self.etape)



    # sauvegarde de la position
    def sauvegarder_pos(self):
        self.ancienne_position = self.position.copy()

    # permet de revenir à l'ancienne position 
    def revenir(self):
        self.position = self.ancienne_position.copy() # revenir à l'ancienne 
        self.rect.topleft = self.position # Prendre la position

    # Permet le découpage de l'image 
    def recuperer_sprite(self, x, y):
        image = pygame.Surface([24, 24]) # extraction image
        image.blit(self.sprite_sheet, (0, 0), (x, y, 24, 24)) # extraction d'un morceau de l'image 
        return image