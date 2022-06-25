import pygame
from sys import exit
from random import randint

pygame.init()

class Paddle:
    def __init__(self, player):
        super().__init__()

        self.paddle_width = 25
        self.paddle_height = 100

        self.speed = 4

        self.up_key = False
        self.down_key = False

        self.points = 0

        self.player = player
        self.winner = ""

        self.starting_ypos = 256 - self.paddle_height/2

        if self.player == 1:
            self.rect = pygame.Rect(10, self.starting_ypos, self.paddle_width, self.paddle_height)
            self.up_key = pygame.K_w
            self.down_key = pygame.K_s
        elif self.player == 2:
            self.rect = pygame.Rect(1024 - 10 - self.paddle_width, self.starting_ypos, self.paddle_width, self.paddle_height)
            self.up_key = pygame.K_UP
            self.down_key = pygame.K_DOWN
        elif self.player == 3:
            self.rect = pygame.Rect(499, 1, 26, 110)
            self.speed = 6

    def reset(self):
        ball.vel = 10
        self.rect.y = self.starting_ypos
        self.points = 0
        self.winner = ""

    def win_condition(self):
        if self.points >= 11:
            
            if self.player == 1: self.winner = "Player 1 "
            elif self.player == 2: self.winner = 'Player 2 '
            
            game_active = False
    
    def controls(self):
        keys = pygame.key.get_pressed()
        if self.player == 1 or self.player == 2:
            if keys[self.up_key] and self.rect.top > 0:
                self.rect.y -= self.speed
            if keys[self.down_key] and self.rect.bottom < 512:
                self.rect.y += self.speed
        if self.player == 3:
            if self.rect.bottom < 512 and self.rect.top > 0:
                self.rect.y += self.speed
            else:
                self.speed = -self.speed
                self.rect.y += self.speed


    def draw_score(self):
        score_font = pygame.font.Font('pong.ttf', 75)
        score_text = score_font.render(str(self.points), False, white)
        p1pos = (492, 10)
        p2pos = (540, 10)
        p3pos = (0, 0)
        if self.player == 1:
            score_rect = score_text.get_rect(topright = p1pos)
        elif self.player == 2:
            score_rect = score_text.get_rect(topleft = p2pos)
        elif self.player == 3:
            score_rect = score_text.get_rect(topright = p3pos)
        screen.blit(score_text, score_rect)

    def update(self):
        self.win_condition()
        self.draw_score()
        self.controls()
        pygame.draw.rect(screen, white, self.rect)
        

class Ball:
    def __init__(self):
        super().__init__()

        self.ball_width = 25
        self.ball_height = 25

        self.xdir = 0
        self.ydir = 0
        self.vel = 10

        self.starting_dir = randint(0, 3)
        if self.starting_dir == 0:
            self.xdir = self.vel
            self.ydir = self.vel
        elif self.starting_dir == 1:
            self.xdir = -self.vel
            self.ydir = self.vel
        elif self.starting_dir == 2:
            self.xdir = -self.vel
            self.ydir = -self.vel
        elif self.starting_dir == 3:
            self.xdir = self.vel
            self.ydir = -self.vel

        self.rect = pygame.Rect(512 - self.ball_width/2, 256 - self.ball_height/2, self.ball_width, self.ball_height)

    def change_speed(self):
        has_run = False
        has_this_run = False
        this_one_though = False
        if (paddle1.points + paddle2.points) == 5 and has_run == False:
            self.vel = 12
        if (paddle1.points + paddle2.points) == 10 and has_this_run == False:
            self.vel = 15
        if (paddle1.points + paddle2.points) == 15 and this_one_though == False:
            self.vel = 18

    def update_dir(self):
        self.starting_dir = randint(0, 3)

        if self.starting_dir == 0:
            self.xdir = self.vel
            self.ydir = self.vel
        elif self.starting_dir == 1:
            self.xdir = -self.vel
            self.ydir = self.vel
        elif self.starting_dir == 2:
            self.xdir = -self.vel
            self.ydir = -self.vel
        elif self.starting_dir == 3:
            self.xdir = self.vel
            self.ydir = -self.vel

    def ball_movement(self):
        self.rect.x += self.xdir
        self.rect.y += self.ydir
        if self.rect.y <= 0 or self.rect.bottom >= 512:
            self.ydir = -self.ydir
            if self.rect.y <= 0:
                self.rect.y = 1
        if self.rect.x <= 0 or self.rect.right >= 1024:
            if self.rect.right >= 1024:
                paddle1.points += 1
            if self.rect.x <= 0:
                paddle2.points += 1
            self.rect.center = 512, 256
            self.update_dir()

        if self.rect.colliderect(paddle1.rect):
            self.rect.x = 35
            self.xdir = -self.xdir
        if self.rect.colliderect(paddle2.rect):
            self.xdir = -self.xdir
            self.rect.right = 989
        if self.rect.colliderect(paddle3.rect) and (self.rect.clipline(512, 0, 512, 512) or self.rect.clipline(502, 0, 502, 512) or self.rect.clipline(522, 0, 522, 512)):

            self.ydir = -self.ydir
            self.rect.x += self.xdir
            self.rect.y += self.ydir * 2
        elif self.rect.colliderect(paddle3.rect):

            self.xdir = -self.xdir
            self.rect.x += self.xdir
            self.rect.y += self.ydir
        
        
    def update(self):
        self.change_speed()
        self.ball_movement()
        pygame.draw.rect(screen, white, self.rect)

width, height = 1024, 512
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Pong")

clock = pygame.time.Clock()

title_font = pygame.font.Font('pong.ttf', 200)

game_active = False

plays = 0

black = (0, 0, 0)
white = (255, 255, 255)

ball = Ball()

paddle1 = Paddle(1)
paddle2 = Paddle(2)
paddle3 = Paddle(3)

def start_screen():
    global game_active

    title = title_font.render("Pong", False, white)
    title_rect = title.get_rect(midtop = (512, 50))

    message_font = pygame.font.Font('pong.ttf', 30)
    message = message_font.render('Press Enter to play.', False, white)
    message_rect = message.get_rect(midtop = (512, 370))

    winner = message_font.render(paddle1.winner + paddle2.winner + ' is the Winner!', False, white)
    winner_rect = winner.get_rect(midtop = (512, 325))

    keys = pygame.key.get_pressed()
    if keys[pygame.K_RETURN]:
        game_active = True
        paddle1.reset()
        paddle2.reset()

    screen.fill(black)
    screen.blit(message, message_rect)
    screen.blit(title, title_rect)

    if plays > 0: screen.blit(winner, winner_rect)

def draw_window():
    screen.fill(black)

def main():
    global game_active
    global plays

    clock = pygame.time.Clock()
    while True:
        clock.tick(30)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        if game_active:
            
            if paddle1.winner != '' or paddle2.winner != '':
                game_active = False

            plays += 1
            draw_window()
            paddle1.update()
            paddle2.update()
            paddle3.update()
            ball.update()
            pygame.draw.line(screen, white, (512, 0), (512, 512))

        else:
            start_screen()

        pygame.display.update()

if __name__ == '__main__':
    main()