from game import Game
from pygame.constants import GL_ACCELERATED_VISUAL
from player import joueur
from ennemi import ennemi
from coin import coin
from projectile import Projectile
import pygame
import pytmx
import pyscroll 
 
surfaceW = 800 #Dimension de la fenêtre / Largeur
surfaceH = 600 #Dimension de la fenêtre / Longueur

class Menu :
    """ Création et gestion des boutons d'un menu """
    def __init__(self, action, *groupes) :
        self.couleurs = dict(normal=(0, 200, 0),survol=(0, 200, 200))
        font = pygame.font.SysFont('Helvetica', 24, bold=True)
        # noms des menus et commandes associées
        items = (('NIVEAU 1', action.lancement),('NIVEAU 2', action.lancement2),('QUITTER', action.quitter))
        x = 400
        y = 200
        self.boutons = []
        for texte, cmd in items :
            mb = MenuBouton(
                texte,
                self.couleurs['normal'],
                font,
                x,
                y,
                200,
                50,
                cmd
            )
            self.boutons.append(mb)
            y += 120
            for groupe in groupes :
                groupe.add(mb)
 
    def update(self, events) :
        clicGauche, *_ = pygame.mouse.get_pressed()
        posPointeur = pygame.mouse.get_pos()
        for bouton in self.boutons :
            # Si le pointeur souris est au-dessus d'un bouton
            if bouton.rect.collidepoint(*posPointeur) :
                # Changement de la couleur du bouton
                bouton.dessiner(self.couleurs['survol'])
                # Si le clic gauche a été pressé
                if clicGauche :
                    # Appel de la fonction du bouton
                    bouton.executerCommande()
                break
            else :
                # Le pointeur n'est pas au-dessus du bouton
                bouton.dessiner(self.couleurs['normal'])
        else :
            # Le pointeur n'est pas au-dessus d'un des boutons
            # initialisation au pointeur par défaut
            pygame.mouse.set_cursor(*pygame.cursors.arrow)
 
    def detruire(self) :
        pygame.mouse.set_cursor(*pygame.cursors.arrow) # initialisation du pointeur
 
 
 
class MenuBouton(pygame.sprite.Sprite) :
    """ Création d'un simple bouton rectangulaire """
    def __init__(self, texte, couleur, font, x, y, largeur, hauteur, commande) :
        super().__init__()
        self._commande = commande
 
        self.image = pygame.Surface((largeur, hauteur))
 
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
 
        self.texte = font.render(texte, True, (0, 0, 0))
        self.rectTexte = self.texte.get_rect()
        self.rectTexte.center = (largeur/2, hauteur/2)
 
        self.dessiner(couleur)
 
    def dessiner(self, couleur) :
        self.image.fill(couleur)
        self.image.blit(self.texte, self.rectTexte)
 
    def executerCommande(self) :
        # Appel de la commande du bouton
        self._commande()
 
 
class Application :
   
    """ Classe maîtresse gérant les différentes interfaces du jeu """
    def __init__(self) :
        pygame.init()
 
        self.fond = (150,)*3
 
        self.fenetre = pygame.display.set_mode((surfaceW,surfaceH))
        # Groupe de sprites utilisé pour l'affichage
        self.groupeGlobal = pygame.sprite.Group()
        self.statut = True
        self.jeu=None
 
    def _initialiser(self) :
        try:
            self.ecran.detruire()
            # Suppression de tous les sprites du groupe
            self.groupeGlobal.empty()
        except AttributeError:
            pass
 
    def menu(self) :
        # Affichage du menu
        self._initialiser()
        self.ecran = Menu(self, self.groupeGlobal)
 
    def lancement(self):
        self.jeu=Game('map/1forest.tmx')
        self.jeu.run()

    def lancement2(self):
        self.jeu=Game('map/2temple.tmx')
        self.jeu.run()

    def quitter(self) :
        self.statut = False
 
    def update(self) :
        events = pygame.event.get()
 
        for event in events :
            if event.type == pygame.QUIT :
                self.quitter()
                return
 
        self.fenetre.fill(self.fond)
        self.ecran.update(events)
        self.groupeGlobal.update()
        self.groupeGlobal.draw(self.fenetre)
        pygame.display.update()
 
 
app = Application()
app.menu()
 
clock = pygame.time.Clock()
 
while app.statut :
    app.update()
    clock.tick(30)
 
pygame.quit()