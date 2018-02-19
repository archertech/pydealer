# -*- coding: utf-8 -*-

"""
This module contains the ``Card`` class. Each ``Card`` instance represents a
single playing card, of a given value and suit.
"""

class Suits(list):
    DIAMONDS = 'Diamonds'
    CLUBS = 'Clubs'
    HEARTS = 'Hearts'
    SPADES = 'Spades'

    def __init__(self, *args):
        if len(args) > 0:
            super(Suits, self).__init__(*args)
        else:
            super(Suits, self).__init__([
                self.CLUBS,
                self.DIAMONDS,
                self.HEARTS,
                self.SPADES
            ])


class Faces(list):
    TWO = '2'
    THREE = '3'
    FOUR = '4'
    FIVE = '5'
    SIX = '6'
    SEVEN = '7'
    EIGHT = '8'
    NINE = '9'
    TEN = '10'
    JACK = 'Jack'
    QUEEN = 'Queen'
    KING = 'King'
    ACE = 'Ace'
    JOKER = 'Joker'

    def __init__(self, *args):
        if len(args) > 0:
            super(Faces, self).__init__(*args)
        else:
            super(Faces, self).__init__([
                '2',
                '3',
                '4',
                '5',
                '6',
                '7',
                '8',
                '9',
                '10',
                self.JACK,
                self.QUEEN,
                self.KING,
                self.ACE
            ])


