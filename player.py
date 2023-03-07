import pygame as pg, sys
from os import walk

class Jogador(pg.sprite.Sprite):
    def __init__(self, pos, groups, colisao_sprites):
        super().__init__(groups)
        self.importar_imagens()
        self.frame_index = 0
        self.status = "down"
        # self.image = self.animation[self.frame_index]
        self.image = self.animations[self.status][self.frame_index]
        self.rect = self.image.get_rect(center = pos)
        

    # float movement
        self.pos = pg.math.Vector2(self.rect.center)
        self.direction = pg.math.Vector2()
        self.speed = 200
    
    # colisão
        self.colisao_sprites = colisao_sprites
        self.hitbox = self.rect.inflate(0, -self.rect.height/2)
    
    def colisao(self, direction):
        if direction == "horizontal":
               for sprite in self.colisao_sprites.sprites():
                    if sprite.hitbox.colliderect(self.hitbox):
                        if hasattr(sprite, "name") and sprite.name == "car":
                            pg.quit()
                            sys.exit()

                        if self.direction.x > 0: # direita
                            self.hitbox.right = sprite.hitbox.left
                            self.rect.centerx = self.hitbox.centerx
                            self.pos.x = self.hitbox.centerx
                        if self.direction.x < 0: # esquerda
                            self.hitbox.left = sprite.hitbox.right
                            self.rect.centerx = self.hitbox.centerx
                            self.pos.x = self.hitbox.centerx
            
        else:
            if direction == "vertical":
                for sprite in self.colisao_sprites.sprites():
                    if sprite.hitbox.colliderect(self.hitbox):
                        if hasattr(sprite, "name") and sprite.name == "car":
                            pg.quit()
                            sys.exit()

                        if self.direction.y > 0: # baixo
                            self.hitbox.bottom = sprite.hitbox.top
                            self.rect.centery = self.hitbox.centery
                            self.pos.y = self.hitbox.centery
                        if self.direction.y < 0: # cima
                            self.hitbox.top = sprite.hitbox.bottom
                            self.rect.centery = self.hitbox.centery
                            self.pos.y = self.hitbox.centery
            # colisão vertical


    def mover(self, deltatime):

    # normalizar um vetor = tamanho do vetor é 1
    # resolve o problema de velocidades diagonais serem mais rápidas
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()
      
        # horizontal movimento e colisões
        self.pos.x += self.direction.x * self.speed * deltatime
        self.hitbox.centerx = round(self.pos.x) # para melhorar a colisão
        self.rect.centerx = self.hitbox.centerx # para desenhar o retângulo
        self.colisao("horizontal")

        # movimento vertical e colisões
        self.pos.y += self.direction.y * self.speed * deltatime
        self.hitbox.centery = round(self.pos.y)
        self.rect.centery = self.hitbox.centery
        self.colisao("vertical")


    
    def importar_imagens(self):
        path = "graphics/player/right/"
        self.animation = [pg.image.load(f"{path}{frame}.png").convert_alpha() for frame in range(4)]

    # importando de uma melhor maneira
        self.animations = {}
        for index, folder in enumerate(walk("graphics/player")):
            if index == 0:
                for name in folder[1]:
                    self.animations[name] = []
            
            else:
                for file_name in folder[2]:
                    path = folder[0].replace("\\", "/") + "/" + file_name
                    surf = pg.image.load(path).convert_alpha()
                    key = folder[0].split("\\")[1]
                    self.animations[key].append(surf)


    def comandos(self):
        key = pg.key.get_pressed()
        
        # horizontal
        if key[pg.K_RIGHT]:
            self.direction.x = 1
            self.status = "right"
        elif key[pg.K_LEFT]:
             self.direction.x = -1
             self.status = "left"
        else:
            self.direction.x = 0

        # vertical
        if key[pg.K_UP]:
            self.direction.y = -1
            self.status = "up"
        elif key[pg.K_DOWN]:
            self.direction.y = 1
            self.status = "down"
        else: 
            self.direction.y = 0

    def animar(self, deltatime):
        current_animation = self.animations[self.status]
        if self.direction.magnitude() != 0:
            self.frame_index += 10 * deltatime
            if self.frame_index >= len(current_animation):
                self.frame_index = 0
        else:
            self.frame_index = 0
        self.image = current_animation[int(self.frame_index)]
      

    def restringir(self):
        if self.rect.left < 640:
            self.pos.x = 640 + self.rect.width / 2
            self.hitbox.left = 640
            self.rect.left = 640
        if self.rect.right > 2560:
            self.pos.x = 2560 - self.rect.width / 2
            self.hitbox.right = 2560
            self.rect.right = 2560
        if self.rect.bottom > 3500:
            self.pos.y = 3500 - self.rect.height / 2
            self.rect.bottom = 3500
            self.hitbox.centery = self.rect.centery

    def update(self, deltatime):
        self.importar_imagens()
        self.comandos()
        self.mover(deltatime)
        self.animar(deltatime)
        self.restringir()