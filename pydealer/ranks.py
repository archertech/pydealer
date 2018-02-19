# -*- coding: utf-8 -*-

class Ranks(object):
    _values = {}

    ace_high = True
    jokers = False
    suit_first = False
    cards = {}

    # In the default rankings, suits are all equal
    ranks = {
        'suits': {
            'Diamonds': 0,
            'Hearts': 0,
            'Spades': 0,
            'Clubs': 0
        },
        'cards': {
            'Ace': 14,
            'King': 13,
            'Queen': 12,
            'Jack': 11,
            '10': 10,
            '9': 9,
            '8': 8,
            '7': 7,
            '6': 6,
            '5': 5,
            '4': 4,
            '3': 3,
            '2': 2
        }
    }

    def __init__(self,
                 ranks=None,
                 ace_high=True,
                 suit_first=None,
                 jokers=None):

        if ranks is not None and self._check_ranks_dict(ranks):
            self.ranks =  ranks

        if not ace_high:
            self.ranks['cards'][CardNames.ACE] = 1
            self.ace_high = False

        if suit_first is not None:
            self.suit_first = suit_first

        self.build_ranks()


    def _check_ranks_dict(self, ranks):
        if not isinstance(ranks, dict):
            raise ValueError('The provided ranks variable is not a dict()')

        if 'suits' not in ranks or 'cards' not in ranks:
            raise ValueError('When providing ranks, both "suits" and "cards" must be specified.')

        return True


    def compare_cards(self, card_x, card_y):
        # This is the python 2.x method of comparing list values, in python 3.x
        # you need to wrap this method with functools.cmp_to_key() in your
        # call to `sorted()`
        return self.get_card_rank(card_y) - self.get_card_rank(card_x)


    def build_ranks(self):
        for suit in self.ranks['suits'].keys():
            suitvalue = self.ranks['suits'][suit]
            if not suit in self._values:
                self._values.update({suit: {}})

            for card in self.ranks['cards'].keys():
                cardvalue = self.ranks['cards'][card]
                if self.suit_first:
                    value = suitvalue * cardvalue
                elif suitvalue != 0:
                    value = cardvalue + (suitvalue / 100)
                else:
                    value = cardvalue

                self._values[suit].update({card: value})


    def get_card_rank(self, card):
        if card.name == 'Joker':
            if self.jokers:
                return self._values['Joker']
            return 0

        if card.suit not in self._values:
            return 0
        elif card.card not in self._values[card.suit]:
            return 0

        return self._values[card.suit][card.card]
