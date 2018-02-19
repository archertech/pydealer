# -*- coding: utf-8 -*-

import time

from pydealer.card import Card


def open_cards(filename=None):
    """
    Open cards from a txt file.

    :arg str filename:
        The filename of the deck file to open. If no filename given,
        defaults to "cards-YYYYMMDD.txt", where "YYYYMMDD" is the year, month,
        and day. For example, "cards-20140711.txt".

    :returns:
        The opened cards, as a list.

    """
    filename = filename or "cards-%s.txt" % (time.strftime("%Y%m%d"))

    with open(filename, "r") as deck_file:
        card_data = [line.rstrip("\n") for line in deck_file.readlines()]

    cards = [None] * len(card_data)

    for i, card in enumerate(card_data):
        card = card.split()
        cards[i] = Card(card[0], card[1])

    return cards


def save_cards(cards, filename=None):
    """
    Save the given cards, in plain text, to a txt file.

    :arg cards:
        The cards to save. Can be a ``Stack``, ``Deck``, or ``list``.
    :arg str filename:
        The filename to use for the cards file. If no filename given,
        defaults to "cards-YYYYMMDD.txt", where "YYYYMMDD" is the year, month,
        and day. For example, "cards-20140711.txt".

    """
    filename = filename or "cards-%s.txt" % (time.strftime("%Y%m%d"))

    with open(filename, "w") as deck_file:
        card_reprs = ["%s %s\n" % (card.value, card.suit) for card in cards]
        card_reprs[-1] = card_reprs[-1].rstrip("\n")
        for card in card_reprs:
            deck_file.write(card)
