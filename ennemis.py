import pygame

class ennemis(pygame.sprite.Sprite,): # pygame.sprite.Sprite -> héritage d'une "super class" pour pouvoir gerer les sprites

    def __init__(self, x, y, image, type):
        super().__init__()
        self.sprite_sheet = pygame.image.load(image)
        self.image = self.recuperer_sprite(0, 0)
        self.image.set_colorkey([0, 0, 0])
        self.rect = self.image.get_rect()
        self.position = [x, y]
        self.all_ennemis = pygame.sprite.Group()
        self.type = type
        # animation joueur
        self.animation_ennemis = {
            1 : self.recuperer_sprite(0, 0), # phase 1 
            2 : self.recuperer_sprite(24, 0), # phase 1 
            3 : self.recuperer_sprite(48, 0), # phase 1 
            4 : self.recuperer_sprite(62, 0), # phase 1 

            5 : self.recuperer_sprite(96, 0), # phase 2
            6 : self.recuperer_sprite(120, 0), # phase 2
            7 : self.recuperer_sprite(144, 0), # phase 2
            8 : self.recuperer_sprite(168, 0), # phase 2

            9 : self.recuperer_sprite(192, 0), # phase 3 
            10 : self.recuperer_sprite(216, 0), # phase 3
            11 : self.recuperer_sprite(240, 0), # phase 3 
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
        image = pygame.Surface([24, 32]) # extraction image
        image.blit(self.sprite_sheet, (0, 0), (x, y, 24, 32)) # extraction d'un morceau de l'image 
        return image