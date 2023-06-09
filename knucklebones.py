import random as r
import pygame as pg


def slide_dice(col):
    """Moves dice in a list to 'fill' empty space. """
    if all(col):
        return col
    elif col.count(None) == 2:
        if col[0]:
            return col
        else:
            while not col[0]:
                col = col[1:] + col[:1]
            return col
    elif col.count(None) == 1:
        if col[0] and col[1]:
            return col
        else:
            for pos, c in enumerate(col):
                if col[pos-1]:
                    continue
                else:
                    col[pos-1] = c
                    col[pos] = None
            return col
    else:
        return col


def match_color(d, pos):
    """Tests a grid to see if there's matches. Returns a color to make it clearer when dice match. """
    d1 = dict(list(d.items())[0:3])
    d2 = dict(list(d.items())[3:6])
    d3 = dict(list(d.items())[6:9])
    if pos in d1.keys():
        match_test = list(d1.values())
        match_col = d1
    elif pos in d2.keys():
        match_test = list(d2.values())
        match_col = d2
    elif pos in d3.keys():
        match_test = list(d3.values())
        match_col = d3
    else:
        print('error')
        return 0, 0, 0
    if match_test.count(match_col[pos]) == 2:
        return 184, 115, 51  # copper color
    elif match_test.count(match_col[pos]) == 3:
        return 204, 204, 204  # silver color
    return 0, 0, 0


class Grid:
    """Grid object. Defaults to empty grid. """

    def __init__(self, coords, matrix=[[None, None, None], [None, None, None], [None, None, None]], name=None):
        self.matrix = matrix
        self.coords = coords
        self.name = name
        self.fixed = [d for col in matrix for d in col]

    def __str__(self):
        return str(self.matrix)

    def __repr__(self):
        return str(self.matrix, self.name)

    def clear(self, col=None):
        """Clears a column or the whole grid. """
        if col:
            self.matrix[col] = [None, None, None]
        else:
            self.matrix = [[None, None, None], [None, None, None], [None, None, None]]

    def add_die(self, col, num):
        """Adds a die to a column. """
        for pos, c in enumerate(self.matrix[col]):
            if not c:
                self.matrix[col][pos] = num
                break
        return self.matrix

    def fix(self):
        """Returns a list with all values of self.matrix. Used for mapping the grid to pygame rectangles. """
        return [d for col in self.matrix for d in col]

    def tally_score(self, w='all'):
        """Tallies the score. """
        score = 0
        if w == 'all':
            for col in self.matrix:
                for c in set(col):
                    if c:
                        if col.count(c) > 1:
                            score += (c * col.count(c)) * col.count(c)
                        else:
                            score += c
        else:
            for c in set(self.matrix[w]):
                if c:
                    if self.matrix[w].count(c) > 1:
                        score += (c * self.matrix[w].count(c)) * self.matrix[w].count(c)
                    else:
                        score += c
        return score

    def check_end(self):
        """Checks if the game is done; if a matrix has all positions filled. """
        c = 0
        for col in self.matrix:
            if all(col):
                c += 1
        if c == 3:
            return True
        else:
            return False

    def del_dice(self, x):
        """Deletes dice in grid self based on grid x. """
        for col, contents in enumerate(x.matrix):
            for die in set(contents):
                if die in set(self.matrix[col]):
                    self.matrix[col] = slide_dice([None if d == die else d for d in self.matrix[col]])
        return self.matrix

    def compare(self, x):
        """Compares this grid to grid x and updates grid x accordingly. """
        return x.del_dice(self)


