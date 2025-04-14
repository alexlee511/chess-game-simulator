import pygame
import sys, os, math



initial_boardmatrix = [[1, 1, 1, 1, 1, 1, 1, 1],
               [1, 1, 1, 1, 1, 1, 1, 1],
               [0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0],
               [2, 2, 2, 2, 2, 2, 2, 2],
               [2, 2, 2, 2, 2, 2, 2, 2]]


MAXNUM = float("inf")
MINNUM = -float("inf")
MAXTUPLE = (MAXNUM, MAXNUM)
MINTUPLE = (MINNUM, MINNUM)
ori_pos = 0
new_pos = 0

# 方向: 1:左, 2:中, 3:右
def single_move(initial_pos, direction, turn):
    if turn == 1:
        if direction == 1:
            return initial_pos[0] + 1, initial_pos[1] - 1
        elif direction == 2:
            return initial_pos[0] + 1, initial_pos[1]
        elif direction == 3:
            return initial_pos[0] + 1, initial_pos[1] + 1
    elif turn == 2:
        if direction == 1:
            return initial_pos[0] - 1, initial_pos[1] - 1
        elif direction == 2:
            return initial_pos[0] - 1, initial_pos[1]
        elif direction == 3:
            return initial_pos[0] - 1, initial_pos[1] + 1

def alterturn(turn):
    if turn == 1:
        return 2
    if turn == 2:
        return 1

#棋子移動資訊
class Action:
    def __init__(self, coordinate, direction, turn):
        self.coordinate = coordinate
        self.direction = direction
        self.turn = turn
    def getaction(self):
        return self.coordinate, self.direction, self.turn

