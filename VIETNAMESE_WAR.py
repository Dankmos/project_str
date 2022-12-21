import pygame as pg
import numpy as np
import math as mh
import random
import sys

pg.init()

'''
setting up music
you can add something else

TODO
1) add more music from those times
2) add ability to choose music or skip it
3) add 'mute' button
'''

pg.mixer.init()
pg.mixer.music.load("textures//creedence-clearwater-revival_-_fortunate-son.mp3")
pg.mixer.music.play()

clock = pg.time.Clock()
dis = pg.display.set_mode((800, 600))

'''
uploading images from folder 'textures'
'''

bgimg = pg.image.load("textures//1548706982174921911.png")
bgimg = pg.transform.scale(bgimg, (800, 600))

guk_img = pg.image.load("textures//guk.png")
guk_img = pg.transform.scale(guk_img, (70, 70))

boss_img = pg.image.load("textures//boss.png")
boss_img = pg.transform.scale(boss_img, (110, 70))

tree_img = pg.image.load("textures//tree1.png")
tree_img = pg.transform.scale(tree_img, (90, 160))

player_img = pg.image.load("textures//test1.png")
player_img = pg.transform.scale(player_img, (300, 130))

player_img_temp = pg.image.load("textures//test1.png")
player_img_temp = pg.transform.scale(player_img, (300, 130))

bomb_img = pg.image.load("textures//bomb1.png")
bomb_img = pg.transform.scale(bomb_img, (11, 23))

grass_img = pg.image.load("textures//grass.png")
grass_img = pg.transform.scale(grass_img, (800, 100))

napalm_img = pg.image.load("textures//napalm1.png")
napalm_img = pg.transform.scale(napalm_img, (100, 70))

rpg_img = pg.image.load("textures//rpg.png")
rpg_img = pg.transform.scale(rpg_img, (60, 11))

rpg_img_temp = pg.image.load("textures//rpg.png")

boom_img = pg.image.load("textures//boom1.png")
boom_img = pg.transform.scale(boom_img, (270, 150))

'''
setting up font and color for text in the game
here are fonts for 'score' and 'You lose!'
'''

font = pg.freetype.Font('textures//GenJyuuGothicX-Bold.ttf', 80)
scorefont = pg.freetype.Font('textures//GenJyuuGothicX-Bold.ttf', 20)
lvlfont = pg.freetype.Font('textures//GenJyuuGothicX-Bold.ttf', 20)

text, _ = font.render("You lose!", (255, 0, 0))
score = 0

'''
class contains all inf about player
pos, lifes, rotation and speed, is player dead

also defines what player can do
now there are moving, dropping bomb(realised in Controlling)
and dying
'''
class Player:
    def __init__(self):
        self.pos = [0, 0]
        self.lifes = 2
        self.speed = 2
        self.rotation = 0
        self.is_dead = False
        self.death_timer = 180
        
    def Move(self):
        self.pos[0] += self.rotation * 0.6
        
        if self.pos[0] < -300:
            self.pos[0] = 800
        elif self.pos[0] > 800:
            self.pos[0] = -300
    
    def Controlling(self, event):
        
        global player_img_temp, player_img
        
        if event[0]:
            self.rotation += 0.7
            
            if self.rotation > 30:
                self.rotation = np.sign(self.rotation) * 30
            player_img_temp = pg.transform.rotate(player_img, -self.rotation)
            
        elif event[1]:
            self.rotation -= 0.7
            
            if -30 > self.rotation:
                self.rotation = np.sign(self.rotation) * 30
            player_img_temp = pg.transform.rotate(player_img, -self.rotation)
            
        elif event[2]:
            self.pos[1] -= self.speed
            
        elif event[3]:
            self.pos[1] += self.speed
            
        elif event[4]:
            pass
            
    def Death(self):
        self.is_dead = True
        self.pos[1] += 1
        if self.pos[1] > 450:
            self.death_timer -= 1
            self.pos[1] = 451
        if self.death_timer <= 0:
            pg.quit()
            sys.exit()
        
'''
Boom motherfucker

class contains inf about bombs
pos, speed, is exploded
and defines moving
'''

class Bomb:
    def __init__(self, x, y):
        self.pos = [x, y]
        self.speed = 0
        self.gravi = 0.2
        self.exploded = False
        self.timer = 60
    
    def Dropping(self):
        if self.exploded:
            self.timer -= 1
        else:
            self.pos[1] += self.speed
            self.speed += self.gravi
    
'''
they're on trees, Johnny!

this class contains inf about enemy
his pos, is it Boss, how many lifes
also it defines all actions
shooting for Boss if the only thing for now

TODO
1)make something else
for example some guks can move (done)
'''
  