class Knucklebones:
    """Main game class. """
    def __init__(self):
        self.x = Grid((460, 740), name='p1')
        self.y = Grid((40, 340), name='p2')
        self.example_1 = Grid((400, 400))
        self.example_2 = Grid((400, 400))

    @staticmethod
    def menu(mpos):
        """Draws the main menu. """
        title = font.render('knucklebones', False, (0, 0, 0))
        start_button = font.render('start 2 player', False, (0, 0, 0))
        start_against = font.render('start vs COM', False, (0, 0, 0))
        quit_button = font.render('quit', False, (0, 0, 0))
        how_button = font.render('how to play', False, (0, 0, 0))
        if pg.Rect(20, 350, 330, 45).collidepoint(mpos):
            start_button = font.render('start 2 player', False, (255, 255, 0))
        if pg.Rect(120, 420, 330, 45).collidepoint(mpos):
            start_against = font.render('start vs COM', False, (255, 255, 0))
        if pg.Rect(202, 510, 100, 45).collidepoint(mpos):
            quit_button = font.render('quit', False, (255, 255, 0))
        if pg.Rect(132, 600, 260, 45).collidepoint(mpos):
            how_button = font.render('how to play', False, (255, 255, 0))
        screen.blit(title, (100, 200))
        screen.blit(start_button, (20, 350))
        screen.blit(start_against, (120, 400))
        screen.blit(quit_button, (202, 500))
        screen.blit(how_button, (132, 600))

    def draw_main(self, turn, mpos, end=False):
        """Draws the main game. """
        for x in range(50, 350, 100):
            for y in range(self.x.coords[0], self.x.coords[1], 100):
                if p1_coords[(x, y)]:
                    num = font.render(str(p1_coords[(x, y)]), False, match_color(p1_coords, (x, y)))
                    screen.blit(num, (x+20, y))
                else:
                    pg.draw.rect(screen, (0, 0, 0), (x, y, 80, 60))
        for x in range(50, 350, 100):
            for y in range(self.y.coords[0], self.y.coords[1], 100):
                if p2_coords[(x, y)]:
                    num = font.render(str(p2_coords[(x, y)]), False, match_color(p2_coords, (x, y)))
                    screen.blit(num, (x+20, y))
                else:
                    pg.draw.rect(screen, (0, 0, 0), (x, y, 80, 60))
        if not end:
            if turn == 0:
                if pg.Rect(40, 450, 98, 275).collidepoint(mpos):  # left
                    pg.draw.rect(screen, 'red', (40, 450, 100, 275), 8)
                if pg.Rect(140, 450, 98, 275).collidepoint(mpos):  # middle
                    pg.draw.rect(screen, 'red', (140, 450, 100, 275), 8)
                if pg.Rect(240, 450, 98, 275).collidepoint(mpos):  # right
                    pg.draw.rect(screen, 'red', (240, 450, 100, 275), 8)
            elif turn == 1:
                if pg.Rect(40, 30, 98, 275).collidepoint(mpos):  # left
                    pg.draw.rect(screen, 'red', (40, 30, 100, 275), 8)
                if pg.Rect(140, 30, 98, 275).collidepoint(mpos):  # middle
                    pg.draw.rect(screen, 'red', (140, 30, 100, 275), 8)
                if pg.Rect(240, 30, 98, 275).collidepoint(mpos):  # right
                    pg.draw.rect(screen, 'red', (240, 30, 100, 275), 8)

    @staticmethod
    def take_turn(p, e, mpos, roll):
        """Takes a turn for one human player. p takes the turn, e is the other player. """
        if p.name == 'p1':
            if pg.Rect(40, 450, 98, 275).collidepoint(mpos) and not all(p.matrix[0]):  # left
                p.add_die(0, roll)
            if pg.Rect(140, 450, 98, 275).collidepoint(mpos) and not all(p.matrix[1]):  # middle
                p.add_die(1, roll)
            if pg.Rect(240, 450, 98, 275).collidepoint(mpos) and not all(p.matrix[2]):  # right
                p.add_die(2, roll)
        elif p.name == 'p2':
            if pg.Rect(40, 30, 98, 275).collidepoint(mpos):  # left
                p.add_die(0, roll)
            if pg.Rect(140, 30, 98, 275).collidepoint(mpos):  # middle
                p.add_die(1, roll)
            if pg.Rect(240, 30, 98, 275).collidepoint(mpos):  # right
                p.add_die(2, roll)
        e.matrix = p.compare(e)  # delete matching dice from the other player's grid

    @staticmethod
    def take_com_turn(p, e, level, roll):
        """Takes a turn for one computer player. level determines difficulty. """
        if level == 0:  # simplest COM player; places dice totally randomly.
            place = r.randint(0, 2)
            p.add_die(place, roll)
            e.matrix = p.compare(e)
        if level == 1:  # tries to delete dice from p1
            options = {0: 0,
                       1: 0,
                       2: 0}
            for loc, col in enumerate(e.matrix):
                if roll in col:
                    options[loc] += 1
            place = max(options, key=options.get)
            if sum(options.values()) == 0:  # if nothing is good just do whatever
                place = r.randint(0, 2)
            p.add_die(place, roll)
            e.matrix = p.compare(e)
        if level == 2:  # tries to maximize score by matching dice
            options = {0: 0,
                       1: 0,
                       2: 0}
            place = -1
            for loc, col in enumerate(p.matrix):
                if roll in col:
                    options[loc] += 1
                    if options[loc] == 3:
                        options[loc] = 0
            if sum(options.values()) > 0:  # viable match
                if not all(p.matrix[max(options, key=options.get)]):
                    place = max(options, key=options.get)
                else:
                    options[max(options, key=options.get)] = 0
            elif sum(options.values()) == 0:  # tries to leave space to match dice
                for loc, col in enumerate(p.matrix):
                    if not any(col):
                        place = loc
            if place == -1:  # do whatever
                place = r.randint(0, 2)
            p.add_die(place, roll)
            e.matrix = p.compare(e)
        if level == 3:  # combines levels 1 and 2 - tries matches, then deleting dice, then random
            options = {0: 0,
                       1: 0,
                       2: 0}
            place = -1
            for loc, col in enumerate(p.matrix):
                if roll in col:
                    options[loc] += 1
                    if options[loc] == 3:
                        options[loc] = 0
            if sum(options.values()) > 0:  # match - place here
                if not all(p.matrix[max(options, key=options.get)]):
                    place = max(options, key=options.get)
                else:
                    options[max(options, key=options.get)] = 0
            elif sum(options.values()) == 0:  # no match - try for deleting
                options = {0: 0,
                           1: 0,
                           2: 0}
                for loc, col in enumerate(e.matrix):
                    if roll in col:
                        options[loc] += 1
                if sum(options.values()) > 0:  # delete - place here
                    if not all(p.matrix[max(options, key=options.get)]):
                        place = max(options, key=options.get)
                    else:
                        options[max(options, key=options.get)] = 0
            if place == -1:  # no delete - try to leave space for better dice
                spots = []
                for loc, col in enumerate(p.matrix):
                    if not any(col):
                        spots.append(loc)
                if spots:
                    place = r.choice(spots)
                else:  # if ALL ELSE fails
                    place = r.randint(0, 2)  # put it wherever
            p.add_die(place, roll)
            e.matrix = p.compare(e)

    @staticmethod
    def draw_score(t):
        """Draws the scores. """
        scores1 = []
        scores2 = []
        ifont = pg.font.Font('papercut.ttf', 30)
        for i in range(3):
            scores1.append(game.x.tally_score(w=i))
            scores2.append(game.y.tally_score(w=i))
        if t == 0:
            p1score = font.render(f"p1: {str(game.x.tally_score())}", False, (255, 255, 0))
            p2score = font.render(f"p2: {str(game.y.tally_score())}", False, (0, 0, 0))
        if t == 1:
            p2score = font.render(f"p2: {str(game.y.tally_score())}", False, (255, 255, 0))
            p1score = font.render(f"p1: {str(game.x.tally_score())}", False, (0, 0, 0))
        if t == 2:
            p1score = font.render(f"p1: {str(game.x.tally_score())}", False, (0, 0, 0))
            p2score = font.render(f"p2: {str(game.y.tally_score())}", False, (0, 0, 0))
        screen.blit(p1score, (350, 660))
        screen.blit(p2score, (350, 40))
        # code to display all the individual column scores
        for i in range(3):
            screen.blit(ifont.render(str(scores1[i]), False, (0, 0, 0)), (50 + 100 * i, 400))
            screen.blit(ifont.render(str(scores2[i]), False, (0, 0, 0)), (50 + 100 * i, 300))

    def loop(self):
        """Simplifies the check to see if the game loop should run. """
        if not self.x.check_end() and not self.y.check_end():
            return True
        else:
            return False

    @staticmethod
    def draw_dice(roll, fancy):
        """Draws the roll with a fun animation. """
        if not fancy:
            rolltext = font.render(f"roll: {str(roll)}", False, (0, 0, 0))
            screen.blit(rolltext, (300, 350))
        if fancy:
            rolltext = font.render(f"roll: {str(roll)}", False, (255, 255, 0))
            screen.blit(rolltext, (300, 350))
        return roll

    def end(self, mpos):
        """Tallies scores and declares a winner! """
        p1score = self.x.tally_score()
        p2score = self.y.tally_score()
        if p1score > p2score:
            screen.blit(font.render('player 1 wins!', False, (0, 0, 0)), (10, 320))
        elif p1score < p2score:
            screen.blit(font.render('player 2 wins!', False, (0, 0, 0)), (10, 320))
        else:
            screen.blit(font.render('TIE???', False, (0, 0, 0)), (10, 320))
        play_again = font.render('play again?', False, (0, 0, 0))
        if pg.Rect(200, 370, 300, 70).collidepoint(mpos):
            play_again = font.render('play again?', False, (255, 255, 0))
        screen.blit(play_again, (200, 370))

    @staticmethod
    def draw_instructions(mpos):
        """Draws the big blocks of text on the how to play page. """
        ifont = pg.font.Font('freesansbold.ttf', 20)
        title = font.render('knucklebones', False, (0, 0, 0))
        start_button = font.render('start', False, (0, 0, 0))
        if pg.Rect(202, 100, 130, 45).collidepoint(mpos):
            start_button = font.render('start', False, (255, 255, 0))
        lines = []
        instructions = "This is a turn-based game about rolling dice.*" \
                       "Each turn, you get a 'roll', seen on the side.*" \
                       "Place this roll in your column with the mouse.*" \
                       "Your score is next to your grid.*" \
                       "Score is calculated by adding dice in your grid.*" \
                       "You can 'destroy' the other player's dice*" \
                       "by aligning the same number in the same column.*" \
                       "For example, if player one has a 4 in column 1*" \
                       "and player 2 places a 4 in column 1, p1's 4 will*" \
                       "disappear.*" \
                       "Two or more matching dice in one column*" \
                       "will increase their score, indicated by color.*" \
                       "The game ends when one player fills their grid.*"\
                       "Score higher than your opponent to win!*" \
                       "Credit to CULT OF THE LAMB for the base game."
        for i in instructions.split('*'):
            lines.append(ifont.render(i, False, (0, 0, 0)))
        screen.blit(title, (100, 10))
        screen.blit(start_button, (202, 90))
        for num, line in enumerate(lines, 5):
            screen.blit(line, (10, num*30))


