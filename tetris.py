#!/usr/bin/env python3
import curses
import time
import board


# Initialize parameters
BOARD_WIDTH = 10
BOARD_HEIGHT = 17


GAME_WINDOW_WIDTH = 2 * BOARD_WIDTH + 2
GAME_WINDOW_HEIGHT = BOARD_HEIGHT + 2


STATUS_WINDOW_HEIGHT = 12
STATUS_WINDOW_WIDTH = 30

BLOCK_SYMBOL = "  "


def init_colors():
    """Init colors"""

    curses.init_pair(99, 8, curses.COLOR_BLACK)  # 1 - grey
    curses.init_pair(98, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(97, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(96, curses.COLOR_BLACK, curses.COLOR_CYAN)
    curses.init_pair(95, curses.COLOR_BLACK, curses.COLOR_WHITE)

    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_BLUE)
    curses.init_pair(2, curses.COLOR_BLACK, 13)  # 13 - pink
    curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_YELLOW)
    curses.init_pair(4, curses.COLOR_BLACK, curses.COLOR_GREEN)
    curses.init_pair(5, curses.COLOR_BLACK, curses.COLOR_MAGENTA)
    curses.init_pair(6, curses.COLOR_BLACK, curses.COLOR_WHITE)


def init_game_window():
    """Create and return game window"""

    window = curses.newwin(GAME_WINDOW_HEIGHT, GAME_WINDOW_WIDTH, 0, 0)
    window.nodelay(True)
    window.keypad(1)
    return window


def init_status_window():
    """Create and return status window"""

    window = curses.newwin(STATUS_WINDOW_HEIGHT, STATUS_WINDOW_WIDTH, 0,
                           GAME_WINDOW_WIDTH)
    return window


def draw_game_window(window):
    """Draw game window"""
    '''
    3 steps create the game window:
        1. Drawing the board with its net and its finished blocks.
        2. Find the position of the current dropping posistion and draw it.
        3. Check the status of the game(Game Over or Pause) to draw
        appropriate title
    '''
    window.border()

    # draw board
    '''
    The board is a matrix which contains 0 and 1.
    The position with value = 1 is the position is built IN FINISH by blocks.
    '''
    for a in range(BOARD_HEIGHT):
        for b in range(BOARD_WIDTH):
            if game_board.board[a][b] == 1:
                window.addstr(a + 1, 2 * b + 1, BLOCK_SYMBOL,
                              curses.color_pair(96))
            else:
                # draw net
                window.addstr(a + 1, 2 * b + 1, " .", curses.color_pair(99))

    # draw current block
    for a in range(game_board.current_block.size()[0]):
        for b in range(game_board.current_block.size()[1]):
            if game_board.current_block.shape[a][b] == 1:
                x = 2 * game_board.current_block_pos[1] + 2 * b + 1
                y = game_board.current_block_pos[0] + a + 1
                window.addstr(y, x, BLOCK_SYMBOL, curses.color_pair(
                              game_board.current_block.color))

    if game_board.is_game_over():
        go_title = " Game Over "
        ag_title = " Enter - play again "

        window.addstr(int(GAME_WINDOW_HEIGHT*.4),
                         (GAME_WINDOW_WIDTH-len(go_title))//2,
                      go_title, curses.color_pair(95))
        window.addstr(int(GAME_WINDOW_HEIGHT*.5),
                         (GAME_WINDOW_WIDTH-len(ag_title))//2,
                      ag_title, curses.color_pair(95))

    if pause:
        p_title = " Pause "
        window.addstr(int(GAME_WINDOW_HEIGHT * .4),
                         (GAME_WINDOW_WIDTH - len(p_title)) // 2,
                      p_title, curses.color_pair(95))

    window.refresh()


def init_status_window():
    """Create and return status window"""

    window = curses.newwin(STATUS_WINDOW_HEIGHT, STATUS_WINDOW_WIDTH, 0,
                           GAME_WINDOW_WIDTH)
    return window


def draw_status_window(window):
    """Draw status window"""

    if game_board.is_game_over():
        return

    # Initialize status window with empty space
    for row in range(1, STATUS_WINDOW_HEIGHT - 1):
        window.addstr(row, 2, (STATUS_WINDOW_WIDTH - 3)*" ")
    window.border()
    window.addstr(1, int(STATUS_WINDOW_WIDTH*.3),
                  "Score: {}".format(game_board.score))
    window.addstr(2, int(STATUS_WINDOW_WIDTH*.3),
                  "Level: {}".format(game_board.level))
    # SCREEN_H, SCREEN_W = scr.getmaxyx()
    # if SCREEN_H <= GAME_WINDOW_HEIGHT + GAME_WINDOW_HEIGHT // 2 or \
    #    SCREEN_W <= GAME_WINDOW_WIDTH * 2:
    window.addstr(3, int(STATUS_WINDOW_WIDTH*.3), "HAPPY BIRTHDAY NAM !")
    window.addstr(4, int(STATUS_WINDOW_WIDTH*.05), "🎂"*20)
    if game_board.score == 1:
        window.addstr(5, int(STATUS_WINDOW_WIDTH*.3), 'DUNG GIAM CAN MA !!')

    # Show the next board at the middle of the status win.
    start_col = int(STATUS_WINDOW_WIDTH / 2 - game_board.next_block.size()[1])
    # Color the next block
    for row in range(game_board.next_block.size()[0]):
        for col in range(game_board.next_block.size()[1]):
            if game_board.next_block.shape[row][col] == 1:
                window.addstr(6 + row, start_col + 2 * col, BLOCK_SYMBOL,
                              curses.color_pair(game_board.next_block.color))

    window.refresh()


pause = False

game_board = board.Board(BOARD_HEIGHT, BOARD_WIDTH)
game_board.start()

old_score = game_board.score

if __name__ == "__main__":
    try:
        scr = curses.initscr()
        curses.noecho()
        curses.cbreak()
        curses.start_color()
        curses.curs_set(0)

        init_colors()

        game_window = init_game_window()
        status_window = init_status_window()

        draw_game_window(game_window)
        draw_status_window(status_window)

        start = time.time()

        quit_game = False
        while not quit_game:
            key_event = game_window.getch()
            draw_status_window(status_window)
            # hack: redraw it on resize
            if key_event == curses.KEY_RESIZE:
                SCREEN_H, SCREEN_W = scr.getmaxyx()
                if SCREEN_H <= GAME_WINDOW_HEIGHT \
                        or SCREEN_W <= GAME_WINDOW_WIDTH:
                    quit_game = True
                game_window.clear()
                draw_game_window(game_window)

            if key_event == ord("q"):
                quit_game = True

            if not game_board.is_game_over():
                if not pause:
                    # Configuring delay speed
                    if time.time() - start >= 1 / game_board.level:
                        game_board.move_block("down")
                        start = time.time()

                    if key_event == curses.KEY_UP:
                        game_board.rotate_block()
                    elif key_event == curses.KEY_DOWN:
                        game_board.move_block("down")
                    elif key_event == curses.KEY_LEFT:
                        game_board.move_block("left")
                    elif key_event == curses.KEY_RIGHT:
                        game_board.move_block("right")
                    elif key_event == ord(" "):
                        game_board.drop()
                if key_event == ord("p"):
                    pause = not pause
                    game_window.nodelay(True)
            else:
                game_window.nodelay(False)
                if key_event == ord("\n"):
                    game_board.start()
                    game_window.nodelay(True)

            draw_game_window(game_window)

            if old_score != game_board.score:
                draw_status_window(status_window)
                old_score = game_board.score
    finally:
        curses.endwin()
