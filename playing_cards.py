suits = (
    "♥",    # hearts
    "♦",    # diamonds
    "♠",    # spades
    "♣"     # clubs
)

ranks = (
    "2",
    "3",
    "4",
    "5",
    "6",
    "7",
    "8",
    "9",
    "10",
    "J",
    "Q",
    "K",
    "A"
)

values = {
    "2": 2,
    "3": 3,
    "4": 4,
    "5": 5,
    "6": 6,
    "7": 7,
    "8": 8,
    "9": 9,
    "10": 10,
    "J": 10,    # all face cards have value 10 in blackjack
    "Q": 10,
    "K": 10,
    "A": 11     # aces can change to value 1 if hand value exceeds 21
}               # refer to "adjust_aces()" method in card_handling.py
