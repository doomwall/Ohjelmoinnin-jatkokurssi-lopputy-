# TEE PELI TÄHÄN
import pygame
import random

class Peli: 
    def __init__(self) -> None:
        pygame.init()

        self.lataa_kuvat()
        #self.uusi_peli()

        self.robo = self.kuvat[0]
        self.kolikko = self.kuvat[1]
        self.vihollinen_kuva = self.kuvat[2]
        self.naytto = pygame.display.set_mode((1200, 800))

        self.vasen = False
        self.oikea = False
        self.ylos = False
        self.alas = False
        self.x = 10
        self.y = 350

        self.maali = pygame.Rect(0, 300, 100, 200)

        self.kolikkox = random.randrange(50, 1100)
        self.kolikkoy = random.randrange(50, 700)

        self.vihollinenx = 1400
        self.vihollineny = random.randrange(-100, 1200)

        self.estekoot = [[300, 200, 100, 100], [800, 200, 100, 100], [800, 500, 100, 100], [300, 500, 100, 100],
                         [0, 0, 1200, 50], [0, 750, 1200, 50], [1150, 0, 50, 800], [0, 0, 50, 300], [0, 500, 50, 350]]
        self.esteet = []
        for i in self.estekoot:
            este = pygame.Rect(i[0], i[1], i[2], i[3])
            self.esteet.append(este)

        self.pisteet = 0
        self.kolikko_tila = 0

        self.aika = 0
        self.viholliset = []
        self.viholliset.append([self.vihollinenx, self.vihollineny])

        self.fontti = pygame.font.SysFont("Arial", 24)
        self.gameover_fontti = pygame.font.SysFont("Arial", 60)
        pygame.display.set_caption("Robo-Mania")
        

        self.kello = pygame.time.Clock()

        self.silmukka()


    def lataa_kuvat(self):
        self.kuvat = []
        for nimi in ["robo", "kolikko", "hirvio"]:
            self.kuvat.append(pygame.image.load(nimi + ".png"))

    def liike(self):
        if self.osuma():
            return
        
        self.sijainti = (self.x, self.y)
        if self.vasen and self.tarkista_liike():
            self.x -= 2
        if self.oikea and self.tarkista_liike():
            self.x += 2
        if self.alas and self.tarkista_liike():
            self.y += 2
        if self.ylos and self.tarkista_liike():
            self.y -= 2

        if not self.tarkista_liike():
            self.x, self.y = self.sijainti

    
    def tarkista_liike(self):

        self.robo_rect = pygame.Rect(self.x, self.y, (self.robo.get_width() - 6), (self.robo.get_height() - 2))
        for i in self.esteet:
            if self.robo_rect.colliderect(i):
                self.x -= 1
                return False
            
        return True
    
    def spawnaa_kolikko(self):
        self.onko_maalissa()

        self.kolikot = [1]
        if self.kolikko_tila == 0:
            for i in self.kolikot:
                self.naytto.blit(self.kolikko, (self.kolikkox, self.kolikkoy))
            self.robo_rect = pygame.Rect(self.x, self.y, (self.robo.get_width() - 6), (self.robo.get_height() - 2))
            self.kolikko_rect = pygame.Rect(self.kolikkox, self.kolikkoy, (self.kolikko.get_width()), (self.kolikko.get_height()))
            for i in self.esteet:
                if self.kolikko_rect.colliderect(i):
                        self.kolikkox = random.randrange(150, 1100)
                        self.kolikkoy = random.randrange(50, 700)
            if self.robo_rect.colliderect(self.kolikko_rect):
                self.kolikkox = -100
                self.kolikkoy = -100
                self.kolikko_tila = 1


    def onko_maalissa(self):
        
        self.robo_rect = pygame.Rect(self.x, self.y, (self.robo.get_width() - 6), (self.robo.get_height() - 2))
        self.kolikko_rect = pygame.Rect(self.kolikkox, self.kolikkoy, (self.kolikko.get_width()), (self.kolikko.get_height()))
        if self.robo_rect.colliderect(self.maali) and self.kolikkox == -100 and self.kolikko_tila == 1:
            self.pisteet += 1
            self.kolikkox = random.randrange(150, 1100)
            self.kolikkoy = random.randrange(50, 700)
            self.kolikko_tila = 0
            

    def vihollinen_liike(self):
        for i in self.viholliset:
            if i[0] < self.x:
                i[0] += 1

            if i[1] < self.y:
                i[1] += 1

            if i[0] > self.x:
                i[0] -= 1

            if i[1] > self.y:
                i[1] -= 1

    def spawnaa_vihollinen(self):
        for i in self.viholliset:
            self.naytto.blit(self.vihollinen_kuva, (i[0], i[1]))
        if self.aika > 15 and len(self.viholliset) == 1:
            self.vihollinenx = 1400
            self.vihollineny = random.randrange(-100, 1200)
            self.viholliset.append([self.vihollinenx, self.vihollineny])
        if self.aika > 30 and len(self.viholliset) == 2:
            self.vihollinenx = 1400
            self.vihollineny = random.randrange(-100, 1200)
            self.viholliset.append([self.vihollinenx, self.vihollineny])

            
    def osuma(self):
        self.robo_rect = pygame.Rect(self.x, self.y, (self.robo.get_width() - 6), (self.robo.get_height() - 2))
        for i in self.viholliset:
            self.vihollinen_rect = pygame.Rect(i[0], i[1], (self.vihollinen_kuva.get_width()), (self.vihollinen_kuva.get_height()))
            if self.robo_rect.colliderect(self.vihollinen_rect):
                return True
            
        return False

    def uusi_peli(self):
        self.pisteet = 0
        self.x = 10
        self.y = 350
        self.aika = 0
        self.viholliset = []
        self.viholliset.append([self.vihollinenx, self.vihollineny])


    def silmukka(self):
        while True:
            self.piirra_naytto()
            self.liike()
            self.vihollinen_liike()
            self.tarkista_tapahtumat()

    def piirra_naytto(self):
        self.naytto.fill((230, 230, 230))
        pygame.draw.rect(self.naytto, (0, 255, 255), self.maali)
        self.naytto.blit(self.robo, (self.x, self.y))
        
        teksti = self.fontti.render(f"Pisteet: {self.pisteet}", True, (255, 255, 255))

        for i in self.esteet:
            pygame.draw.rect(self.naytto, (255, 0, 0), i)
        self.spawnaa_kolikko()
        self.naytto.blit(teksti, (1000, 10))
        self.spawnaa_vihollinen()
        self.aika += 0.01
        if self.osuma():
            game_over = self.gameover_fontti.render("GAME OVER", True, (0, 100, 100))
            pistetilanne = self.gameover_fontti.render(f"Pisteet: {self.pisteet}", True, (0, 100, 100))
            aloita_uusi = self.fontti.render("Haluatko kokeilla uudestaan? Paina 1", True, (0, 100, 100))
            lopeta = self.fontti.render("Lopeta: paina ESC", True, (0, 100, 100))
            self.naytto.blit(game_over, (420, 300))
            self.naytto.blit(pistetilanne, (480, 370))
            self.naytto.blit(aloita_uusi, (405, 450))
            self.naytto.blit(lopeta, (495, 480))
        pygame.display.flip()
        self.kello.tick(60)
        

    def tarkista_tapahtumat(self):
        for tapahtuma in pygame.event.get():
            if tapahtuma.type == pygame.KEYDOWN:
                if tapahtuma.key == pygame.K_LEFT:
                    self.vasen = True
            if tapahtuma.type == pygame.KEYDOWN:
                if tapahtuma.key == pygame.K_RIGHT:
                    self.oikea = True
            if tapahtuma.type == pygame.KEYDOWN:
                if tapahtuma.key == pygame.K_UP:
                    self.ylos = True
            if tapahtuma.type == pygame.KEYDOWN:
                if tapahtuma.key == pygame.K_DOWN:
                    self.alas = True
            if tapahtuma.type == pygame.KEYDOWN:
                if tapahtuma.key == pygame.K_1:
                    self.uusi_peli()
            if tapahtuma.type == pygame.KEYDOWN:
                if tapahtuma.key == pygame.K_ESCAPE:
                    quit()

            if tapahtuma.type == pygame.KEYUP:
                if tapahtuma.key == pygame.K_LEFT:
                    self.vasen = False
            if tapahtuma.type == pygame.KEYUP:
                if tapahtuma.key == pygame.K_RIGHT:
                    self.oikea = False
            if tapahtuma.type == pygame.KEYUP:
                if tapahtuma.key == pygame.K_UP:
                    self.ylos = False
            if tapahtuma.type == pygame.KEYUP:
                if tapahtuma.key == pygame.K_DOWN:
                    self.alas = False

            if tapahtuma.type == pygame.QUIT:
                exit()



if __name__ == "__main__":
    Peli()