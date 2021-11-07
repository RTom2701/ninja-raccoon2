import pygame

class coin(pygame.sprite.Sprite): # pygame.sprite.Sprite -> héritage d'une "super class" pour pouvoir gerer les sprites

    def __init__(self, x, y, image, type):
        super().__init__()
        self.sprite_sheet = pygame.image.load(image)
        self.image = self.recuperer_sprite(0, 0)
        self.image.set_colorkey([0, 0, 0])
        self.rect = self.image.get_rect()
        self.position = [x, y]
        self.all_coin = pygame.sprite.Group()
        self.type = type
        # animation joueur
        self.animation_piece_or = {
            1 : self.recuperer_sprite(0, 0), # phase 1 
            1.25 : self.recuperer_sprite(0, 0), # phase 1 
            1.5 : self.recuperer_sprite(0, 0), # phase 1 
            1.75 : self.recuperer_sprite(0, 0), # phase 1 

            2 : self.recuperer_sprite(16, 0), # phase 2
            2.25 : self.recuperer_sprite(16, 0), # phase 2
            2.5 : self.recuperer_sprite(16, 0), # phase 2
            2.75 : self.recuperer_sprite(16, 0), # phase 2

            3 : self.recuperer_sprite(32, 0), # phase 3 
            3.25 : self.recuperer_sprite(32, 0), # phase 3
            3.5 : self.recuperer_sprite(32, 0), # phase 3 
            3.75 : self.recuperer_sprite(32, 0), # phase 3 

            4 : self.recuperer_sprite(48, 0), # phase 4
            4.25 : self.recuperer_sprite(48, 0), # phase 4
            4.5 : self.recuperer_sprite(48, 0), # phase 4
            4.75 : self.recuperer_sprite(48, 0), # phase 4
            
            5 : self.recuperer_sprite(64,0), # phase 5 
            5.25 : self.recuperer_sprite(64,0), # phase 5
            5.5 : self.recuperer_sprite(64,0), # phase 5
            5.75 : self.recuperer_sprite(64,0) # phase 5

        }
        self.animation_rubis = {
            1 : self.recuperer_sprite(0, 0), # phase 1 
            1.25 : self.recuperer_sprite(0, 0), # phase 1 
            1.5 : self.recuperer_sprite(0, 0), # phase 1 
            1.75 : self.recuperer_sprite(0, 0), # phase 1 

            2 : self.recuperer_sprite(16, 0), # phase 2
            2.25 : self.recuperer_sprite(16, 0), # phase 2
            2.5 : self.recuperer_sprite(16, 0), # phase 2
            2.75 : self.recuperer_sprite(16, 0), # phase 2

            3 : self.recuperer_sprite(32, 0), # phase 3 
            3.25 : self.recuperer_sprite(32, 0), # phase 3
            3.5 : self.recuperer_sprite(32, 0), # phase 3 
            3.75 : self.recuperer_sprite(32, 0), # phase 3 

            4 : self.recuperer_sprite(48, 0), # phase 4
            4.25 : self.recuperer_sprite(48, 0), # phase 4
            4.5 : self.recuperer_sprite(48, 0), # phase 4
            4.75 : self.recuperer_sprite(48, 0), # phase 4

        }
        self.etape = [1, 1]
        self.ancienne_position = self.position.copy()

        # changement animation
    def changer_animation(self,name, type):
        if type == 'piece_or':
            self.image = self.animation_piece_or[name]
        if type == 'rubis':
            self.image = self.animation_rubis[name]

        self.image.set_colorkey((0, 0, 0))

    # Mise à jour de la position du joueur
    def update(self):
        self.rect.topleft = self.position # Prendre la position du joueur
        # Permet un changement fluide de l'animation
        if self.type == 'piece_or':
            self.changer_animation(self.etape[0], 'piece_or')
            if self.etape[0] < 5.75:
                self.etape[0] += 0.25
            else:
                self.etape[0] = 1
        if self.type == 'rubis':
            self.changer_animation(self.etape[1], 'rubis')
            if self.etape[1] < 4.75:
                self.etape[1] += 0.25
            else:
                self.etape[1] = 1
        
    # sauvegarde de la position du joueur
    def sauvegarder_pos(self):
        self.ancienne_position = self.position.copy()

    # permet de revenir à l'ancienne position 
    def revenir(self):
        self.position = self.ancienne_position.copy() # revenir à l'ancienne 
        self.rect.topleft = self.position # Prendre la position du joueur

    def recuperer_sprite(self, x, y):
        image = pygame.Surface([16, 16]) # extraction image
        image.blit(self.sprite_sheet, (0, 0), (x, y, 16, 16)) # extraction d'un morceau de l'image 
        return image