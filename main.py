from easyansi import cursor, screen
import getkey
# from time import sleep

WIN_POS = cursor.get_location()


def clear(n_lines: int):
    """
    Clear some number of lines.
    """
    for r in range(n_lines+1):
        screen.clear_line(WIN_POS[1] + r)


def draw_game(game_status) -> tuple:
    """
    Mostra o tabuleiro do jogo.
    """
    print('\033[7m   0   1   2\n \033[m')
    cords = 0
    for line in game_status:
        print(f'\033[7m{cords}\033[m  {line[0]} | {line[1]} | {line[2]}')
        if cords < 2:
            print('\033[7m \033[m ' + '-'*11)
        cords += 1


def draw_menu(menu_opts) -> int:
    """
    Função que desenha na tela um menu

    :param menu_opts: Lista ou tupla contendo as opções
    :return: o index da opção selecionada
    """
    selected = 0
    cursor.hide()
    while True:
        cursor.locate(WIN_POS[0], WIN_POS[1])
        for opt in menu_opts:
            if selected == menu_opts.index(opt):
                print('\033[7m', end='')
            print(opt + '\033[m')
        key = getkey.getkey()

        clear(len(menu_opts))

        if key == getkey.keys.UP and selected > 0:
            selected -= 1
        elif key == getkey.keys.DOWN and selected < len(menu_opts)-1:
            selected += 1
        elif key == getkey.keys.ENTER:
            break
    cursor.show()
    return selected


main_menu = ('New', 'Quit')
opt = draw_menu(main_menu)

# Exit Game
if opt == 1:
    exit()

game_end = False
default_pos = (WIN_POS[0]+3, WIN_POS[1]+2)
selection = [0, 0]
player = True
cursor.show()

game_status = [
    [' ', ' ', ' '],
    [' ', ' ', ' '],
    [' ', ' ', ' ']
]
last_pos = default_pos
while not game_end:
    cursor.locate(WIN_POS[0], WIN_POS[1])
    draw_game(game_status)
    print(f'\n\033[32mEstá na vez do jogador {int(player)+1}\033[m')
    cursor.locate(last_pos[0], last_pos[1])

    while True:
        key = getkey.getkey()
        if key == getkey.keys.UP and selection[1] > 0:
            selection[1] -= 1
        elif key == getkey.keys.DOWN and selection[1] < 2:
            selection[1] += 1
        elif key == getkey.keys.LEFT and selection[0] > 0:
            selection[0] -= 1
        elif key == getkey.keys.RIGHT and selection[0] < 2:
            selection[0] += 1
        elif (
            key == getkey.keys.ENTER and
            game_status[selection[1]][selection[0]] == ' '
        ):
            game_status[selection[1]][selection[0]] = 'O' if player else 'X'
            break

        cursor.locate(
            default_pos[0] + selection[0] * 4,
            default_pos[1] + selection[1] * 2
        )
    player = not player
    last_pos = cursor.get_location()