#介面控制、流程控制
class BreakthroughGame:
    def __init__(self):
        pygame.init()
        self.width, self.height = 700, 560
        self.sizeofcell = int(560/8)
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.screen.fill([123, 63, 0])
        self.board = 0
        self.blackchess = 0
        self.whitechess = 0
        self.outline = 0
        self.reset = 0
        self.winner = 0
        self.computer = None
        self.auto_choose = False #自動輪到電腦移動

        # status 0: 尚未選擇棋子  1: 選擇移動位置; 2: end
        # turn 1:黑棋 2:白棋
        self.status = 0
        self.turn = 1
        # 棋子座標
        self.ori_x = 0
        self.ori_y = 0
        self.new_x = 0
        self.new_y = 0

        # 0 空格, 1:黑棋, 2:白棋
        self.boardmatrix = [[1, 1, 1, 1, 1, 1, 1, 1],
                            [1, 1, 1, 1, 1, 1, 1, 1],
                            [0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0],
                            [2, 2, 2, 2, 2, 2, 2, 2],
                            [2, 2, 2, 2, 2, 2, 2, 2]]

        pygame.display.set_caption("Breakthrough")
        self.initgraphics()
    
    #遊戲運行
    def run(self):

        self.screen.fill([123, 63, 0])

        if self.auto_choose and self.status != 5:
            if self.turn == 1:

                self.ai_move_alphabeta(1)

        if self.status == 5:
            # Black
            if self.turn == 1:

                self.ai_move_alphabeta(2)

            elif self.turn == 2:

                self.ai_move_alphabeta(2)

        #介面互動偵測
        for event in pygame.event.get():
            #退出遊戲
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            #遊戲衝新開始
            elif event.type == pygame.MOUSEBUTTONDOWN and self.isreset(event.pos):
                self.boardmatrix = [[1, 1, 1, 1, 1, 1, 1, 1],
                            [1, 1, 1, 1, 1, 1, 1, 1],
                            [0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0],
                            [2, 2, 2, 2, 2, 2, 2, 2],
                            [2, 2, 2, 2, 2, 2, 2, 2]]
                self.turn = 1
                self.status = 0
                self.auto_choose = False
                #自動移動時棋子的前後座標
                global ori_pos
                global new_pos
                ori_pos = 0
                new_pos = 0
            #玩家與電腦對戰
            elif event.type == pygame.MOUSEBUTTONDOWN and self.iscomputer(event.pos):
                if not self.auto_choose:
                    self.auto_choose = True
                    self.ai_move_alphabeta(1)


            #電腦與電腦對戰
            elif event.type == pygame.MOUSEBUTTONDOWN and self.isauto(event.pos):
                self.status = 5

            #玩家選擇白棋
            elif event.type == pygame.MOUSEBUTTONDOWN and self.status == 0:
                x, y = event.pos
                coor_y = math.floor(x / self.sizeofcell)
                coor_x = math.floor(y / self.sizeofcell)
                if coor_y < 8 and coor_x < 8:
                    if self.boardmatrix[coor_x][coor_y] == self.turn:
                        self.status = 1
                        self.ori_y = math.floor(x / self.sizeofcell)
                        self.ori_x = math.floor(y / self.sizeofcell)
                else:
                    continue
            #玩家選擇白棋移動位置
            elif event.type == pygame.MOUSEBUTTONDOWN and self.status == 1:
                x, y = event.pos
                select_y = math.floor(x / self.sizeofcell)
                select_x =math.floor(y / self.sizeofcell)
                if select_y < 8 and select_x < 8:
                    self.new_y = select_y
                    self.new_x = select_x
                    
                    #判斷移動是否合理
                    if self.isabletomove():
                        self.movechess()
                        
                        if (self.new_x == 7 and self.boardmatrix[self.new_x][self.new_y] == 1) \
                            or (self.new_x == 0 and self.boardmatrix[self.new_x][self.new_y] == 2):
                            self.status = 3
                    #允許玩家另選棋子
                    elif self.boardmatrix[self.new_x][self.new_y] == self.boardmatrix[self.ori_x][self.ori_y]:

                        self.ori_x = self.new_x
                        self.ori_y = self.new_y
                else:
                    continue
                
            
        self.display()
        pygame.display.flip()

    #導入介面照片和圖示
    def initgraphics(self):
        self.board = pygame.image.load_extended(os.path.join('picture','chess_board.png'))
        self.board = pygame.transform.scale(self.board, (560, 560))
        self.blackchess = pygame.image.load_extended(os.path.join('picture','black.png'))
        self.blackchess = pygame.transform.scale(self.blackchess, (self.sizeofcell- 20, self.sizeofcell - 20))
        self.whitechess = pygame.image.load_extended(os.path.join('picture','white.png'))
        self.whitechess = pygame.transform.scale(self.whitechess, (self.sizeofcell - 20, self.sizeofcell - 20))
        self.outline = pygame.image.load_extended(os.path.join('picture','outline.png'))
        self.outline = pygame.transform.scale(self.outline, (self.sizeofcell, self.sizeofcell))
        self.reset = pygame.image.load_extended(os.path.join('picture','reset.png'))
        self.reset = pygame.transform.scale(self.reset, (80, 80))
        self.winner = pygame.image.load_extended(os.path.join('picture','finish.png'))
        self.winner = pygame.transform.scale(self.winner, (250, 250))
        self.computer = pygame.image.load_extended(os.path.join('picture','computer.png'))
        self.computer = pygame.transform.scale(self.computer, (80, 80))
        self.auto = pygame.image.load_extended(os.path.join('picture','auto_play.jpg'))
        self.auto = pygame.transform.scale(self.auto, (80, 80))

    #將畫面顯示在介面上
    def display(self):
        self.screen.blit(self.board, (0, 0))
        self.screen.blit(self.reset, (590, 50))
        self.screen.blit(self.computer, (590, 200))
        self.screen.blit(self.auto, (590, 340))
        for i in range(8):
            for j in range(8):
                if self.boardmatrix[i][j] == 1:
                    self.screen.blit(self.blackchess, (self.sizeofcell * j +10, self.sizeofcell * i + 10))
                elif self.boardmatrix[i][j] == 2:
                    self.screen.blit(self.whitechess, (self.sizeofcell * j + 10, self.sizeofcell * i + 10))
        
        #顯示玩家選擇白棋移動位置時的黑框
        if self.status == 1:
            if self.boardmatrix[self.ori_x][self.ori_y] == 1:
                x1 = self.ori_x + 1
                y1 = self.ori_y - 1
                x2 = self.ori_x + 1
                y2 = self.ori_y + 1
                x3 = self.ori_x + 1
                y3 = self.ori_y

                if y1 >= 0 and self.boardmatrix[x1][y1] != 1:
                    self.screen.blit(self.outline,
                                     (self.sizeofcell * y1, self.sizeofcell * x1))
                if y2 <= 7 and self.boardmatrix[x2][y2] != 1:
                    self.screen.blit(self.outline,
                                     (self.sizeofcell * y2, self.sizeofcell * x2))
                if x3 <= 7 and self.boardmatrix[x3][y3] == 0:
                    self.screen.blit(self.outline,
                                     (self.sizeofcell * y3, self.sizeofcell * x3))

            if self.boardmatrix[self.ori_x][self.ori_y] == 2:
                x1 = self.ori_x - 1
                y1 = self.ori_y - 1
                x2 = self.ori_x - 1
                y2 = self.ori_y + 1
                x3 = self.ori_x - 1
                y3 = self.ori_y
                # left up
                if y1 >= 0 and self.boardmatrix[x1][y1] != 2:
                    self.screen.blit(self.outline,
                                     (self.sizeofcell * y1, self.sizeofcell * x1))
                # right up
                if y2 <= 7 and self.boardmatrix[x2][y2] != 2:
                    self.screen.blit(self.outline,
                                     (self.sizeofcell * y2, self.sizeofcell * x2))
                # up
                if x3 >= 0 and self.boardmatrix[x3][y3] == 0:
                    self.screen.blit(self.outline,
                                     (self.sizeofcell * y3, self.sizeofcell * x3))
        global ori_pos
        global new_pos
        #顯示電腦移動時的棋子前後位置黑框
        if self.auto_choose or self.status == 5:
            
            if (ori_pos != 0 and self.status != 1 and self.turn != 1) or (ori_pos != 0 and self.status == 5):
                # print("display ori_pos: ", ori_pos)
                # print("display new_pos: ", new_pos)
                self.screen.blit(self.outline,
                                  (self.sizeofcell * ori_pos[1], self.sizeofcell * ori_pos[0]))
                self.screen.blit(self.outline,
                                  (self.sizeofcell * new_pos[1], self.sizeofcell * new_pos[0]))
        if self.status == 3:
            self.screen.blit(self.winner, (150, 150))

    def movechess(self):
        self.boardmatrix[self.new_x][self.new_y] = self.boardmatrix[self.ori_x][self.ori_y]
        self.boardmatrix[self.ori_x][self.ori_y] = 0
        if self.turn == 1:
            self.turn = 2
        elif self.turn == 2:
            self.turn = 1
        self.status = 0

    def isreset(self, pos):
        x, y = pos
        if 670 >= x >= 590 and 50 <= y <= 130:
            return True
        return False

    def iscomputer(self, pos):
        x, y = pos
        if 590 <= x <= 670 and 200 <= y <= 280:
            return True
        return False

    def isauto(self, pos):
        x, y = pos
        if 590 <= x <= 670 and 340 <= y <= 420:
            return True
        return False

    #判斷移動是否合法
    def isabletomove(self):
        if (self.boardmatrix[self.ori_x][self.ori_y] == 1
            and self.boardmatrix[self.new_x][self.new_y] != 1
            and self.new_x - self.ori_x == 1
            and self.ori_y - 1 <= self.new_y <= self.ori_y + 1
            and not (self.ori_y == self.new_y and self.boardmatrix[self.new_x][self.new_y] == 2)) \
            or (self.boardmatrix[self.ori_x][self.ori_y] == 2
                and self.boardmatrix[self.new_x][self.new_y] != 2
                and self.ori_x - self.new_x == 1
                and self.ori_y - 1 <= self.new_y <= self.ori_y + 1
                and not (self.ori_y == self.new_y and self.boardmatrix[self.new_x][self.new_y] == 1)):
            return 1
        return 0
    #電腦移動並傳入演算法，並判斷盤面狀態
    def ai_move_alphabeta(self, function_type):
        board, piece = AlphaBetaAgent(self.boardmatrix, self.turn, 5, function_type).alpha_beta_decision()
        self.boardmatrix = board.getMatrix()
        if self.turn == 1:
            self.turn = 2
        elif self.turn == 2:
            self.turn = 1
        if self.isgoalstate():
            self.status = 3
            
    #判斷玩家與電腦對戰時雙方是否滿足勝利條件
    def isgoalstate(self, base=0):
        if base == 0:
            if 2 in self.boardmatrix[0] or 1 in self.boardmatrix[7]:
                return True
            else:
                for line in self.boardmatrix:
                    if 1 in line or 2 in line:
                        return False
            return True
        else:
            count = 0
            for i in self.boardmatrix[0]:
                if i == 2:
                    count += 1
            if count == 3:
                return True
            count = 0
            for i in self.boardmatrix[7]:
                if i == 1:
                    count += 1
            if count == 3:
                return True
            count1 = 0
            count2 = 0
            for line in self.boardmatrix:
                for i in line:
                    if i == 1:
                        count1 += 1
                    elif i == 2:
                        count2 += 1
            if count1 <= 2 or count2 <= 2:
                return True
        return False
    