class Card(object):
    """
    The Card class, each instance representing a single playing card.

    :arg str value:
        The card value.
    :arg str suit:
        The card suit.

    """
    def __init__(self, face, suit, ranks=None, value=None):
        """
        Card constructor method.

        :arg str value:
            The card value.
        :arg str suit:
            The card suit.
        :arg pydealer.Ranks ranks:
            Optional. A pydealer.Ranks object for comparisons.
        :arg int value:
            Optional. When using non-standard decks, this must be provided as
            the card's simple comparison value
        """

        self.face = str(face).capitalize()
        self.suit = str(suit).capitalize() if suit else suit
        if ranks is not None:
            self.set_ranks(ranks)

        if value is not None:
            self.value = int(value)
        elif self.face == Faces.JOKER:
            self.value = 15
        elif self.face == Faces.ACE:
            self.value = 14
        elif self.face == Faces.KING:
            self.value = 13
        elif self.face == Faces.QUEEN:
            self.value = 12
        elif self.face == Faces.JACK:
            self.value = 11
        else:
            self.value = int(self.face)


    def set_ranks(self, ranks):
        if not isinstance(ranks, Ranks):
            raise ValueError('Ranks object must be a valid pydealer.Ranks object')

        self.ranks = ranks


    def get_rank(self):
        if not isinstance(self.ranks, Ranks):
            return self.value

        else:
            return self.ranks.get_card_rank(self)


    def __eq__(self, other):
        """
        Allows for Card value/suit equality comparisons.

        :arg Card other:
            The other card to compare to.

        :returns:
            ``True`` or ``False``.

        """
        if not isinstace(other, Card):
            raise ValueError('Invalid comparison: One value is not a Card object')

        return (self.value == other.value and self.suit == other.suit)


    def __ne__(self, other):
        """
        Allows for Card value/suit equality comparisons.

        :arg Card other:
            The other card to compare to.

        :returns:
            ``True`` or ``False``.

        """
        return not (self == other)


    def __ge__(self, other):
        """
        Allows for Card value/suit comparisons.

        :arg Card other:
            The other card to compare to.

        :returns:
            ``True`` or ``False``.

        """
        if not isinstance(other, Card):
            raise ValueError('Invalid comparison: One value is not a Card object')

        return (self.value >= other.value)


    def __gt__(self, other):
        """
        Allows for Card value/suit comparisons.

        :arg Card other:
            The other card to compare to.

        :returns:
            ``True`` or ``False``.

        """
        if not isinstance(other, Card):
            raise ValueError('Invalid comparison: One value is not a Card object')

        return (self.value > other.value)


    def __le__(self, other):
        """
        Allows for Card value/suit comparisons.

        :arg Card other:
            The other card to compare to.

        :returns:
            ``True`` or ``False``.

        """
        if not isinstance(other, Card):
            raise ValueError('Invalid comparison: One value is not a Card object')

        return (self.value <= other.value)


    def __lt__(self, other):
        """
        Allows for Card value/suit comparisons.

        :arg Card other:
            The other card to compare to.

        :returns:
            ``True`` or ``False``.

        """
        if not isinstance(other, Card):
            raise ValueError('Invalid comparison: One value is not a Card object')

        return (self.value < other.value)


    def __hash__(self):
        """
        Returns the hash value of the ``Card`` instance.

        :returns:
            A unique number, or hash for the Card.

        """
        return hash((self.face, self.suit))


    def __repr__(self):
        """
        Returns a string representation of the ``Card`` instance.

        :returns:
            A string representation of the Card instance.

        """
        return "Card(face=%r, suit=%r)" % (self.face, self.suit)


    def __str__(self):
        """
        Returns the full name of the ``Card`` instance.

        :returns:
            The card name.

        """
        return "%s" % (self.name)


    def eq(self, other):
        """
        Compares the card against another card, ``other``, checking whether
        the card is equal to ``other``, based on the ranks.

        :arg Card other:
            The second Card to compare.

        :returns:
            ``True`` or ``False``.

        """
        if not isinstance(other, Card):
            raise ValueError('Comparison must be made against another Card object')

        return self.get_rank() == other.get_rank()


    def ge(self, other):
        """
        Compares the card against another card, ``other``, checking whether
        the card is greater than or equal to ``other``, based on the ranks.

        :arg Card other:
            The second Card to compare.

        :returns:
            ``True`` or ``False``.

        """
        if not isinstance(other, Card):
            raise ValueError('Comparison must be made against another Card object')

        return self.get_rank() >= other.get_rank()


    def gt(self, other):
        """
        Compares the card against another card, ``other``, checking whether
        the card is greater than ``other``, based on the ranks.

        :arg Card other:
            The second Card to compare.

        :returns:
            ``True`` or ``False``.

        """
        if not isinstance(other, Card):
            raise ValueError('Comparison must be made against another Card object')

        return self.get_rank() > other.get_rank()


    def le(self, other):
        """
        Compares the card against another card, ``other``, checking whether
        the card is less than or equal to ``other``, based on the ranks.

        :arg Card other:
            The second Card to compare.

        :returns:
            ``True`` or ``False``.

        """
        return not self.gt(other)


    def lt(self, other):
        """
        Compares the card against another card, ``other``, checking whether
        the card is less than ``other``, based on the ranks.

        :arg Card other:
            The second Card to compare.

        :returns:
            ``True`` or ``False``.

        """
        return not self.ge(other)


    def ne(self, other, ranks=None):
        """
        Compares the card against another card, ``other``, checking whether
        the card is not equal to ``other``, based on the ranks.

        :arg Card other:
            The second Card to compare.

        :returns:
            ``True`` or ``False``.

        """
        return not self.eq(other)


    def matches(self, term):
        """
        Checks a given search term against a the card's full name, suit,
        value, and abbreviation.
    
        :arg str term:
            The search term to check for. Can be a card full name, suit,
            value, or abbreviation.
    
        :returns:
            ``True`` or ``False``.
    
        """

        check_list = [
            x.lower() for x in [
                self.name,
                self.suit,
                self.face,
                self.value,
                self.abbrev,
                self.suit[0]
            ]
        ]
        if self.face in [
                Faces.JOKER,
                Faces.ACE,
                Faces.KING,
                Faces.QUEEN,
                Faces.JACK
            ]:
            check_list.add(self.face[0].lower())

        return term.lower() in check_list


    @property
    def abbrev(self):
        """
        Constructs an abbreviation for the card
    
        :returns:
            A newly constructed abbreviation string
        """

        if self.face == Faces.JOKER:
            return "JKR"
        elif self.face in [
                Faces.ACE,
                Faces.KING,
                Faces.QUEEN,
                Faces.JACK
            ]:
            return "%s%s" % (self.face[0], suit[0])
        else:
            return "%s%s" % (self.face, suit[0])


    @property
    def name(self):
        """
        Constructs a name for the card
    
        :returns:
            A newly constructed name string
        """

        if self.value == Faces.JOKER:
            return "Joker"
        else:
            return "%s of %s" % (self.face, self.suit)
