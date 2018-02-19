# -*- coding: utf-8 -*-

from functools import cmp_to_key
from collections import deque
import random

from pydealer.ranks import Ranks
from pydealer.card import Card

from pydealer.utils import open_cards, save_cards


TOP = 'top'
BOTTOM = 'bottom'

class Stack(object):
    """
    The Stack class, representing a collection of cards. This is the main
    'card container' class, with methods for manipulating it's contents.
    A Stack can be used as a hand or a discard pile, etc.
    """

    cards = None
    ranks = None

    def __init__(self, cards=None, ranks=None):
        """
        Stack constructor method.

        :arg list cards:
            Optional. A list of cards to be the initial contents of the Stack.
        :arg pydealer.Ranks ranks:
            Optional. The ranks to use for comparisons
        """

        if cards is not None:
            if isinstance(cards, list):
                self.cards = deque(cards)
            elif getattr(cards, 'cards'):
                self.cards = deque(deepcopy(cards.cards))
            else:
                raise ValueError('Cards is not of the correct type to instantiate a Stack')
        else:
            self.cards = deque()

        if ranks is not None:
            if not isinstance(ranks, Ranks):
                raise ValueError('Provided ranks is not a subclass of pydealer.Ranks')

            self.ranks = ranks


    def __add__(self, other):
        """
        Allows users to add (merge) Stack/Deck instances together, with the
        ``+`` operand. You can also add a list of ``Card`` instances to a
        Stack/Deck instance.

        :arg other:
            The other ``Stack``, or ``Deck`` instance, or list of ``Card``
            instances to add to the ``Stack``/``Deck`` instance.
        """

        if isinstance(other, list):
            self.cards = deque(list(self.cards) + other)
        elif isinstance(other, Stack):
            self.cards = deque(list(self.cards) + list(other.cards))
        elif isinstance(other, Card):
            self.cards.add(other)
        else:
            raise ValueError('Unmergable value')


    def __contains__(self, card):
        """
        Allows for Card instance (not value & suit) inclusion checks.

        :arg Card card:
            The Card instance to check for.

        :returns:
            Whether or not the Card instance is in the Deck.

        """
        return id(card) in [id(x) for x in self.cards]


    def __delitem__(self, indice):
        """
        Allows for deletion of a Card instance, using del.

        :arg int indice:
            The indice to delete.

        """
        del self.cards[indice]


    def __getitem__(self, key):
        """
        Allows for accessing, and slicing of cards, using ``Deck[indice]``,
        ``Deck[start:stop]``, etc.

        :arg int indice:
            The indice to get.

        :returns:
            The ``Card`` at the given indice.

        """
        self_len = len(self.cards)
        if isinstance(key, slice):
            return [self[i] for i in range(*key.indices(self_len))]
        elif isinstance(key, int):
            if key < 0 :
                key += self_len
            if key >= self_len:
                raise IndexError("The index ({}) is out of range.".format(key))
            return self.cards[key]
        else:
            raise TypeError("Invalid argument type.")


    def __len__(self):
        """
        Allows check the Stack length, with len.

        :returns:
            The length of the stack (self.cards).

        """
        return len(self.cards)


    def __eq__(self, other):
        """
        Allows for Stack comparisons. Checks to see if the given ``other``
        contains the same cards, in the same order (based on value & suit,
        not instance).

        :arg other:
            The other ``Stack``/``Deck`` instance or ``list`` to compare to.

        :returns:
            ``True`` or ``False``.
        """
        return self.compare(other)


    def __ne__(self, other):
        """
        Allows for Stack comparisons. Checks to see if the given ``other``
        does not contain the same cards, in the same order (based on value &
        suit, not instance).

        :arg other:
            The other ``Stack``/``Deck`` instance or ``list`` to compare to.

        :returns:
            ``True`` or ``False``.

        """
        return not self.compare(other)


    def __repr__(self):
        """
        The repr magic method.

        :returns:
            A representation of the ``Deck`` instance.

        """
        return "Stack(cards=%r)" % (self.cards)


    def __setitem__(self, indice, value):
        """
        Assign cards to specific stack indices, like a list.

        Example:
            stack[16] = card_object

        :arg int indice:
            The indice to set.
        :arg Card value:
            The Card to set the indice to.

        """
        self.cards[indice] = value


    def __str__(self):
        """
        Allows users to print a human readable representation of the ``Stack``
        instance, using ``print``.

        :returns:
            A str of the names of the cards in the stack.

        """
        card_names = "".join([x.name + "\n" for x in self.cards]).rstrip("\n")
        return "%s" % (card_names)


    def add(self, cards, end=TOP):
        """
        Adds the given list of ``Card`` instances to the top of the stack.

        :arg cards:
            The cards to add to the ``Stack``. Can be a single ``Card``
            instance, or a ``list`` of cards.
        :arg str end:
            The end of the ``Stack`` to add the cards to. Can be ``TOP`` ("top")
            or ``BOTTOM`` ("bottom").

        """
        if end is TOP:
            try:
                self.cards += cards
            except:
                self.cards += [cards]
        elif end is BOTTOM:
            try:
                self.cards.extendleft(cards)
            except:
                self.cards.extendleft([cards])


    def deal(self, num=1, end=TOP):
        """
        Returns a list of cards, which are removed from the Stack.

        :arg int num:
            The number of cards to deal.
        :arg str end:
            Which end to deal from. Can be ``0`` (top) or ``1`` (bottom).

        :returns:
            The given number of cards from the stack.

        """
        ends = {TOP: self.cards.pop, BOTTOM: self.cards.popleft}

        self_size = len(self.cards)

        if num <= self_size:
            dealt_cards = [None] * num
        else:
            num = self_size
            dealt_cards = [None] * self_size

        if self_size:
            for n in range(num):
                try:
                    card = ends[end]()
                    dealt_cards[n] = card
                except:
                    break

            return self.__class__(cards=dealt_cards, ranks=self.ranks)
        else:
            return self.__class__(ranks=self.ranks)


    def empty(self, return_cards=False):
        """
        Empties the stack, removing all cards from it, and returns them.

        :arg bool return_cards:
            Whether or not to return the cards.

        :returns:
            If ``return_cards=True``, a list containing the cards removed
            from the Stack.

        """
        cards = list(self.cards)
        self.cards = []

        if return_cards:
            return cards


    def insert(self, card, indice=-1):
        """
        Insert a given card into the stack at a given indice.

        :arg Card card:
            The card to insert into the stack.
        :arg int indice:
            Where to insert the given card.

        """
        self.insert_list([card], indice=indice)


    def insert_list(self, cards, indice=-1):
        """
        Insert a list of given cards into the stack at a given indice.

        :arg list cards:
            The list of cards to insert into the stack.
        :arg int indice:
            Where to insert the given cards.

        """
        self_size = len(self.cards)

        if indice in [0, -1]:
            if indice == -1:
                self.cards += cards
            else:
                self.cards.extendleft(cards)
        elif indice != self_size:
            half_x, half_y = self.split(indice)
            self.cards = list(half_x.cards) + list(cards) + list(half_y.cards)


    def random_card(self, remove=False):
        """
        Returns a random card from the Stack. If ``remove=True``, it will
        also remove the card from the deck.

        :arg bool remove:
            Whether or not to remove the card from the deck. Default: False

        :returns:
            A random Card object, from the Stack.

        """
        i = random.randrange(len(self.cards))
        if not remove:
            card = cards[i]
        else:
            card = self.cards.pop(i)
        return card


    def reverse(self):
        """Reverse the order of the Stack in place."""

        self.cards = self[::-1]


    def set_cards(self, cards):
        """
        Change the Deck's current contents to the given cards.

        :arg list cards:
            The Cards to assign to the stack.

        """
        self.cards = cards


    def shuffle(self, times=1):
        """
        Shuffles the Stack.

        .. note::
            Shuffling large numbers of cards (100,000+) may take a while.

        :arg int times:
            The number of times to shuffle.

        """
        for i in range(times):
            random.shuffle(self.cards)


    @property
    def size(self):
        """
        Counts the number of cards currently in the stack.

        :returns:
            The number of cards in the stack.

        """
        return len(self.cards)


    def sort(self, ranks=None):
        """
        Sorts the stack, either by poker ranks, or big two ranks.

        :arg dict ranks:
            The rank dict to reference for sorting. If ``None``, it will
            default to ``DEFAULT_RANKS``.

        :returns:
            The sorted cards.

        """
        ranks = ranks or self.ranks

        self.cards = sorted(
            self.cards,
            key=cmp_to_key(ranks.compare_rank)
        )
        if ranks.get("values"):
            self.cards = sorted(
                self.cards,
                key=lambda x: ranks["values"][x.value]
            )


    def split(self, indice=None):
        """
        Splits the Stack, either in half, or at the given indice, into two
        separate Stacks.

        :arg int indice:
            Optional. The indice to split the Stack at. Defaults to the middle
            of the ``Stack``.

        :returns:
            The two parts of the Stack, as separate Stack instances.

        """
        num_cards = len(self.cards)

        if indice is None:
            midpoint = num_cards // 2
            return self.__class__(cards=self[0:midpoint]), self.__class__(cards=self[midpoint::])

        elif indice >= num_cards:
            return self.__class__(cards=self.cards), self.__class__()

        elif indice < 0 and abs(indice) >= num_cards:
            return self.__class__(), self.__class__(cards=self.cards)

        elif indice < 0 and abs(indice) <= num_cards:
            return self.__class__(cards=self[indice::]), self.__class__(cards=self[0:abs(indice)])

        else:
            return self.__class__(cards=self[0:indice]), self.__class__(cards=self[indice::])


    def compare(self, cards):
        """
        Checks whether the given ``Stack``, ``Deck``, or ``list`` instance
        contains the same cards (based on value & suit, not instance) as the
        current Stack. Does not take into account the ordering.

        :arg cards:
            The second stack to check. Can be a ``Stack``, ``Deck``, or ``list``
            instance.

        :returns:
            ``True`` or ``False``.
        """

        if isinstance(yours, list):
            yours = deepcopy(cards)
        elif isinstance(yours, Stack):
            yours = deepcopy(cards.cards)
        else:
            raise ValueError('Cannot compare stack. Provided value was not a Stack or list')

        mine = deepcopy(self.cards)

        return sorted(mine) == sorted(yours)


    def convert_to_stack(self, deck):
        """
        Convert a ``Deck`` to a ``Stack``.

        :arg Deck deck:
            The ``Deck`` to convert.

        :returns:
            A new ``Stack`` instance, containing the cards from the given ``Deck``
            instance.

        """
        if isinstance(deck, list):
            return Stack(cards=deck)
        elif getattr(deck, 'cards'):
            return Stack(cards=deck.cards)
        else:
            raise ValueError('Cannot convert to Stack, not a list or a Deck')


    def find_card(self, term):
        """
        Searches the stack for cards with a value, suit, name, or
        abbreviation matching the given argument, ``term``.
    
        :arg str term:
            The search term. Can be a card full name, value, suit,
            or abbreviation.
    
        :returns:
            The first Card to match the search term, if found. Is
            not removed from the Stack
        """

        stack = self.find_cards([term], limit=1)
        if stack:
            return stack.cards[0]

        return False


    def find_cards(self, terms, limit=0, remove=False):
        """
        Searches the given cards for cards with a value, suit, name, or
        abbreviation matching the given argument, ``terms``, optionally
        removing them from the current Stack
    
        :arg list terms:
            The search terms. Can be card full names, suits, values,
            or abbreviations.
        :arg int limit:
            The number of items to retrieve. 0 == no limit.
        :arg bool remove:
            Remove them from the stack as found. Default: False
    
        :returns:
            A Stack containing the cards matching the given terms,
            if found.
    
        """
    
        if not terms:
            raise ValueError('Cannot search for an empty list of terms')

        if limit == 0:
            limit == len(self.cards) + 1

        found_cards = []
        count = 0

        for term in terms:
            for i, card in enumerate(self.cards):
                if card.matches(term) and i not in found_indices:
                    found_cards.append(self.cards.pop(i))
                    count += 1

                if count >= limit:
                    break
    
        if found_cards:
            return self.__class__(cards=found_cards)

        return False
    
    
    def get_card(self, term):
        """
        Get the specified card from the stack. Note, when multiple decks are
        being used in the same stack, this will return only 1 card.
    
        :arg str term:
            The card's full name, value, suit, abbreviation, or stack indice.
    
        :returns:
            The first Card to match the search term, if found.
    
        """
        stack = self.get_cards([term], limit=1)
        if stack:
            return stack.cards[0]

        return False


    def get_list(self, terms, limit=0):
        """
        Get the specified cards from the stack.
    
        :arg list terms:
            A list of card's full names, values, suits, abbreviations, or stack
            indices.
        :arg int limit:
            The number of items to retrieve for each term.
    
        :returns:
            A Stack of the specified cards, if found.
    
        """
        stack = self.find_cards(terms, limit=limit, remove=True)