#電腦移動演算法
class AlphaBetaAgent:
    def __init__(self, boardmatrix, turn, depth, function):
        self.boardmatrix = boardmatrix
        self.turn = turn
        self.maxdepth = depth
        self.function = function

        self.piece_num = 0
        

    def max_value(self, state, alpha, beta, depth):
        if depth == self.maxdepth or state.isgoalstate() != 0:
            return state.utility(self.turn)
        v = MINNUM
        actions = state.available_actions()

        actions = sorted(state.available_actions(), key=lambda action: 0, reverse=True)


        for action in actions:

            v = max(v, self.min_value(state.transfer(action), alpha, beta, depth + 1))
            if v >= beta:
                return v
            alpha = max(alpha, v)
        return v

    def min_value(self, state, alpha, beta, depth):
        if depth == self.maxdepth or state.isgoalstate() != 0:
            return state.utility(self.turn)
        v = MAXNUM
        actions = state.available_actions()

        actions = sorted(state.available_actions(), key=lambda action: 0)

        for action in actions:

            v = min(v, self.max_value(state.transfer(action), alpha, beta, depth + 1))
            if v <= alpha:
                return v
            beta = min(beta, v)
        return v
    
    #電腦決定移動位置
    def alpha_beta_decision(self):
        final_action = None
        initialstate = State(boardmatrix=self.boardmatrix, turn=self.turn, function=self.function)
        v = MINNUM
        for action in initialstate.available_actions():

            new_state = initialstate.transfer(action)
            if new_state.isgoalstate():
                final_action = action
                break
            minresult = self.min_value(new_state, MINNUM, MAXNUM, 1)
            if minresult > v:
                final_action = action
                v = minresult
        if self.turn == 1:
            self.piece_num = initialstate.transfer(final_action).white_num
        elif self.turn == 2:
            self.piece_num = initialstate.transfer(final_action).black_num
        #print(final_action.getaction())
        
        global ori_pos
        global new_pos
        ori_pos = final_action.coordinate
        new_pos = single_move(final_action.coordinate, final_action.direction, final_action.turn)
        # print("ori pos:", ori_pos)
        # print("new_pos:", new_pos)
        return initialstate.transfer(final_action), self.piece_num
    