# various init stuff
pg.init()
font = pg.font.Font('papercut.ttf', 50)  # using a custom font!
game = Knucklebones()
screen = pg.display.set_mode((500, 800))  # window size
clock = pg.time.Clock()
pg.display.set_caption("KNUCKLEBONES")  # window title
bgcolor = (82, 24, 44)
rectcolor = (255, 219, 88)

# these lines of code map Grid objects to x and y coordinates to draw the dice on the game screen
p1_c = [(50, 460), (50, 560), (50, 660), (150, 460), (150, 560), (150, 660), (250, 460), (250, 560), (250, 660)]
p2_c = [(50, 240), (50, 140), (50, 40), (150, 240), (150, 140), (150, 40), (250, 240), (250, 140), (250, 40)]
p1_coords, p2_coords = dict(zip(p1_c, game.x.fix())), dict(zip(p2_c, game.y.fix()))

# game-centric variables
running = True
stage = 1  # stage 1 is menu, stage 2 is main game, stage 3 is tally, stage 0 is how to play
turn = 0  # turn 0 is p1, turn 1 is p2
com = False  # are you playing against a computer or not
com_vs = False  # used for testing COM
drawroll = True  # play the "rolling" animation
roll = r.randint(1, 6)  # the first roll
com_level = 3  # how hard is the computer?

