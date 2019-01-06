import math
import random
import os


block_shapes = [
    # N Block
    [[1, 1, 0, 1],
     [1, 0, 1, 1]],
    # A Block
    [[0, 1, 0],
     [1, 0, 1],
     [1, 1, 1],
     [1, 0, 1]],
    # M Block
    [[1, 1, 0, 1, 1],
     [1, 0, 1, 0, 1]],
    # small O Block
    [[1]]
]


class Board:
    """Board representation"""

    def __init__(self, height, width):
        self.height = height
        self.width = width
        self.board = self._get_new_board()

        self.current_block_pos = None
        self.current_block = None
        self.next_block = None

        self.game_over = False
        self.score = None
        self.level = None

    def start(self):
        """Start game"""

        self.board = self._get_new_board()

        self.current_block_pos = None
        self.current_block = None
        self.next_block = None

        self.game_over = False
        self.score = 0
        self.level = 1

        self._place_new_block()

    def _get_new_board(self):
        """Create new empty board"""

        return [[0 for _ in range(self.width)] for _ in range(self.height)]

    def _place_new_block(self):
        """Place new block and generate the next one"""

        if self.next_block is None:
            self.current_block = self._get_new_block()
            self.next_block = self._get_new_block()
        else:
            self.current_block = self.next_block
            self.next_block = self._get_new_block()

        size = Block.get_size(self.current_block.shape)
        col_pos = math.floor((self.width - size[1]) / 2)
        self.current_block_pos = [0, col_pos]

        if self._check_overlapping(self.current_block_pos,
                                   self.current_block.shape):
            self.game_over = True

    def _check_overlapping(self, pos, shape):
        """If current block overlaps any other on the board"""
        '''
        size[0]: height of the block
        size[1]: width of the block
        '''
        size = Block.get_size(shape)
        for row in range(size[0]):
            for col in range(size[1]):
                if shape[row][col] == 1:
                    if self.board[pos[0] + row][pos[1] + col] == 1:
                        return True
        return False

    def _can_move(self, pos, shape):
        """Check if move is possible"""
        '''
        pos[0]: y coordinate
        pos[1]: x coordinate
        2 steps:
            1. Comparing the block with the board.
            2. Comparing the block with the current landed blocks.
        '''
        size = Block.get_size(shape)
        if pos[1] < 0 or pos[1] + size[1] > self.width \
                or pos[0] + size[0] > self.height:
            return False

        return not self._check_overlapping(pos, shape)

    def _burn(self):
        """Remove matched lines"""

        for row in range(self.height):
            if all(col != 0 for col in self.board[row]):
                for r in range(row, 0, -1):
                    self.board[r] = self.board[r - 1]
                self.board[0] = [0 for _ in range(self.width)]
                self.score += 1
                if self.score % 5 == 0:
                    self.level += 1

    def _land_block(self):
        """Put block to the board and generate a new one"""

        size = Block.get_size(self.current_block.shape)
        for row in range(size[0]):
            for col in range(size[1]):
                if self.current_block.shape[row][col] == 1:
                    current_block_x = self.current_block_pos[1]
                    current_block_y = self.current_block_pos[0]
                    self.board[current_block_y + row][
                               current_block_x + col] = 1

    def drop(self):
        """Move to very very bottom"""

        while self._can_move((self.current_block_pos[0] + 1,
                             self.current_block_pos[1]),
                             self.current_block.shape):
            self.move_block("down")

        self._land_block()
        self._burn()
        self._place_new_block()

    def is_game_over(self):
        """Is game over"""

        return self.game_over

    def rotate_block(self):
        rotated_shape = list(map(list, zip(*self.current_block.shape[::-1])))

        if self._can_move(self.current_block_pos, rotated_shape):
            self.current_block.shape = rotated_shape

    def move_block(self, direction):
        """Try to move block"""

        pos = self.current_block_pos
        if direction == "left":
            new_pos = [pos[0], pos[1] - 1]
        elif direction == "right":
            new_pos = [pos[0], pos[1] + 1]
        elif direction == "down":
            new_pos = [pos[0] + 1, pos[1]]

        if self._can_move(new_pos, self.current_block.shape):
            self.current_block_pos = new_pos
        elif direction == "down":
            self._land_block()
            self._burn()
            self._place_new_block()

    @staticmethod
    def _get_new_block():
        """Get random block"""

        block = Block(random.randint(0, len(block_shapes) - 1))

        return block


class Block:
    """Block representation"""

    def __init__(self, block_type):
        self.shape = block_shapes[block_type]
        self.color = block_type + 1

    def size(self):
        """Get size of the block"""

        return self.get_size(self.shape)

    @staticmethod
    def get_size(shape):
        """Get size of a shape"""

        return [len(shape), len(shape[0])]