class Guk:
    def __init__(self, B, l):
        self.on_tree = random.choice((True, False, False))
        self.pos = [random.randint(0, 730), 490 - 80 * self.on_tree]
        self.is_Boss = B
        self.life = l
        self.timer = 120
        self.RPG_pos = [-100, -100]
        self.xs = 0
        self.ys = 0
        self.moves = False
        if not self.on_tree:
            self.moves = random.choice([True] + [False] * 2)
        self.speed = random.choice((1, -1))
        
    def moving(self):
        self.pos[0] += self.speed
        
        if 0 > self.pos[0] or self.pos[0] > 750:
            # print(self.pos[0])
            self.speed = -self.speed
            self.pos[0] += self.speed * 2
            
        
    def Shoot(self, p_pos):
        global rpg_img_temp, rpg_img
        
        self.timer -= 1
        
        if self.timer <= 0:
            self.timer = 120
            self.RPG_pos = [i for i in self.pos]
            self.xs = p_pos[0] + 150 - self.pos[0]
            self.ys = p_pos[1] + 100 - self.pos[1]
            
            if self.xs < 0:
                ang = - mh.degrees(mh.atan(self.ys / self.xs));
                rpg_img_temp = pg.transform.rotate(rpg_img, ang)
            else:
                ang = 180 - mh.degrees(mh.atan(self.ys / self.xs));
                rpg_img_temp = pg.transform.rotate(rpg_img, ang)
                
        if p_pos[1] + 100 >= self.RPG_pos[1] and p_pos[0]-30 < self.RPG_pos[0] < p_pos[0]+170:
            return True
        self.Shot()
        return False
        
    def Shot(self):
        self.RPG_pos[0] += self.xs // 100
        self.RPG_pos[1] += self.ys // 100
        
        if 800 < self.RPG_pos[0] < 0 or self.RPG_pos[1] < 0:
            self.RPG_pos = [-100, -100]

'''
main game

this class stores all inf about current situation in a game
also it defines all actions in a game
dropping bombs by player, spawning enemys
and main process of game
'''

class Game:
    def __init__(self):
        self.level = 1
        self.guks = []
        self.bombs = []
        self.player = Player()
        self.guks_killed = 1
        self.on_boss = False
        
    def Drop_bomb(self):
        self.bombs.append(Bomb(self.player.pos[0] + 100, self.player.pos[1] + 100))
        
    def Spawn(self):
        if len(self.guks) < self.level + 1 and not self.on_boss:
            lifes = 1
            self.guks.append(Guk(False, lifes))
        elif len(self.guks) == 0 and self.on_boss:
            lifes = 3 * self.level
            self.guks.append(Guk(True, lifes))
            
    def Running(self):
        global move_dir, score
        
        if not self.player.is_dead:
            self.player.Move()
            game.player.Controlling(move_dir)
            self.Spawn()
            
            for b in self.bombs:
                b.Dropping()
                
                if b.pos[1] > 550:
                    for g in self.guks:
                        if g.pos[0] - 31 < b.pos[0] < g.pos[0] + 90:
                            g.life -= 1
                            
                    if not b.exploded:
                        b.pos[0] += 1000
                    b.exploded = True
                    
                if b.timer <= 0:
                    self.bombs.remove(b)
                    
            if not self.guks_killed % (10 * self.level):
                self.on_boss = True
                self.guks_killed = 1
                    
            for g in self.guks:
                if g.moves:
                    g.moving()
                    
                if g.life <= 0:
                    if g.is_Boss:
                        self.on_boss = False
                        score += 9
                        self.level += 1
                        
                    score += 1
                    self.guks.remove(g)
                    self.guks_killed += 1
                    
                if g.is_Boss:
                    self.player.is_dead = g.Shoot(game.player.pos)
                
        if self.player.pos[1] > 280 or self.player.is_dead:
            self.player.Death()

game = Game()
move_dir = [0] * 5

'''
Main Cycle

here are all about running game
also this cycle displays image

TODO
1) make function for displaying image
it's not the best way to show image by using main cycle
2) move checking events from here to class Player or class Game
3) create another way to keep inf about events instead of using list
'''

while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()
            
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_RIGHT:
                move_dir[0] = 1
                
            elif event.key == pg.K_LEFT:
                move_dir[1] = 1
                
            elif event.key == pg.K_UP:
                move_dir[2] = 1
                
            elif event.key == pg.K_DOWN:
                move_dir[3] = 1
                
            elif event.key == pg.K_SPACE:
                move_dir[4] = 1
                game.Drop_bomb()
                
            elif event.key -- pg.K_ESCAPE:
                pg.quit()
                sys.exit()
                
        if event.type == pg.KEYUP:
            if event.key == pg.K_RIGHT:
                move_dir[0] = 0
                
            elif event.key == pg.K_LEFT:
                move_dir[1] = 0
                
            elif event.key == pg.K_UP:
                move_dir[2] = 0
                
            elif event.key == pg.K_DOWN:
                move_dir[3] = 0
                
            elif event.key == pg.K_SPACE:
                move_dir[4] = 0
                
    game.Running()
    
    dis.blit(bgimg, (0, 0))
    dis.blit(player_img_temp, game.player.pos)
    
    for g in game.guks:
        guk = guk_img
        
        if g.on_tree:
            dis.blit(tree_img, g.pos)
            
        if g.is_Boss:
            guk = boss_img
            
        dis.blit(rpg_img_temp, g.RPG_pos)
        dis.blit(guk, g.pos)
        
    for b in game.bombs:
        if b.exploded:
            dis.blit(napalm_img, (b.pos[0] - 1050, b.pos[1] - 80))
        else:
            dis.blit(bomb_img, b.pos)
            
    if game.player.is_dead:
        dis.blit(boom_img, game.player.pos)
        dis.blit(text, (200, 260))
        
    dis.blit(grass_img, (0, 500))
    
    #rendering text
    lvlimg, _ = scorefont.render('level: {}'.format(game.level))
    scoreimg, _ = scorefont.render('score: {}'.format(score)) 
    
    dis.blit(scoreimg, (700, 10))
    dis.blit(lvlimg, (10, 10))
    
    clock.tick(60)
    pg.display.update()