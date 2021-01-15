from easyansi import cursor, screen
import getkey

DEFAULT_POS = cursor.get_location()


def clear(n_lines: int):
    """
    Clear some number of lines.
    """
    for r in range(n_lines+1):
        screen.clear_line(DEFAULT_POS[1] + r)


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
        cursor.locate(DEFAULT_POS[0], DEFAULT_POS[1])
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


game_status = [
    [' ', ' ', ' '],
    [' ', ' ', ' '],
    [' ', ' ', ' ']
]

main_menu = ('New', 'Quit')
opt = draw_menu(main_menu)
cursor.locate(DEFAULT_POS[0], DEFAULT_POS[1])
draw_game(game_status)
