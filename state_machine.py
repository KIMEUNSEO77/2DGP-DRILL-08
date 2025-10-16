from event_to_string import event_to_string

class StateMachine:
    def __init__(self, start_state, rules):
        self.cur_state = start_state
        self.rules = rules
        self.cur_state.enter(('START', 0))  # 처음 시작할 때 enter 실행

    def update(self):
        self.cur_state.do()

    def draw(self):
        self.cur_state.draw()

    def handle_state_event(self, state_event):
        for check_event in self.rules[self.cur_state].keys():  # keys(): 딕셔너리의 모든 키들
            if check_event(state_event):  # 만약 true이면 (spacedown이면)
                self.next_state = self.rules[self.cur_state][check_event]  # next가 IDLE이 됨
                self.cur_state.exit(state_event)     # 현재 상태 exit 실행
                self.next_state.enter(state_event)   # 다음 상태 enter 실행
                # 현재 상태가 어떤 이벤트에 의해서 다음 상태로 바뀌는지 정보를 표시
                print(f'{self.cur_state.__class__.__name__}======={event_to_string(state_event)}======>{self.next_state.__class__.__name__}')
                self.cur_state = self.next_state  # 현재 상태를 다음 상태로 변경
                return

            # 처리 되지 않은 이벤트를 출력
            print(f'처리되지 않은 이벤트 {event_to_string(state_event)}')

