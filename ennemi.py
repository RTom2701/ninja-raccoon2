import pygame
#non implémenté
class ennemi(pygame.sprite.Sprite):
    def __init__(self, x, y, image, coordonnee_sprite_x, coordonnee_sprite_y):
        super().__init__()

        # Gestion du sprite
        self.sprite_sheet = pygame.image.load(image)
        self.image = self.recuperer_sprite(coordonnee_sprite_x, coordonnee_sprite_y)
        self.image.set_colorkey([0, 0, 0])
        self.rect = self.image.get_rect()

        # Gestion coordonnée
        self.position = [x, y]
        self.ancienne_position = self.position.copy()
        self.vitesse_x = 3
        self.vitesse_y = 0
    
    def recuperer_sprite(self, x, y):
        image = pygame.Surface([32, 32]) # extraction image
        image.blit(self.sprite_sheet, (0, 0), (x, y, 32, 32)) # extraction d'un morceau de l'image 
        return image
    