# used for timing logic without using sleep
comtimer = 0  # times computer "play" time
rolltimer = 0  # times roll animation
roll_counter = 0  # times roll animation
inbetween = 0  # used as the basis for all the timing logic

while running:  # main game loop
    events = pg.event.get()
    click = False
    for event in events:
        if event.type == pg.QUIT:  # if the player closes the window close the game
            running = False
        # sets up click logic
        if event.type == pg.MOUSEBUTTONUP:
            click = False
        if event.type == pg.MOUSEBUTTONDOWN:
            click = True
        if event.type == pg.KEYDOWN:  # used to skip screens; for debugging
            if event.key == pg.K_p:
                stage += 1
            if event.key == pg.K_c:
                com_vs = True
    mousepos = pg.mouse.get_pos()
    screen.fill(bgcolor)
    if stage == 0:
        game.draw_instructions(mousepos)
        if click:
            if pg.Rect(202, 110, 130, 45).collidepoint(mousepos):
                stage = 1
    if stage == 1:
        game.menu(mousepos)
        if click:
            if pg.Rect(20, 350, 330, 45).collidepoint(mousepos):  # start the game!
                stage = 2
                com = False
                game.x.clear()
                game.y.clear()
            if pg.Rect(120, 420, 330, 45).collidepoint(mousepos):  # against a COM
                stage = 2
                com = True
                com_level = r.randint(1, 2)
                game.x.clear()
                game.y.clear()
            if pg.Rect(202, 500, 130, 45).collidepoint(mousepos):  # or if the player clicks quit close the game
                running = False
            if pg.Rect(132, 600, 260, 45).collidepoint(mousepos):  # go to instructions
                stage = 0
    if stage == 2:
        if game.loop():  # if neither player has filled their board
            game.draw_main(turn, mousepos)  # draw the grids
            if com_vs:  # com VS com
                if turn == 0:
                    comtimer = 0
                    testm = game.x.fix()
                    game.take_com_turn(game.x, game.y, 3, roll)
                    p1_coords = dict(zip(p1_c, game.x.fix()))
                    p2_coords = dict(zip(p2_c, game.y.fix()))
                    if testm != game.x.fix():
                        turn = 1
                        roll = r.randint(1, 6)
                if turn == 1:  # adds a slight delay to the computer's turn
                    comtimer = 0
                    testm = game.y.fix()
                    game.take_com_turn(game.y, game.x, 3, roll)
                    p1_coords = dict(zip(p1_c, game.x.fix()))
                    p2_coords = dict(zip(p2_c, game.y.fix()))
                    if testm != game.y.fix():
                        turn = 0
                        roll = r.randint(1, 6)
            elif com:  # VS computer
                if not drawroll:
                    if turn == 0 and click:
                        testm = game.x.fix()
                        game.take_turn(game.x, game.y, mousepos, roll)
                        p1_coords = dict(zip(p1_c, game.x.fix()))
                        p2_coords = dict(zip(p2_c, game.y.fix()))
                        if testm != game.x.fix():  # this makes sure that the player has updated their grid
                            turn = 1
                            roll = r.randint(1, 6)
                            drawroll = True
                    if turn == 1 and comtimer > 900:  # adds a slight delay to the computer's turn
                        comtimer = 0
                        testm = game.y.fix()
                        game.take_com_turn(game.y, game.x, 3, roll)
                        p1_coords = dict(zip(p1_c, game.x.fix()))
                        p2_coords = dict(zip(p2_c, game.y.fix()))
                        if testm != game.y.fix():
                            turn = 0
                            roll = r.randint(1, 6)
                            drawroll = True
                    elif turn == 1 and comtimer < 1000:
                        comtimer += inbetween
            else:
                if not drawroll:
                    if click:  # take a turn
                        testm = []
                        if turn == 0:
                            testm = game.x.fix()
                            game.take_turn(game.x, game.y, mousepos, roll)
                            p1_coords = dict(zip(p1_c, game.x.fix()))
                            p2_coords = dict(zip(p2_c, game.y.fix()))
                            if testm != game.x.fix():
                                turn = 1
                                roll = r.randint(1, 6)
                                drawroll = True
                        elif turn == 1:
                            testm = game.y.fix()
                            game.take_turn(game.y, game.x, mousepos, roll)
                            p1_coords = dict(zip(p1_c, game.x.fix()))
                            p2_coords = dict(zip(p2_c, game.y.fix()))
                            if testm != game.y.fix():
                                turn = 0
                                roll = r.randint(1, 6)
                                drawroll = True
            #  this has to be in the loop to stay updated with the game
            #  renders the next roll and each player's scores
            game.draw_score(turn)
            #  this draws a little roll animation
            if drawroll:
                game.draw_dice(roll, False)
                if roll_counter < 13:
                    if rolltimer > 20:
                        roll = r.randint(1, 6)
                        roll_counter += 1
                        rolltimer = 0
                    else:
                        print(roll_counter)
                        rolltimer += inbetween
                elif roll_counter >= 13:
                    drawroll = False
                    roll_counter = 0
            else:
                game.draw_dice(roll, True)
        else:  # once a player fills their board end the game
            stage = 3
    if stage == 3:
        game.draw_main(turn, mousepos, end=True)  # keep the grids there
        game.end(mousepos)  # tally up the scores
        game.draw_score(2)
        if click:  # restart the game
            if pg.Rect(200, 370, 300, 70).collidepoint(mousepos):
                stage = 1
    pg.display.flip()
    clock.tick(60)  # fps
    inbetween = clock.get_time()  # how much time between frames, used for timing
pg.quit()
