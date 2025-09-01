import curses

import pyspaced
import sys

from curses import wrapper

class ConsoleTraining:

    def __init__(self, deck):
        self.deck = deck

    def train(self):
        for card_score in self.deck.get_next_card():
            print('--------------------------------')
            print('QUESTION (press enter to see the answer):\t', card_score.front)
            input()
            print('ANSWER:\t', self.deck.get_answer(card_score))
            outcome = ''
            while outcome not in ['B', 'H', 'E', 'Q']:
                outcome = (input('Enter B for BAD, H for HARD, E for EASY, Q for QUIT, then press ENTER...').
                           strip().upper())
            if outcome == 'Q':
                break
            else:
                if outcome == 'B':
                    user_grade = 1
                elif outcome == 'H':
                    user_grade = 3
                elif outcome == 'E':
                    user_grade = 5
                self.deck.update_scores(user_grade, card_score)
        self.deck.save_scores()


class CursesTraining:

    def __init__(self, deck):
        self.deck = deck

    def train(self, stdscr):
        curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_BLUE, curses.COLOR_BLACK)
        for card_score in self.deck.get_next_card():
            stdscr.clear()
            stdscr.addstr(0, 0, 'QUESTION', curses.A_UNDERLINE)
            stdscr.addstr(1, 0, card_score.front, curses.color_pair(1))
            stdscr.addstr(8, 0, 'Press a key ', curses.A_STANDOUT)
            stdscr.refresh()
            stdscr.getkey()
            stdscr.clear()
            stdscr.addstr(0, 0, 'QUESTION', curses.A_UNDERLINE)
            stdscr.addstr(1, 0, card_score.front, curses.color_pair(1))
            stdscr.addstr(3, 0, 'ANSWER', curses.A_UNDERLINE)
            stdscr.addstr(4, 0, self.deck.get_answer(card_score), curses.color_pair(2))
            stdscr.addstr(8, 0, '(B)ad ', curses.A_STANDOUT)
            stdscr.addstr(8, 10, '(H)ard ', curses.A_STANDOUT)
            stdscr.addstr(8, 20, '(E)asy ', curses.A_STANDOUT)
            stdscr.addstr(8, 30, '(Q)uit ', curses.A_STANDOUT)
            stdscr.refresh()
            outcome = ''
            while outcome not in ['B', 'H', 'E', 'Q']:
                outcome = stdscr.getkey().upper()
            if outcome == 'Q':
                break
            else:
                if outcome == 'B':
                    user_grade = 1
                elif outcome == 'H':
                    user_grade = 3
                elif outcome == 'E':
                    user_grade = 5
                self.deck.update_scores(user_grade, card_score)
        self.deck.save_scores()


if __name__ == '__main__':
    deck_file_path = sys.argv[1]
    deck = pyspaced.Deck(deck_file_path)
    # training = ConsoleTraining(deck)
    # training.train()
    training = CursesTraining(deck)
    wrapper(training.train)
