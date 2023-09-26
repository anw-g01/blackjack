
import random
from playing_cards import suits, ranks, values  # import data from playing_cards.py


class Card:
    """Represents a single playing card with a rank, suit, and assigned value associated in Blackjack."""

    def __init__(self, card_rank, card_suit):
        """
        args:
            card_rank (str): rank of the card (e.g., '2', 'A', 'K').
            card_suit (str): suit of the card (e.g., '♥' for Hearts).

        attributes:
            rank (str): rank of the card.
            suit (str): suit of the card.
            value (int): numerical value assigned to the card.
        """
        self.rank = card_rank
        self.suit = card_suit
        self.value = values[card_rank]

    def display_card(self):
        """
        Returns a single card display in the format 'RankSuit' (e.g. '2♥' for the 'Two of Hearts')
        Used for debugging purposes - see display_deck() method within Deck class.
        """
        return f"{self.rank}{self.suit}"


class Deck:
    """Represents a full 52-deck of playing cards. """

    def __init__(self):
        """Initializes a Deck object as an empty list of cards."""
        self.cards = []

    def reinstate_deck(self):
        """Resets a given deck object of all cards and reinstates the full deck in order."""
        self.cards = []
        for suit in suits:
            for rank in ranks:
                self.cards.append(Card(rank, suit))  # add to cards list

    def shuffle_deck(self):
        """Shuffles the deck of cards in-place using shuffle() from the built-in random module."""
        random.shuffle(self.cards)

    def deal_card(self):
        """Removes (in-place) and returns the top card from the deck, to be dealt to a given hand."""
        return self.cards.pop()

    def display_deck(self):
        """
        Displays the state of all present cards on a deck in a line. Prints a
        comma-separated list of cards present in a deck - used for debugging.
        """
        print(f"\nCurrently {len(self.cards)} card(s) in the deck.")
        print(", ".join([card.display_card() for card in self.cards]))


class Hand:
    """Represents a player's or dealer's hand of playing cards in Blackjack."""

    def __init__(self):
        """
        attributes:
            cards (list): list of dealt cards representing a given hand (player or dealer).
            aces (int): number of aces present in a hand with value 11 - used in adjust_aces() method.
            value (int): total sum of a given hand in Blackjack.
            adjusted (bool): flag variable to signify if a hand has been adjusted for aces.
        """
        self.cards = []
        self.aces = 0
        self.value = 0

    def reset_hand(self):
        """Resets the hand, clearing cards and resetting attributes for the start of a new round"""
        self.cards = []
        self.aces = 0
        self.value = 0

    def display_hand(self):
        """
        Displays all present cards in a given hand. Prints a
        comma-separated list of cards in a single line - for debugging.
        """
        print(f"\nCurrently {len(self.cards)} cards in hand with {self.aces} 11-value aces.")
        print(f"Total value: {self.value} (adjusted: {self.adjusted})")
        print(", ".join([card.display_card() for card in self.cards]))

    def draw_card(self, card_deck):
        """
        Adds a card to a given hand from a specified card deck and updates the hand's value.

        args:
            card_deck (Deck): deck object from which to draw a card.
        """
        card = card_deck.deal_card()     # take card from a given deck
        self.cards.append(card)     # add to hand's cards list (hand)
        self.value += card.value    # update hand value
        if card.rank == "A":
            self.aces += 1

    def adjust_aces(self):
        """
        Adjusts the value of a given hand by checking if the hand value has exceeded 21 and
        whether one or more ace cards are present. If so, it deducts hand value by 10 for each ace
        card adjust to prevent busting, i.e. equivalent to changing an ace card's value from 11 to 1.
        """
        while self.aces > 0 and self.value > 21:
            self.value -= 10    # equivalent to ace card value changing to 1
            self.aces -= 1      # keep track of aces with value 11
