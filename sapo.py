import pygame as pg, sys
from settings import *
from player import Jogador
from car import Carro
from random import choice,randint
from sprites import *

class AllSprites(pg.sprite.Group):
    def __init__(self):
        super().__init__()
        self.offset = pg.math.Vector2()
        self.fundo = pg.image.load("graphics/main/map.png").convert()
        self.frente = pg.image.load("graphics/main/overlay.png").convert_alpha()

    def customize(self):

        self.offset.x = jogador.rect.centerx - comprimento_tela / 2
        self.offset.y = jogador.rect.centery - altura_tela / 2  

        tela.blit(self.fundo,-self.offset)

        for sprite in sorted(self.sprites(), key = lambda sprite: sprite.rect.centery):
            offset_pos = sprite.rect.topleft - self.offset
            tela.blit(sprite.image, offset_pos)
        
        tela.blit(self.frente,-self.offset)

pg.init()
tela = pg.display.set_mode((comprimento_tela, altura_tela))
pg.display.set_caption("Travessia")
clock = pg.time.Clock()

all_sprites = AllSprites()
obstaculo_sprites = pg.sprite.Group()

jogador = Jogador((2062,3274), all_sprites, obstaculo_sprites)

# timer
car_timer = pg.event.custom_type()
pg.time.set_timer(car_timer, 50)
pos_list = []

font = pg.font.Font(None, 50)
text_surf = font.render("Vitória! Vamo trabaia", True, "White")
text_rect = text_surf.get_rect(center = (640, 360))

# music
music = pg.mixer.Sound("music.mp3")
music.play(loops = -1)

# sprite setup
for file_name, pos_list in OBJ_SIMPLES.items():
    path = f"graphics/objects/simple/{file_name}.png"
    surf = pg.image.load(path).convert_alpha()
    for pos in pos_list:
        SimpleSprite(surf, pos, [all_sprites, obstaculo_sprites])

for file_name, pos_list in OBJ_GRANDES.items():
    path = f"graphics/objects/long/{file_name}.png"
    surf = pg.image.load(path).convert_alpha()
    for pos in pos_list:
        LongSprite(surf, pos, [all_sprites, obstaculo_sprites])


while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()
        if event.type == car_timer:
            random_pos = choice(INICIO_CARROS)
            if random_pos not in pos_list:
                pos_list.append(random_pos)
                new_pos = (random_pos[0], random_pos[1] + randint(-8,8))
                Carro(new_pos, [all_sprites, obstaculo_sprites])
            if len(pos_list) > 5:
                del pos_list[0]



    deltatime = clock.tick()/1000

    tela.blit(tela, (0,0))
    tela.fill((0,0,0))

    if jogador.pos.y >= 1180:
        all_sprites.update(deltatime)

        all_sprites.customize()

    else:
        tela.fill("Crimson")
        tela.blit(text_surf, text_rect)

    pg.display.update()

