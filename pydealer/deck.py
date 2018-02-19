# -*- coding: utf-8 -*-

from collections import deque

from pydealer.card import Card, Faces, Suits
from pydealer.stack import Stack, TOP, BOTTOM
from pydealer.ranks import Ranks


class Deck(Stack):

    decks = 1
    jokers = 0
    rebuild = False
    reshuffle = True
    ranks = None
    faces = None
    suits = None

    """
    The Deck class, representing the deck that the cards will be in. It is
    a sublcass of Stack, sharing all of the same methods, in addition to a
    couple of others you would expect a deck class to have.

    .. warning::
        At the moment, adding Jokers may cause some (most) functions/methods
        to throw errors.

    :arg cards:
        A list of cards to be the initial contents of the Deck. If provided,
        the deck will not automatically build a new deck. Can be a ``Stack``,
        ``Deck``, or ``list`` instance.
    :arg int decks:
        How many decks should be used. Default: 1
    :arg int jokers:
        How many jokers to add to the deck. Default: 0
    :arg bool build:
        Whether or not to build the deck on instantiation. Default: True
    :arg bool rebuild:
        Whether or not to rebuild the deck when it runs out of
        cards due to dealing. Default: False
    :arg bool reshuffle:
        Whether or not to shuffle the deck after rebuilding. Default: True
    :arg dict ranks:
        The rank class that will be referenced by the sorting
        methods etc. Default: pydealer.ranks.Ranks
    """

    def __init__(self,
                 decks=None,
                 jokers=None,
                 ranks=None,
                 cards=None,
                 build=True,
                 rebuild=False,
                 reshuffle=True,
                 faces=None,
                 suits=None):
        """
        Deck constructor method.
        """
        if ranks is None:
            ranks = Ranks()

        if cards is not None:
            if decks is not None or jokers is not None:
                raise ValueError('Invalid combination of parameters for deck instantiation')

            super(Deck, self).__init__(cards=cards, ranks=ranks)

        else:
            super(Deck, self).__init__(ranks=ranks)

            if decks is not None:
                if int(decks) < 0:
                    raise ValueError('Cannot instantiate a Deck with a negative amount of decks')

                self.decks = int(decks)

            if jokers is not None:
                if int(jokers) < 0:
                    raise ValueError('Cannot instantiate a Deck with a negative amount of jokers')

                self.jokers = int(jokers)

        if rebuild is not None:
            self.rebuild = rebuild

        if reshuffle is not None:
            self.reshuffle = reshuffle

        if faces is not None:
            if not isinstance(faces, list):
                raise ValueError('Provided faces must be a list')

            self.faces = faces
        else:
            self.faces = Faces()

        if suits is not None:
            if not isinstance(suits, list):
                raise ValueError('Provided suits must be a list')

            self.suits = suits
        else:
            self.suits = Suits()

        if build:
            self.build()


    def __repr__(self):
        """
        Returns a string representation of the ``Deck`` instance.

        :returns:
            A string representation of the Deck instance.

        """
        return "Deck(cards=%r)" % (self.cards)



    def deal(self, num=1, rebuild=None, shuffle=None, end=TOP):
        """
        Returns a list of cards, which are removed from the deck.

        :arg int num:
            The number of cards to deal.
        :arg bool rebuild:
            Whether or not to rebuild the deck when cards run out.
        :arg bool shuffle:
            Whether or not to shuffle on rebuild.
        :arg str end:
            The end of the ``Stack`` to add the cards to. Can be ``TOP`` ("top")
            or ``BOTTOM`` ("bottom").

        :returns:
            A Stack containing the given number of cards from the deck.

        """
        _num = num

        if rebuild is None:
            rebuild = self.rebuild

        if shuffle is None:
            reshuffle = self.reshuffle

        self_size = len(self.cards)

        if rebuild or num <= self_size:
            dealt_cards = [None] * num
        elif num > self_size:
            dealt_cards = [None] * self_size

        while num > 0:
            ends = {TOP: self.cards.pop, BOTTOM: self.cards.popleft}
            n = _num - num
            try:
                card = ends[end]()
                dealt_cards[n] = card
                num -= 1
            except:
                if self.size == 0:
                    if rebuild:
                        self.build()
                        if reshuffle:
                            self.shuffle()
                    else:
                        break

        return Stack(cards=dealt_cards, ranks=self.ranks)


    def build(self, faces=None, suits=None):
        """
        Builds a list containing a full French deck of 52 Card instances.
    
        :arg int jokers:
            The number of jokers to include.
    
        :returns:
            A list containing a full French deck of 52 Card instances, plus
            Jokers, if applicable.
        """

        faces = faces or self.faces
        suits = suits or self.suits

        if not isinstance(faces, list) or not isinstance(suits, list):
            raise ValueError('Cannot build a deck with a list of faces and suits')

        self.cards = [Card(face, suit) for face in faces for suit in suits]

        if self.jokers:
            self.cards += [Card(Faces.JOKER, None) for i in range(int(self.jokers))]
    
        self.cards = deque(self.cards)
        return self.cards