#記錄盤面狀態並計算期望值
class State:
    def __init__(self,
                 boardmatrix=None,
                 black_position=None,
                 white_position=None,
                 black_num=0,
                 white_num=0,
                 turn=1,
                 function=0,
                 width=8,
                 height=8):
        self.width = width
        self.height = height
        if black_position is None:
            self.black_positions = []
        else:
            self.black_positions = black_position
        if white_position is None:
            self.white_positions = []
        else:
            self.white_positions = white_position
        self.black_num = black_num
        self.white_num = white_num
        self.turn = turn
        self.function = function
        if boardmatrix is not None:
            # self.wide = len(boardmatrix[0])
            # self.height = len(boardmatrix)
            for i in range(self.height):
                for j in range(self.width):
                    if boardmatrix[i][j] == 1:
                        self.black_positions.append((i, j))
                        self.black_num += 1
                    if boardmatrix[i][j] == 2:
                        self.white_positions.append((i, j))
                        self.white_num += 1

    #盤面棋子移動
    def transfer(self, action):
        black_pos = list(self.black_positions)
        white_pos = list(self.white_positions)

        #黑棋
        if action.turn == 1:
            if action.coordinate in self.black_positions:
                index = black_pos.index(action.coordinate)
                new_pos = single_move(action.coordinate, action.direction, action.turn)
                black_pos[index] = new_pos
                if new_pos in self.white_positions:
                    white_pos.remove(new_pos)
            else:
                print("Invalid action!")

        #白棋
        elif action.turn == 2:
            if action.coordinate in self.white_positions:
                index = white_pos.index(action.coordinate)
                new_pos = single_move(action.coordinate, action.direction, action.turn)
                white_pos[index] = new_pos
                if new_pos in self.black_positions:
                    black_pos.remove(new_pos)
            else:
                print("Invalid action!")

        state = State(black_position=black_pos, white_position=white_pos, black_num=self.black_num, white_num=self.white_num, turn=alterturn(action.turn), function=self.function, height=self.height, width=self.width)
        return state
    
    #記錄電腦移動後盤面可能的狀況
    def available_actions(self):
        available_actions = []
        if self.turn == 1:
            for pos in sorted(self.black_positions, key=lambda p: (p[0], -p[1]), reverse=True):

                if pos[0] != self.height - 1 and pos[1] != 0 and (pos[0] + 1, pos[1] - 1) not in self.black_positions:
                    available_actions.append(Action(pos, 1, 1))
                if pos[0] != self.height - 1 and (pos[0] + 1, pos[1]) not in self.black_positions and (pos[0] + 1, pos[1]) not in self.white_positions:
                    available_actions.append(Action(pos, 2, 1))
                if pos[0] != self.height - 1 and pos[1] != self.width - 1 and (pos[0] + 1, pos[1] + 1) not in self.black_positions:
                    available_actions.append(Action(pos, 3, 1))

        elif self.turn == 2:
            for pos in sorted(self.white_positions, key=lambda p: (p[0], p[1])):

                if pos[0] != 0 and pos[1] != 0 and (pos[0] - 1, pos[1] - 1) not in self.white_positions:
                    available_actions.append(Action(pos, 1, 2))
                if pos[0] != 0 and (pos[0] - 1, pos[1]) not in self.black_positions and (pos[0] - 1, pos[1]) not in self.white_positions:
                    available_actions.append(Action(pos, 2, 2))
                if pos[0] != 0 and pos[1] != self.width - 1 and (pos[0] - 1, pos[1] + 1) not in self.white_positions:
                    available_actions.append(Action(pos, 3, 2))

        return available_actions

    def getMatrix(self):
        matrix = [[0 for _ in range(self.width)] for _ in range(self.height)]
        for item in self.black_positions:
            matrix[item[0]][item[1]] = 1
        for item in self.white_positions:
            matrix[item[0]][item[1]] = 2
        return matrix
    
    #電腦與電腦對戰選擇模式
    def utility(self, turn):
        if self.function == 0:
            return 0
        elif self.function == 1:
            return self.offensive_function(turn)
        elif self.function == 2:
            return self.defensive_function(turn)
        
    #將200訂為獲勝的期望值，並在電腦對戰時給予雙方正負不同的回傳值
    def winningscore(self, turn):
        winningvalue = 200
        if turn == 1:
            if self.isgoalstate() == 1:
                return winningvalue
            elif self.isgoalstate() == 2:
                return -winningvalue
            else:
                return 0
        elif turn == 2:
            if self.isgoalstate() == 2:
                return winningvalue
            elif self.isgoalstate() == 1:
                return -winningvalue
            else:
                return 0
    #判斷電腦與電腦對戰時雙方是否滿足勝利條件
    def isgoalstate(self, type=0):
        if type == 0:
            if 0 in [item[0] for item in self.white_positions] or len(self.black_positions) == 0:
                return 2
            if self.height - 1 in [item[0] for item in self.black_positions] or len(self.white_positions) == 0:
                return 1
            return 0
        else:
            count = 0
            for i in self.black_positions:
                if i[0] == 7:
                    count += 1
            if count == 3:
                return True
            count = 0
            for i in self.white_positions:
                if i[0] == 0:
                    count += 1
            if count == 3:
                return True
            if len(self.black_positions) <= 2 or len(self.white_positions) <= 2:
                return True
        return False
    
    #以盤面尚留存的棋子數以及棋子所在位置計算我方目前狀態的期望值，越靠近對方邊界期望值越高
    def myscore(self, turn):
        if turn == 1:
            return len(self.black_positions) \
                   + sum(pos[0] for pos in self.black_positions) + self.winningscore(turn)

        elif turn == 2:
            return len(self.white_positions) \
                   + sum(7 - pos[0] for pos in self.white_positions) + self.winningscore(turn)


    #以盤面尚留存的棋子數以及棋子所在位置計算對手目前狀態的期望值，越靠近對方邊界期望值越高
    def enemyscore(self, turn):
        if turn == 1:
            return len(self.white_positions) \
                   + sum(7 - pos[0] for pos in self.white_positions) + self.winningscore(2)
                   #+ max(7 - pos[0] for pos in self.white_positions)\

        elif turn == 2:
            return len(self.black_positions) \
                   + sum(pos[0] for pos in self.black_positions) + self.winningscore(1)
                   #+ max(pos[0] for pos in self.black_positions) \

    #電腦1
    def offensive_function(self, turn):
        return 2 * self.myscore(turn) - 1 * self.enemyscore(turn)
    #電腦2
    def defensive_function(self, turn):
        return 1 * self.myscore(turn) - 2 * self.enemyscore(turn)

   

def main():
    game = BreakthroughGame()
    while 1:
        game.run()


if __name__ == '__main__':
    main()

