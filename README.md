# Blackjack with Python

A simple command-line-based implementation of the classic card game Blackjack. It allows the user to play successive rounds of Blackjack against a computer dealer until they lose all their chips or decide to cash out. The program keeps track of a highly in-depth game statistics displayed after the end of a game. The current project is a simplified version of Blackjack and does not implement further gameplay options such as splitting pairs or doubling down.

## Project Files
1. `main.py`: Orchestrates the entire game by utilizing the defined classes and calling necessary methods to create the classic flow of Blackjack.
2. `gameplay.py`: Defines the main blackjack class housing the necessary game logic as well as a chips class for handling betting.
3. `card_handling.py`: Defines essential classes for cards, decks, and hands. Houses all class methods and attributes related to card handling.
4. `playing_cards.py`: File containing tuples of card-related data (suits and ranks), and a dictionary to map all ranks to an associated value (see game rules).

## Game Objectives
1. The objective of the game is to get your hand value as close to 21, but not exceed it, otherwise, you **BUST**.
2. If you decide to stop drawing (**HIT**) more cards, you **STAND** and must beat the dealer's hand value to win.
3. If you reach a hand value of 21, you don't win immediately; you can still tie (**PUSH**) if the dealer also has or reaches 21 during their turn.

## Game Rules
1. Number cards (2-10) are worth their face value and face cards (J, Q, K) are all worth 10 points.
2. Aces are initially worth 11 points but can change their value to 1 point if the total hand value exceeds 21 (i.e. to prevent a bust).
3. If your hand value exceeds 21, you bust and lose the round immediately, irrespective of the dealer's hand.
4. The dealer will keep drawing cards if their hand value is below 17. If they bust during this process, you will win the round.
5. During the player's turn to hit or stand, only the dealer's second card is displayed.

## How To Play
1. Run the game by executing the `main.py` file.
2. The game will prompt you to cash-in with a starting number of chips.
3. Follow the on-screen instructions to place bets and hit or stand.play successive Blackjack rounds until you either lose all your chips or decide to cash out.
4. Gameplay includes 





