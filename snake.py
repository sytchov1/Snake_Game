import pygame
import sys
import random


class Cube:
    def __init__(self, x, y, color):
        self.pos_x = x
        self.pos_y = y
        self.color = color


class Snake:
    parts = []

    def __init__(self):
        self.size = 3
        self.speedX = 0
        self.speedY = 0

        x = 200
        y = 200
        self.parts.append(Cube(x, y, RED))
        for i in range(self.size - 1):
            y += scale
            self.parts.append(Cube(x, y, WHITE))

    def draw(self):
        for part in self.parts:
            pygame.draw.rect(sc, part.color, (part.pos_x, part.pos_y, scale, scale))
            pygame.draw.rect(sc, GREY, (part.pos_x, part.pos_y, scale, scale), 2)

    def rotate(self, x, y):
        if self.speedX == self.speedY == 0:
            if y == 1:
                return
        elif self.speedX == 1 and x == -1 or self.speedX == -1 and x == 1 or self.speedY == 1 and y == -1 or self.speedY == -1 and y == 1:
            return
        self.speedX = x
        self.speedY = y

    def move(self):
        if self.speedX == self.speedY == 0:
            pass
        else:
            tempX = self.parts[0].pos_x
            tempY = self.parts[0].pos_y
            for part in self.parts:
                if self.parts.index(part) == 0:
                    part.pos_x += self.speedX * scale
                    part.pos_y += self.speedY * scale
                else:
                    part.pos_x, tempX = tempX, part.pos_x
                    part.pos_y, tempY = tempY, part.pos_y

    def grow(self):
        self.parts.insert(1, Cube(self.parts[0].pos_x, self.parts[0].pos_y, WHITE))
        self.size += 1

    def isFood(self):
        global apple
        if (self.parts[0].pos_x == apple.pos_x) and (self.parts[0].pos_y == apple.pos_y):
            while True:
                appleX = random.randint(0, 19) * scale
                appleY = random.randint(0, 19) * scale
                flag = True
                for part in self.parts:
                    if (part.pos_x == appleX) and (part.pos_y == appleY):
                        flag = False
                        break
                if flag:
                    break
            apple = Cube(appleX, appleY, GREEN)
            self.grow()

    def isLose(self):
        if self.parts[0].pos_x < 0 or self.parts[0].pos_x > Width - scale or self.parts[0].pos_y < 0 or self.parts[0].pos_y > Height - scale:
            textSize = font.render('Ваша длина = ' + str(self.size), 1, (200, 0, 200))
            placeSize = textSize.get_rect(center=(Width / 2, Height / 2 + 32))
            sc.blit(textSize, placeSize)
            sc.blit(textLose, placeLose)
            pygame.display.update()
            pygame.time.delay(1500)
            sys.exit()
        else:
            for part in self.parts:
                if self.parts.index(part) == 0:
                    headX = part.pos_x
                    headY = part.pos_y
                elif headX == part.pos_x and headY == part.pos_y:
                    textSize = font.render('Ваша длина = ' + str(self.size), 1, (200, 0, 200))
                    placeSize = textSize.get_rect(center=(Width / 2, Height / 2 + 32))
                    sc.blit(textSize, placeSize)
                    sc.blit(textLose, placeLose)
                    pygame.display.update()
                    pygame.time.delay(1500)
                    sys.exit()

    def isWin(self):
        if self.size == (Width * Height) / scale:
            sc.blit(textWin, placeWin)
            pygame.display.update()
            pygame.time.delay(1500)
            sys.exit()


FPS = 10
RED = (255, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
DGREEN = (0, 128, 0)
GREY = (128, 128, 128)
scale = 20
Height = 400
Width = 400

pygame.init()

clock = pygame.time.Clock()
sc = pygame.display.set_mode((Width, Height))

snake = Snake()
snake.draw()
apple = Cube(random.randint(0, 19) * scale, random.randint(0, 19) * scale, GREEN)
pygame.draw.rect(sc, DGREEN, (apple.pos_x, apple.pos_y, scale, scale), 2)
pygame.draw.rect(sc, GREEN, (apple.pos_x, apple.pos_y, scale, scale))
pygame.display.update()

font = pygame.font.SysFont("comicsansms", 32)
textWin = font.render('Победа!', 1, (200, 0, 200))
textLose = font.render('Поражение!', 1, (200, 0, 200))
placeWin = textWin.get_rect(center=(Width / 2, Height / 2))
placeLose = textLose.get_rect(center=(Width / 2, Height / 2 - 32))


while 1:
    for i in pygame.event.get():
        if i.type == pygame.QUIT:
            sys.exit()
        elif i.type == pygame.KEYDOWN:
            if i.key == pygame.K_ESCAPE:
                sys.exit()
            elif i.key == pygame.K_UP:
                snake.rotate(0, -1)
            elif i.key == pygame.K_DOWN:
                snake.rotate(0, 1)
            elif i.key == pygame.K_LEFT:
                snake.rotate(-1, 0)
            elif i.key == pygame.K_RIGHT:
                snake.rotate(1, 0)

    sc.fill((0, 0, 0))
    pygame.draw.rect(sc, GREEN, (apple.pos_x, apple.pos_y, scale, scale))
    pygame.draw.rect(sc, DGREEN, (apple.pos_x, apple.pos_y, scale, scale), 2)
    snake.move()
    snake.isLose()
    snake.isFood()
    snake.isWin()
    snake.draw()
    pygame.display.update()
    clock.tick(FPS)
