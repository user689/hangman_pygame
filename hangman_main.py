import pygame as py
from math import sqrt
from random import sample
import json

py.init()
W, H = 800, 500
win = py.display.set_mode((W, H))
py.display.set_caption('Hangman - Guess The Word')

# load images
images = []
for i in range(7):
    images.append(py.image.load("./hangman/hangman{}.png".format(i)))

# global
fonts = {'letter': py.font.SysFont(
    'Arial', 40), 'word': py.font.SysFont('Arial', 60),
    'end': py.font.SysFont('comicsans', 80),
    'endp': py.font.SysFont('comicsans', 100),
    'button': py.font.SysFont('comicsans', 30)
    }
colors = {'white': (255, 255, 255), 'black': (
        0, 0, 0), 'blue': (151, 146, 227), 'red': (228, 63, 111)}


def get_word(word='', guessed=[], difficulty=1):
    if word == '':
        with open('words.json', 'r') as words:
            data = json.load(words)
            if difficulty == 1:
                word_list = data['6'] + data['7']
            elif difficulty == 2:
                word_list = data['8'] + data['9'] + data['10']
            else:
                word_list = data['11'] + data['12'] + data['13'] + data['14']
            return sample(word_list, 1)[0]
    else:
        temp = ''
        for letter in word:
            if letter in guessed:
                temp += letter + " "
            else:
                temp += "_ "
        return temp


def draw(status, circles, r, outline, word):
    win.fill(colors['white'])
    update_score(total)
    win.blit(images[status], (50, 100))
    for circle in circles:
        x, y, letter, visible = circle
        if visible:
            py.draw.circle(win, colors['black'], (x, y), r, outline)
            text = fonts['letter'].render(letter, 1, colors['black'])
            win.blit(text, (x-text.get_width()/2, y-text.get_height()/2))
    text = fonts['word'].render(word, 1, colors['blue'])
    win.blit(text, (280, 200))


def check_win_loss(word, guessed, hangman_status):
    """
    -1:lost;1: won
    """
    if hangman_status == 6:
        return -1
    for i in word:
        if i not in guessed:
            return False
    return 1

# TODO:  add menu
# TODO:  add more words


def draw_button(color, x, y, w, h, text, active=False):
    button = py.draw.rect(win, colors[color], (x, y, w, h), 0)
    draw_text(text, 'button', 'white', y+h//2,
              x+w//2)
    return button


def draw_text(text, font, color, y=(H//2), x=(W//2)):
    txt = fonts[font].render(text, 1, colors[color])
    txt = win.blit(txt, (x-txt.get_width()//2, y-txt.get_height()//2))
    return txt


def draw_end(game_status, word, difficulty):
    win.fill(colors['white'])
    if game_status == -1:
        draw_text("Game Over!", 'end', 'red', 200)
    else:
        draw_text("Hooray!", 'end', 'red', 100)
        draw_text("You Win", 'endp', 'red', 200)
    button_retry = draw_button('black', W//3 + W//20, H//2+H//20,
                               80, 60, 'Retry')
    button_menu = draw_button('black', W//3 + W//20 + 80*1.5, H//2+H//20,
                              80, 60, 'Menu')
    draw_text("Word was: {}".format(word), 'word', 'blue', 400)
    py.display.update()
    for ev in py.event.get():
        pos = py.mouse.get_pos()
        if ev.type == py.QUIT:
            py.quit()
        elif ev.type == py.MOUSEBUTTONDOWN:
            if ev.button == 1:
                if button_retry.collidepoint(pos):
                    return False, difficulty
                elif button_menu.collidepoint(pos):
                    difficulty = menu()
                    return False, difficulty
    return True, difficulty

    # py.time.delay(4000)


def hint(difficulty, word, guessed, circles, used, pygame_events):
    hints_allowed = (3 - difficulty) % 3
    if (hints_allowed - used) > 0:
        # give hint
        hint_button = draw_text('Hint', 'letter', 'blue', 20, 750)
        for ev in pygame_events:
            pos = py.mouse.get_pos()

            if ev.type == py.MOUSEBUTTONDOWN:
                if hint_button.collidepoint(pos):
                    possible = []
                    for letter in word:
                        if letter not in guessed and letter not in possible:
                            possible.append(letter)
                    hint = sample(possible, 1)[0]
                    for circle in circles:
                        x, y, letter, visible = circle
                        if hint == letter:
                            circle[3] = False
                            guessed.append(letter)
                            used += 1
            else:
                pass
    return guessed, circles, used


def menu():
    global total
    total = -1
    while True:
        win.fill(colors['white'])
        draw_text("Hangman Game", 'endp', 'black', H//5)
        menu_items = ['Easy', 'Medium', 'Hard', 'Quit']
        menu_buttons = []
        for i, item in enumerate(menu_items):
            menu_buttons.append(draw_text(item, 'word', 'blue',
                                          H//4 + 60 + i * 60))
        for ev in py.event.get():
            if ev.type == py.QUIT:
                py.quit()
            elif ev.type == py.MOUSEBUTTONDOWN:
                pos = py.mouse.get_pos()
                if ev.button == 1:
                    if menu_buttons[0].collidepoint(pos):
                        return 1
                    elif menu_buttons[1].collidepoint(pos):
                        return 2
                    elif menu_buttons[2].collidepoint(pos):
                        return 3
                    elif menu_buttons[3].collidepoint(pos):
                        py.quit()

        py.display.update()
    # py.time.delay(4000)


def update_score(total):
    draw_text("Score: {}".format(total), 'letter', 'black', 20)


def main(difficulty, total):
    # variables
    hangman_status = 0
    clock = py.time.Clock()
    running = True
    circles = []
    guessed = []
    used = 0
    word = get_word('', [], difficulty)
    # constants
    FPS = 60
    # circle options
    RADIUS = 20
    GAP = 15
    OUTLINE = 3
    A = 65
    startx = round((W - (RADIUS * 2 + GAP)*13)/2)
    starty = 400
    for i in range(26):
        x = startx + GAP * 2 + ((RADIUS * 2 + GAP)*(i % 13))
        y = starty + ((i//13) * (GAP+RADIUS * 2))
        circles.append([x, y, chr(A+i), True])

    # main loop
    while running:
        clock.tick(FPS)
        pygame_events = py.event.get()
        for ev in pygame_events:
            if ev.type == py.QUIT:
                py.quit()
            elif ev.type == py.MOUSEBUTTONDOWN:
                mx, my = py.mouse.get_pos()
                for circle in circles:
                    x, y, letter, visible = circle
                    if visible:
                        dist = sqrt((x-mx)**2+(y-my)**2)
                        if dist < RADIUS:
                            circle[3] = False
                            if letter in word:
                                guessed.append(letter)
                            else:
                                hangman_status += 1

        guessed_word = get_word(word, guessed)
        draw(hangman_status, circles, RADIUS, OUTLINE, guessed_word)
        guessed, circles, used = hint(difficulty, word, guessed,
                                      circles, used, pygame_events)
        py.display.update()
        game_status = check_win_loss(word, guessed, hangman_status)
        if game_status:
            not_clicked = True
            py.time.delay(1000)
            while not_clicked:
                not_clicked, difficulty = draw_end(
                    game_status, word, difficulty)
            return game_status, difficulty


# menu
difficulty = menu()
total = 0
score = 0

while True:
    score, difficulty = main(difficulty, total)
    total += score
    if total < 0:
        total = 0
    for ev in py.event.get():
        if ev.type == py.QUIT:
            break

py.quit()
