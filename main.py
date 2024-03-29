import random
import time
import turtle
from copy import deepcopy

class OthelloUI:
    def __init__(self, board_size=6, square_size=60):
        self.board_size = board_size
        self.square_size = square_size
        self.screen = turtle.Screen()
        self.screen.setup(self.board_size * self.square_size + 50, self.board_size * self.square_size + 50)
        self.screen.bgcolor('white')
        self.screen.title('Othello')
        self.pen = turtle.Turtle()
        self.pen.hideturtle()
        self.pen.speed(0)
        turtle.tracer(0, 0)

    def draw_board(self, board):
        self.pen.penup()
        x, y = -self.board_size / 2 * self.square_size, self.board_size / 2 * self.square_size
        for i in range(self.board_size):
            self.pen.penup()
            for j in range(self.board_size):
                self.pen.goto(x + j * self.square_size, y - i * self.square_size)
                self.pen.pendown()
                self.pen.fillcolor('green')
                self.pen.begin_fill()
                self.pen.setheading(0)
                for _ in range(4):
                    self.pen.forward(self.square_size)
                    self.pen.right(90)
                self.pen.penup()
                self.pen.end_fill()
                self.pen.goto(x + j * self.square_size + self.square_size / 2,
                              y - i * self.square_size - self.square_size + 5)
                if board[i][j] == 1:
                    self.pen.fillcolor('white')
                    self.pen.begin_fill()
                    self.pen.circle(self.square_size / 2 - 5)
                    self.pen.end_fill()
                elif board[i][j] == -1:
                    self.pen.fillcolor('black')
                    self.pen.begin_fill()
                    self.pen.circle(self.square_size / 2 - 5)
                    self.pen.end_fill()

        turtle.update()


class Othello:
    def __init__(self, ui, minimax_depth=1, prune=True):
        self.size = 6
        self.ui = OthelloUI(self.size) if ui else None
        self.board = [[0 for _ in range(self.size)] for _ in range(self.size)]
        self.board[int(self.size / 2) - 1][int(self.size / 2) - 1] = self.board[int(self.size / 2)][
            int(self.size / 2)] = 1
        self.board[int(self.size / 2) - 1][int(self.size / 2)] = self.board[int(self.size / 2)][
            int(self.size / 2) - 1] = -1
        self.current_turn = random.choice([1, -1])
        self.minimax_depth = minimax_depth
        self.prune = prune
        self.number_of_seen_nodes = 0

    def get_winner(self):
        white_count = sum([row.count(1) for row in self.board])
        black_count = sum([row.count(-1) for row in self.board])
        if white_count > black_count:
            return 1
        elif white_count < black_count:
            return -1
        else:
            return 0

    def get_valid_moves(self, player):
        moves = set()
        for i in range(self.size):
            for j in range(self.size):
                if self.board[i][j] == 0:
                    for di in [-1, 0, 1]:
                        for dj in [-1, 0, 1]:
                            if di == 0 and dj == 0:
                                continue
                            x, y = i, j
                            captured = []
                            start_time = time.time()
                            while 0 <= x + di < self.size and 0 <= y + dj < self.size and self.board[x + di][
                                    y + dj] == -player:
                                captured.append((x + di, y + dj))
                                x += di
                                y += dj
                            if 0 <= x + di < self.size and 0 <= y + dj < self.size and self.board[x + di][
                                    y + dj] == player and len(captured) > 0:
                                moves.add((i, j))
        return list(moves)

    def make_move(self, player, move):
        i, j = move
        self.board[i][j] = player
        for di in [-1, 0, 1]:
            for dj in [-1, 0, 1]:
                if di == 0 and dj == 0:
                    continue
                x, y = i, j
                captured = []
                while 0 <= x + di < self.size and 0 <= y + dj < self.size and self.board[x + di][y + dj] == -player:
                    captured.append((x + di, y + dj))
                    x += di
                    y += dj
                if 0 <= x + di < self.size and 0 <= y + dj < self.size and self.board[x + di][y + dj] == player:
                    for (cx, cy) in captured:
                        self.board[cx][cy] = player

    def get_cpu_move(self):
        moves = self.get_valid_moves(-1)
        if len(moves) == 0:
            return None
        return random.choice(moves)


    def alpha_beta_minimax(self, depth, player, alpha, beta):
        if depth == 0 or self.terminal_test():
            return self.evaluate(player)
        if player == -1:
            best_score = float('inf')
            for move in self.get_valid_moves(player):
                temp_board = deepcopy(self.board)
                self.make_move(player, move)
                score = self.alpha_beta_minimax(depth - 1, 1, alpha, beta)
                self.board = deepcopy(temp_board)
                best_score = min(best_score, score)
                beta = min(beta, score)
                if alpha >= beta:
                    break
            return best_score
        else:
            best_score = float('-inf')
            for move in self.get_valid_moves(player):
                board_copy = [row[:] for row in self.board]
                self.make_move(player, move)
                score = self.alpha_beta_minimax(depth - 1, -1, alpha, beta)
                self.board = board_copy
                best_score = max(best_score, score)
                alpha = max(alpha, score)
                if alpha >= beta:
                    break
            return best_score

        
    def get_human_move(self):
        moves = self.get_valid_moves(1)
        if len(moves) == 0:
            return None
        best_move = None
        best_score = float('-inf')
        for move in moves:
            temp_board = deepcopy(self.board)
            self.make_move(1, move)
            score = self.alpha_beta_minimax(self.minimax_depth-1, -1, float('-inf'), float('inf'))
            self.board = deepcopy(temp_board)
            if score > best_score:
                best_move = move
                best_score = score
        return best_move

    def evaluate(self, player):
        score = 0
        score += sum([row.count(player) for row in self.board])
        return score
        
    def terminal_test(self):
        return len(self.get_valid_moves(1)) == 0 and len(self.get_valid_moves(-1)) == 0

    def play(self):
        start_time = time.time()
        winner = None
        while not self.terminal_test():
            if time.time() - start_time > 8:
                return (0,0,0)
            if self.ui:
                self.ui.draw_board(self.board)
            if self.current_turn == 1:
                move = self.get_human_move()
                if move:
                    self.make_move(self.current_turn, move)
            else:
                move = self.get_cpu_move()
                if move:
                    self.make_move(self.current_turn, move)
            self.current_turn = -self.current_turn
            if self.ui:
                self.ui.draw_board(self.board)
                time.sleep(1)
        winner = self.get_winner()
        end_time = time.time()
        execution_time = end_time - start_time
        return winner, execution_time, self.number_of_seen_nodes