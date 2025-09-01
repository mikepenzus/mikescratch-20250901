import os
from pathlib import Path
import csv
import datetime


# https://orgmode.org/worg/org-contrib/org-drill.html#orgb87b089
# https://en.wikipedia.org/wiki/SuperMemo#Description_of_SM-2_algorithm
# https://super-memory.com/english/ol/sm2.htm
# https://faqs.ankiweb.net/the-2021-scheduler.html
# https://github.com/thyagoluciano/sm2
# https://www.youtube.com/watch?v=dF5rY3xQeAQ
# https://en.wikipedia.org/wiki/Incremental_reading


class CardScore:

    def __init__(self, input_dictionary = None):
        if input_dictionary:
            self.front = input_dictionary['front'].strip()
            self.last_review_date = datetime.datetime.fromisoformat(input_dictionary['last_review_date']
                                                           .strip().replace('Z', '+00:00'))
            self.no_repetitions = int(input_dictionary['no_repetitions'])
            self.easiness_factor = float(input_dictionary['easiness_factor'])
            self.interval = int(input_dictionary['interval'])
        else:
            self.front = ''
            self.last_review_date = datetime.date(1970, 1, 1)
            self.no_repetitions = 0
            self.easiness_factor = 2.5
            self.interval = 1

    def __dict__(self):
        return {'front': self.front, 'last_review_date': self.last_review_date, 'no_repetitions': self.no_repetitions,
                'easiness_factor': self.easiness_factor, 'interval': self.interval}

    def __str__(self):
        return str(self.__dict__())

    def __repr__(self):
        return str(self.__dict__())


class Deck:

    def __init__(self, deck_file_path: str):
        self.card_scores = None
        self.cards = {}
        self.owner = ''                         # TODO: to fix
        self.no_max_items_per_session = 30      # TODO: to fix
        self.wait_time = 3                      # TODO: to fix
        self.deck_file_path = os.path.abspath(deck_file_path)
        self.deck_name = Path(self.deck_file_path).stem
        self.deck_score_file_path = os.path.splitext(self.deck_file_path)[0] + '.csv'
        current_front = ''
        with open(self.deck_file_path) as deck_file:
            for line in deck_file:
                normalized_line = line.strip()
                if normalized_line != '':
                    if current_front == '':
                        current_front = normalized_line
                    else:
                        if normalized_line.startswith(':'):
                            normalized_line = normalized_line[1:].strip()
                            self.cards[current_front] = normalized_line
                            current_front = ''
                        else:
                            raise Exception('Deck back cards must start with :')
        self.load_scores()

    def load_scores(self):
        self.card_scores = {}
        try:
            with open(self.deck_score_file_path) as csvfile:
                reader = csv.DictReader(csvfile, delimiter='|')
                for row in reader:
                    card_score = CardScore(row)
                    if card_score.front in self.cards:
                        self.card_scores[card_score.front] = card_score
        except FileNotFoundError:
            self.card_scores = {}
        for key, value in self.cards.items():
            if key not in self.card_scores:
                default_card_score = CardScore()
                default_card_score.front = key
                self.card_scores[key] = default_card_score

    def save_scores(self):
        with open(self.deck_score_file_path, 'w') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=['front', 'last_review_date',
                        'no_repetitions', 'easiness_factor', 'interval'], delimiter='|')
            writer.writeheader()
            for key, card in self.card_scores.items():
                writer.writerow(card.__dict__())

    def get_answer(self, card_score: CardScore):
        return self.cards[card_score.front]

    def get_next_card(self):
        # TODO: scanning of cards to implement
        # scheduled reviews
        trial_index = 1
        for card_score in self.card_scores.values():
            if trial_index > self.no_max_items_per_session:
                return
            trial_index += 1
            yield card_score
        # TODO: re-review any cards marked with a grade less than 4 repeatedly until they give a grade ≥ 4

    def update_scores(self, user_grade, card_score):
        # 0: "Total blackout", complete failure to recall the information.
        # B -> 1: Incorrect response, but upon seeing the correct answer it felt familiar.
        # 2: Incorrect response, but upon seeing the correct answer it seemed easy to remember.
        # H -> 3: Correct response, but required significant effort to recall.
        # 4: Correct response, after some hesitation.
        # E -> 5: Correct response with perfect recall.

        if user_grade >= 3: # correct response
            if card_score.no_repetitions == 0:
                card_score.interval = 1
            elif card_score.no_repetitions == 1:
                card_score.interval = 6
            else:
                card_score.interval = int(round(card_score.interval * card_score.easiness_factor))
            card_score.no_repetitions += 1
        else: # incorrect response
            card_score.no_repetitions = 0
            card_score.interval = 1

        card_score.easiness_factor += 0.1 - (5 - user_grade) * (0.08 + (5 - user_grade) * 0.02)
        if card_score.easiness_factor < 1.3:
            card_score.easiness_factor = 1.3

        now = datetime.datetime.now()
        card_score.last_review_date = datetime.date(now.year, now.month, now.day)
        self.card_scores[card_score.front] = card_score

