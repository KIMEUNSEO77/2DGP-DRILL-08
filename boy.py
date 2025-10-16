from pico2d import load_image, get_time
from sdl2 import SDL_KEYDOWN, SDLK_SPACE, SDLK_RIGHT, SDL_KEYUP, SDLK_LEFT

from state_machine import StateMachine

# 이벤트 체크 함수
def right_down(e): # e가 right key input인가를 확인 -> True/False 반환
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_RIGHT
def left_down(e): # e가 left key input인가를 확인 -> True/False 반환
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_LEFT
def right_up(e): # e가 right key up input인가를 확인 -> True/False
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_RIGHT
def left_up(e): # e가 left key up input인가를 확인 -> True/False
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_LEFT
def input_Akey(e): # e가 A key를 눌렀는지 확인
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == 'a'

def time_out(e): # e가 시간 초과 이벤트인가를 확인 -> True/False 반환
    return e[0] == 'TIME_OUT'

def space_down(e): # e가 space key input인가를 확인 -> True/False 반환
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_SPACE

class AutoRun:
    def __init__(self, boy):
        self.boy = boy
    def enter(self, e):
        self.boy.dir = self.boy.face_dir
        self.boy.wait_start_time = get_time()  # 현재 지난 시간 체크

    def exit(self, e):
        pass

    def do(self):
        self.boy.frame = (self.boy.frame + 1) % 8   # 2초가 경과하면 timeout 이벤트 발생
        self.boy.x += self.boy.dir * 10
        if self.boy.x <= 10:
            self.boy.x = 10
            self.boy.dir = self.boy.face_dir = 1
        elif self.boy.x >= 760:
            self.boy.x = 760
            self.boy.dir = self.boy.face_dir = -1
        if get_time() - self.boy.wait_start_time > 5.0:
            self.boy.state_machine.handle_state_event(('TIME_OUT', 0))

    def draw(self):
        if self.boy.face_dir == 1:  # right
            self.boy.image.clip_composite_draw(self.boy.frame * 100, 100, 100, 100, 0, '', self.boy.x,
                                               self.boy.y + 25, 200, 200)
        else:  # face_dir == -1: # left
            self.boy.image.clip_composite_draw(self.boy.frame * 100, 0, 100, 100, 0, '', self.boy.x,
                                               self.boy.y + 25, 200, 200)


class Run:
    def __init__(self, boy):
        self.boy = boy

    def enter(self, e):
        if right_down(e) or left_up(e):
            self.boy.dir = self.boy.face_dir = 1
        elif left_down(e) or right_up(e):
            self.boy.dir = self.boy.face_dir = -1

    def exit(self, e):
        pass

    def do(self):
        self.boy.frame = (self.boy.frame + 1) % 8   # 2초가 경과하면 timeout 이벤트 발생
        self.boy.x += self.boy.dir * 5

    def draw(self):
        if self.boy.face_dir == 1: # right
            self.boy.image.clip_draw(self.boy.frame * 100, 100, 100, 100, self.boy.x, self.boy.y)
        else: # face_dir == -1: # left
            self.boy.image.clip_draw(self.boy.frame * 100, 0, 100, 100, self.boy.x, self.boy.y)

class Sleep:
    def __init__(self, boy):
        self.boy = boy

    def enter(self, e):
        self.boy.dir = 0

    def exit(self, e):
        pass

    def do(self):
        self.boy.frame = (self.boy.frame + 1) % 8

    def draw(self):
        if self.boy.face_dir == 1: # right
            self.boy.image.clip_composite_draw(self.boy.frame * 100, 300, 100, 100, 3.141592/2, '', self.boy.x-25, self.boy.y-25,100,100)
        else: # face_dir == -1: # left
            self.boy.image.clip_composite_draw(self.boy.frame * 100, 200, 100, 100, -3.141592/2, '', self.boy.x+25, self.boy.y-25,100,100)

class Idle:
    def __init__(self, boy):
        self.boy = boy

    def enter(self, e):
        self.boy.dir = 0
        self.boy.wait_start_time = get_time() # 현재 지난 시간 체크

    def exit(self, e):
        pass

    def do(self):
        self.boy.frame = (self.boy.frame + 1) % 8   # 2초가 경과하면 timeout 이벤트 발생
        if get_time() - self.boy.wait_start_time > 2.0:
            #TIME_OUT 이벤트 발생
            self.boy.state_machine.handle_state_event(('TIME_OUT', 0))

    def draw(self):
        if self.boy.face_dir == 1: # right
            self.boy.image.clip_draw(self.boy.frame * 100, 300, 100, 100, self.boy.x, self.boy.y)
        else: # face_dir == -1: # left
            self.boy.image.clip_draw(self.boy.frame * 100, 200, 100, 100, self.boy.x, self.boy.y)

class Boy:
    def __init__(self):
        self.x, self.y = 400, 90
        self.frame = 0
        self.face_dir = 1
        self.dir = 0
        self.image = load_image('animation_sheet.png')

        self.IDLE = Idle(self)
        self.SLEEP = Sleep(self)
        self.RUN = Run(self)
        self.AUTORUN = AutoRun(self)

        self.state_machine = StateMachine(
            self.AUTORUN,  # 초기 상태
            {
                self.SLEEP : {space_down: self.IDLE},
                self.IDLE : {right_up:self.RUN, left_up : self.RUN, left_down: self.RUN, right_down: self.RUN, time_out: self.SLEEP},
                self.RUN : {right_down:self.IDLE, left_down:self.IDLE, left_up:self.IDLE, right_up:self.IDLE},
                self.AUTORUN : {time_out:self.IDLE}
            })

    def update(self):
        self.state_machine.update()


    def draw(self):
        self.state_machine.draw()

    def handle_event(self, event):
        self.state_machine.handle_state_event(('INPUT', event))  # 스테이트 머신에 적합한 이벤트를 전달
