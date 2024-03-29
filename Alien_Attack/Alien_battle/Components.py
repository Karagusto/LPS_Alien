import pygame
import Alien_Attack.LPS.Interfaces as int




walkRight = [pygame.image.load('starship.png')]
walkLeft = [pygame.image.load('starship.png')]
char = pygame.image.load('starship.png')

class my_background(int.background):
    def __init__(self, screenwidth, screenheight):
        self.screenwidth = screenwidth
        self.screenheight = screenheight

    def drawBackground(self):
        win = pygame.display.set_mode((self.screenwidth, self.screenheight))
        pygame.display.set_caption("Alien Battle")
        return win




class my_player(int.player):
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = 5
        self.isJump = False
        self.left = False
        self.right = False
        self.walkCount = 0
        self.jumpCount = 10
        self.standing = True
        self.hitbox = (self.x + 15, self.y + 10, self.width//2, self.height)
        self.health = 10
        self.visible = True

    def draw(self, win):
        if self.walkCount + 1 >= 1:
            self.walkCount = 0

        if not(self.standing):
            if self.left:
                win.blit(walkLeft[self.walkCount // 3], (self.x, self.y))
                self.walkCount += 1
            elif self.right:
                win.blit(walkRight[self.walkCount // 3], (self.x, self.y))
                self.walkCount += 1
        else:
            win.blit(char, (self.x, self.y))
        self.hitbox = (self.x + 5, self.y, self.width//2 - 7, self.height//2)
        #pygame.draw.rect(win, (255, 0, 0), self.hitbox, 2)
        pygame.draw.rect(win, (255, 0, 0), (self.hitbox[0], self.hitbox[1] - 20, 50, 10))
        pygame.draw.rect(win, (0, 255, 0), (self.hitbox[0], self.hitbox[1] - 20, 50 - ((50/10) * (10 - self.health)), 10))
    def hit(self):
        if self.health > 0:
            self.health -= 1
            return self.health
        else:
            self.visible = False
            return self.health
        print("hit")

    def score(self):
        return 10

class my_projectile(int.projectile):
    def __init__(self, x, y, radius, color):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        # self.facing = facing
        self.vel = 8
        self.hitbox = (self.x - 20, self.y - 20, 20, 20)

    def draw(self, win):
        pygame.draw.circle(win, self.color, (self.x, self.y), self.radius)
        self.hitbox = (self.x - 10, self.y - 10, 20, 20)
        #pygame.draw.rect(win, self.color, self.hitbox, 2)

class my_enemy(int.enemy):
    enemySprite = [pygame.image.load('alien4.png')]

    def __init__(self, x, y, width, height, end):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.end = end
        self.path = [20, self.end]
        self.walkCount = 0
        self.vel = 3
        self.hitbox = (self.x, self.y, self.width//2, self.height//2)
        self.health = 10
        self.visible = True

    def draw(self, win):
        self.move()
        if self.visible:
            pygame.draw.rect(win, (255, 0, 0), (self.hitbox[0], self.hitbox[1] - 20, 50, 10))
            pygame.draw.rect(win, (0, 255, 0),
                             (self.hitbox[0], self.hitbox[1] - 20, 50 - ((50 / 10) * (10 - self.health)), 10))
            if self.walkCount + 1 >= 1:
                self.walkCount = 0
            if self.vel > 0:
                win.blit(self.enemySprite[self.walkCount//3], (self.x, self.y))
                self.walkCount += 1
            else:
                win.blit(self.enemySprite[self.walkCount // 3], (self.x, self.y))
                self.walkCount += 1
            self.hitbox = (self.x, self.y, self.width//2 + 5, self.height//2 + 5)
            #pygame.draw.rect(win, (255, 0, 0), self.hitbox, 2)

            pass

    def move(self):
        if self.vel > 0:
            if self.x + self.vel < self.path[1]:
                self.x += self.vel
            else:
                self.vel = self.vel * -1
                self.walkCount = 0
        else:
            if self.x - self.vel > self.path[0]:
                self.x += self.vel
            else:
                self.vel = self.vel * -1
                self.walkCount = 0
        pass

    def hit(self):
        print("boom!")
        if self.health > 0:
            self.health -= 1
            return self.health
        else:
            self.visible = False
            return self.health
        print("hit")
        pass

    def shoot(self):
        pass


#Class for collision development
class my_collision(int.collision):

    def __init__(self, hitbox1, hitbox2, hitbox, projectile):
        self.hitbox1 = hitbox1
        self.hitbox2 = hitbox2
        self.hitbox = hitbox
        self.projectile = projectile

    def isCollidingEnemy(self):
        if self.hitbox1[0] >= self.hitbox2[0] and self.hitbox1[0] < self.hitbox2[0] + self.hitbox2[2] or self.hitbox1[0] + self.hitbox1[2] >= self.hitbox2[0] and self.hitbox1[0] + self.hitbox1[2] < self.hitbox2[0] + self.hitbox2[2]:
            #print("xcrossover")
            if self.hitbox1[1] >= self.hitbox2[1] and self.hitbox1[1] < self.hitbox2[1] + self.hitbox2[3] or self.hitbox1[1] + self.hitbox1[3] >= self.hitbox2[1] and self.hitbox1[1] + self.hitbox1[3] < self.hitbox2[1] + self.hitbox2[3]:
                #print("xandycrossover")
                return 0

    def isCollidingBullet(self):
        if self.hitbox[1] - self.hitbox[3] < self.projectile.y + self.projectile.radius and self.hitbox[1] + self.hitbox[3] > self.projectile.y:
            if self.hitbox[0] + self.hitbox[2] > self.projectile.x and self.hitbox[0] - self.hitbox[2] < self.projectile.x + self.projectile.radius:
                return 0


class my_regras1(int.regras):

    def __init__(self, win, man, goblin, bullets, bullets2, score, isdead):
        self.win = win
        self.man = man
        self.goblin = goblin
        self.bullets = bullets
        self.bullets2 = bullets2
        self.score = score
        self.isdead = isdead