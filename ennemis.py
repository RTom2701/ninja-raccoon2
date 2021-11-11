import pygame

class ennemis(pygame.sprite.Sprite,): # pygame.sprite.Sprite -> héritage d'une "super class" pour pouvoir gerer les sprites

    def __init__(self, x, y, image, type):
        super().__init__()
        self.sprite_sheet = pygame.image.load(image)
        self.type = type
        self.image = self.recuperer_sprite(0, 0)
        self.image.set_colorkey([255, 255, 255])
        self.rect = self.image.get_rect()
        self.position = [x, y]
        self.position_initial = (x, y)
        self.all_ennemis = pygame.sprite.Group() # Création d'un nouveau groupe de sprite
        # animation de l'ennemis
        self.animation_skeleton = {
            1 : self.recuperer_sprite(0, 0), # phase 1 
            1.25 : self.recuperer_sprite(0, 0), # phase 1 
            1.5 : self.recuperer_sprite(0, 0), # phase 1
            1.75 : self.recuperer_sprite(0, 0), # phase 1  

            2 : self.recuperer_sprite(24, 0), # phase 2
            2.25 : self.recuperer_sprite(24, 0), # phase 2
            2.5 : self.recuperer_sprite(24, 0), # phase 2
            2.75 : self.recuperer_sprite(24, 0), # phase 2

            3 : self.recuperer_sprite(48, 0), # phase 3
            3.25 : self.recuperer_sprite(48, 0), # phase 3 
            3.5 : self.recuperer_sprite(48, 0), # phase 3
            3.75 : self.recuperer_sprite(48, 0), # phase 3 
            
            4 : self.recuperer_sprite(72, 0), # phase 4
            4.25 : self.recuperer_sprite(72, 0), # phase 4 
            4.5 : self.recuperer_sprite(72, 0), # phase 4
            4.75 : self.recuperer_sprite(72, 0), # phase 4 

            5 : self.recuperer_sprite(96, 0), # phase 5
            5.25 : self.recuperer_sprite(96, 0), # phase 5
            5.5 : self.recuperer_sprite(96, 0), # phase 5
            5.75 : self.recuperer_sprite(96, 0), # phase 5

            6 : self.recuperer_sprite(120, 0), # phase 6
            6.25 : self.recuperer_sprite(120, 0), # phase 6
            6.5 : self.recuperer_sprite(120, 0), # phase 6
            6.75 : self.recuperer_sprite(120, 0), # phase 6

            7 : self.recuperer_sprite(144, 0), # phase 7
            7.25 : self.recuperer_sprite(144, 0), # phase 7
            7.5 : self.recuperer_sprite(144, 0), # phase 7
            7.75 : self.recuperer_sprite(144, 0), # phase 7

            8 : self.recuperer_sprite(168, 0), # phase 8
            8.25 : self.recuperer_sprite(168, 0), # phase 8
            8.5 : self.recuperer_sprite(168, 0), # phase 8
            8.75 : self.recuperer_sprite(168, 0), # phase 8

            9 : self.recuperer_sprite(192, 0), # phase 9
            9.25 : self.recuperer_sprite(192, 0), # phase 9 
            9.5 : self.recuperer_sprite(192, 0), # phase 9
            9.75 : self.recuperer_sprite(192, 0), # phase 9 

            10 : self.recuperer_sprite(216, 0), # phase 10
            10.25 : self.recuperer_sprite(216, 0), # phase 10
            10.5 : self.recuperer_sprite(216, 0), # phase 10
            10.75 : self.recuperer_sprite(216, 0), # phase 10

            11 : self.recuperer_sprite(240, 0), # phase 11
            11.25 : self.recuperer_sprite(240, 0), # phase 11 
            11.5 : self.recuperer_sprite(240, 0), # phase 11
            11.75 : self.recuperer_sprite(240, 0), # phase 11 
        }
        self.animation_flight = {
            1 : self.recuperer_sprite(0, 0), # phase 1 
            1.25 : self.recuperer_sprite(0, 0), # phase 1 
            1.5 : self.recuperer_sprite(0, 0), # phase 1
            1.75 : self.recuperer_sprite(0, 0), # phase 1  

            2 : self.recuperer_sprite(41, 0), # phase 2
            2.25 : self.recuperer_sprite(41, 0), # phase 2
            2.5 : self.recuperer_sprite(41, 0), # phase 2
            2.75 : self.recuperer_sprite(41, 0), # phase 2

            3 : self.recuperer_sprite(82, 0), # phase 3
            3.25 : self.recuperer_sprite(82, 0), # phase 3 
            3.5 : self.recuperer_sprite(82, 0), # phase 3
            3.75 : self.recuperer_sprite(82, 0), # phase 3 
            
            4 : self.recuperer_sprite(123, 0), # phase 4
            4.25 : self.recuperer_sprite(123, 0), # phase 4 
            4.5 : self.recuperer_sprite(123, 0), # phase 4
            4.75 : self.recuperer_sprite(123, 0), # phase 4 

            5 : self.recuperer_sprite(164, 0), # phase 5
            5.25 : self.recuperer_sprite(164, 0), # phase 5
            5.5 : self.recuperer_sprite(164, 0), # phase 5
            5.75 : self.recuperer_sprite(164, 0), # phase 5

            6 : self.recuperer_sprite(205, 0), # phase 6
            6.25 : self.recuperer_sprite(205, 0), # phase 6
            6.5 : self.recuperer_sprite(205, 0), # phase 6
            6.75 : self.recuperer_sprite(205, 0), # phase 6

            7 : self.recuperer_sprite(246, 0), # phase 7
            7.25 : self.recuperer_sprite(246, 0), # phase 7
            7.5 : self.recuperer_sprite(246, 0), # phase 7
            7.75 : self.recuperer_sprite(246, 0), # phase 7

            8 : self.recuperer_sprite(287, 0), # phase 8
            8.25 : self.recuperer_sprite(287, 0), # phase 8
            8.5 : self.recuperer_sprite(287, 0), # phase 8
            8.75 : self.recuperer_sprite(287, 0), # phase 8

        }
        self.etape = [1, 1]
        self.ancienne_position = self.position.copy()
        self.vitesse_y = 3

        # changement animation
    def changer_animation(self,name, type):
        if type == 'skeleton':
            self.image = self.animation_skeleton[name]
            self.image.set_colorkey((255, 255, 255))
        if type == 'flight':
            self.image = self.animation_flight[name]
            self.image.set_colorkey((0, 0, 0))

    # Mise à jour de la position du joueur/animation
    def update(self):
        self.rect.topleft = self.position # Prendre la position
        # Permet d'avoir les différentes étapes de l'animation
        if self.type == 'skeleton':
            self.changer_animation(self.etape[0], 'skeleton')
            if self.etape[0] < 11.75:
                self.etape[0] += 0.25
            else:
                self.etape[0] = 1
        if self.type == 'flight':
            self.changer_animation(self.etape[1], 'flight')
            if self.etape[1] < 8.75:
                self.etape[1] += 0.25
            else:
                self.etape[1] = 1
            if self.position_initial[0]+50 > self.position[0]:
                if self.position_initial[0]-50 < self.position[0]:
                    self.position[0] += -1*self.vitesse_y
                else:
                    self.position[0] += 1*self.vitesse_y
        
    # sauvegarde de la position
    def sauvegarder_pos(self):
        self.ancienne_position = self.position.copy()

    # permet de revenir à l'ancienne position 
    def revenir(self):
        self.position = self.ancienne_position.copy() # revenir à l'ancienne 
        self.rect.topleft = self.position # Prendre la position

    def recuperer_sprite(self, x, y):
        if self.type == 'skeleton':
            image = pygame.Surface([24, 32]) # extraction image
            image.blit(self.sprite_sheet, (0, 0), (x, y, 24, 32)) # extraction d'un morceau de l'image 
            return image
        if self.type == 'flight':
            image = pygame.Surface([41, 32]) # extraction image
            image.blit(self.sprite_sheet, (0, 0), (x, y, 41, 32)) # extraction d'un morceau de l'image 
            return image