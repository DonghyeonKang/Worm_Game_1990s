import pygame   # 게임 모듈 
import time     # 이용
import random

UP = 0
DOWN = 2
LEFT = 1
RIGHT = 3

class Food:
    def __init__(self):
        self.create_food()
        self.color = (255, 201, 14)
        self.length = 1

    def create_food(self):
        x = random.randint(1, 1200 // 20)
        y = random.randint(1, 880 // 20)
        self.position = [[x * 20, y * 20]]

    def draw_food(self, screen):
        draw_obj(screen, self)

    def get_FoodPosition(self):
        return self.position[0]


class Worm:
    def __init__(self):
        self.color = (185, 122, 87, 255)
        self.length = 1
        self.position = [[500, 500]]
        self.direction = [0]
        self.delay = 0

    def create_worm(self):
        self.position.append([self.position[self.length - 1][0], self.position[self.length - 1][1]])
        self.direction.append(self.direction[self.length - 1])
        self.length += 1
        self.delay = 1

    def draw_worm(self, screen):
        draw_obj(screen, self)

    def move(self):     # 위치 변경 후 방향 변경
        for i in range(self.length - self.delay):
            if self.direction[i] == 0:        # UP 
                self.position[i][1] -= 20
            elif self.direction[i] == 2:      # DOWM
                self.position[i][1] += 20
            elif self.direction[i] == 1:      # left 
                self.position[i][0] -= 20
            elif self.direction[i] == 3:      # right
                self.position[i][0] += 20

        if self.length > 1:
            tmp1 = self.direction[0]
            for i in range(1, self.length):
                tmp2 = self.direction[i]
                self.direction[i] = tmp1
                tmp1 = tmp2

        if self.delay == 1:
            self.delay = 0

    def control_worm(self, key):    # 머리 위치만 바꿈
        if (key % 2) == (self.direction[0] % 2):     # 
            return     
        if key == 0:
            self.direction[0] = 0
        elif key == 2:
            self.direction[0] = 2
        elif key == 1:
            self.direction[0] = 1
        elif key == 3:
            self.direction[0] = 3
    
    def get_HeadPosition(self):
        return self.position[0]

#-------------------------------------------

def draw_obj(screen, obj):
    for i in range(obj.length):
        rect = pygame.Rect(obj.position[i], (20, 20))
        pygame.draw.rect(screen, obj.color, rect)

def check_position(worm, food):
    worm_head = worm.get_HeadPosition()    
    if worm_head == food.get_FoodPosition():
        food.create_food()
        worm.create_worm()
    if worm_head[0] < 0 or worm_head[0] > 1180 or worm_head[1] < 0 or worm_head[1] > 880:
        time.sleep(0.5)
        game_over(worm, food)

def game_over(worm, food):
    # 커튼 올리고
    rect = pygame.Rect((0, 920), (1200, 20))
    pygame.draw.rect(screen, (185, 122, 87, 255), rect)
    for i in range(int(900 / 20)):
        worm.draw_worm(screen)
        food.draw_food(screen)
        pygame.Rect.inflate_ip(rect, 0, 40)
        pygame.draw.rect(screen, (185, 122, 87, 255), rect)
        pygame.display.update()
        clock.tick(50)
    
    # 초기화 
    worm.__init__()
    food.__init__()

    # 커튼 내리고
    for i in range(int(900 / 20)):
        pygame.Surface.fill(screen, (239, 228, 176))
        worm.draw_worm(screen)
        food.draw_food(screen)
        pygame.Rect.inflate_ip(rect, 0, -40)
        pygame.draw.rect(screen, (185, 122, 87, 255), rect)
        pygame.display.update()
        clock.tick(50)
    time.sleep(1.3)


#-------------------------------------------
pygame.init()   # 모든 모듈 초기화 
screen = pygame.display.set_mode((1200, 900))
pygame.display.set_caption("Worm_Game") #게임 이름
clock = pygame.time.Clock()
run = True
worm = Worm()
food = Food()

while(run):
    for event in pygame.event.get(): # running 중 키보드나,마우스 입력값(이벤트)을 체크해주는것
        if event.type == pygame.QUIT: # 창이 닫히는 이벤트가 발생하였는지
            run = False # 게임이 진행중이 아님
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                run = False
            elif event.key == pygame.K_UP:
                worm.control_worm(UP)
            elif event.key == pygame.K_DOWN:
                worm.control_worm(DOWN)
            elif event.key == pygame.K_LEFT:
                worm.control_worm(LEFT)
            elif event.key == pygame.K_RIGHT:
                worm.control_worm(RIGHT)
    
    # 화면 채우기
    pygame.Surface.fill(screen, (239, 228, 176))
    # 지렁이 이동
    worm.move()
    # 위치 확인
    check_position(worm, food)
    # 지렁이 출력
    worm.draw_worm(screen)
    # 먹이 출력
    food.draw_food(screen)
    # 게임화면 업데이트
    pygame.display.update()
    clock.tick(5 + 0.5 * worm.length)


pygame.quit()