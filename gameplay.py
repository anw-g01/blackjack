from card_handling import Deck, Hand

WIDTH, CHAR = 50, "-"


class Chips:
    """Represents a player's chips and handles all betting."""
    def __init__(self, starting_chips):
        """
        Initialize the Chips object with a starting value of chips and track betting statistics.

        args:
            starting_chips (int): initial amount of chips the player can cash into the game for all playable rou.

        attributes:
            total (int): total number of chips the player has at current time.
            current_bet (int): value of current bet in the current round.
            total_bets (int): total value of all bets made in all played rounds.
            winnings (int): total value of all bets won in all played rounds.
            losses (int): total value of all bets lost in all played rounds.
            biggest_bet_won (int): value of the biggest bet won in a particular round.
            biggest_bet_loss (int): value of the smallest bet won in a particular round.
        """
        self.total = starting_chips
        self.current_bet = 0
        self.total_bets = 0
        self.winnings = 0
        self.losses = 0
        self.biggest_bet_won = 0
        self.biggest_bet_loss = 0

    def bet_won(self):
        """
        Player receives a multiple of their current round bet after a win in a given round.
        Values of the total chips, total winnings and highest bet win, if applicable, are updated.
        """
        multiplier = 1
        self.total += multiplier * self.current_bet
        self.winnings += self.current_bet
        if self.current_bet > self.biggest_bet_won:
            self.biggest_bet_won = self.current_bet     # update as largest bet

    def bet_lost(self):
        """
        Player loses their current round bet after a loss in a given round.
        Values of the total chips, total losses and highest bet loss, if applicable, are updated.
        """
        self.total -= self.current_bet
        self.losses += self.current_bet
        if self.current_bet > self.biggest_bet_loss:
            self.biggest_bet_loss = self.current_bet


class Blackjack:
    """Represents a simple version of a blackjack game to call and handle gameplay methods accordingly."""

    def __init__(self):
        """
        Initialize a Blackjack game object with a deck of cards, player's and dealer's hands, and chip management.
        Deck, Hand, and Card classes have been defined and programmed within the card_handling.py file.

        Attributes:
            deck (Deck): deck of cards object used in the game.
            hands (dict): dictionary containing objects of the player's and dealer's hands.
            starting_chips (int): initial amount of chips the player cashes-in for all rounds.
            player_chips (Chips): The player's chip management.
            rounds (int): total number of all rounds played in a single game until user quits the command interface.
            player_wins (int): total number of games won by the player.
            blackjacks (int): total number of times the player achieved a blackjack, not including dealer busts.
            pushes (int): total number of games that ended in a tie (push).
            busts (int): total number of rounds that ended with the player busting (hand value exceeding 21)
        """
        self.deck = Deck()  # initialises and shuffles deck
        self.hands = {
            "dealer": Hand(),
            "player": Hand()
        }
        self.starting_chips = self.cash_in()
        self.player_chips = Chips(self.starting_chips)
        self.rounds = 0
        self.player_wins = 0
        self.blackjacks = 0
        self.pushes = 0
        self.busts = 0

    @staticmethod
    def cash_in():
        """Prompts the user to enter the starting chips value for all playable rounds."""
        while True:
            try:
                amount = int(input("\nEnter starting chips: "))
                if amount > 0:
                    return amount
                else:
                    print("Error: negative value.")
            except ValueError:
                print("Error: invalid input.")
        return amount

    def has_chips(self):
        """Returns a quick boolean result checking if the user has sufficient remaining chips."""
        return self.player_chips.total > 0

    def start_round(self):
        """
        Asks the player if they wish to start or continue a new round, given they have sufficient chips remaining.
        has_chips() - will return False if player runs out of chips.
        "y" (yes) -> returns True: continues the same game loop logic for each subsequent round.
        "n" (no) -> returns False: allows the player to cash out.
        """
        if self.has_chips():
            print(f"\n(Total chips: {self.player_chips.total})")
            while True:
                ans = input("\nStart new round? (y/n) ").lower()
                if ans == "y":
                    return True
                elif ans == "n":
                    return False
                print("Error: invalid input.")
        return False

    def handle_bet(self):
        """Manage the player's round bet by checking if the bet is valid and updating chip information accordingly."""
        while True:
            try:
                print(f"\n(Total chips: {self.player_chips.total})")
                player_bet = int(input("\nEnter your bet: "))
                if player_bet < 0:
                    print("Error: negative bet value.")
                elif player_bet > self.player_chips.total:
                    print("Error: bet exceeds available chips.")
                elif player_bet == 0:
                    print("Error: null bet value")
                else:
                    self.player_chips.current_bet = player_bet      # current round player bet
                    self.player_chips.total_bets += player_bet
                    break
            except ValueError:
                print("Error: invalid input.")

    def handle_deck(self):
        """Resets player and dealer hand attributes, and creates a new shuffled deck of cards for a new round."""
        if self.hands["player"].cards:
            for hand in self.hands.values():
                hand.reset_hand()
        self.deck.reinstate_deck()      # re-gather all cards
        self.deck.shuffle_deck()        # shuffle deck

    def first_deal(self):
        """
        Deals the first two initial cards of blackjack to the player and dealer. Uses the adjust_aces() method
        call to adjust the values of aces in the players hands. For two cards, this would only occur in the instance
        that a player is dealt two ace cards whereby the value would be adjusted from 22 to 12.
        """
        for _ in range(2):
            for hand in self.hands.values():
                hand.draw_card(self.deck)
        self.hands["player"].adjust_aces()

    def show_player_hand(self):
        """Displays all cards in the player's hand and its total value"""
        player_hand = self.hands["player"].cards
        print(f"YOU: {', '.join([f'({card.display_card()})' for card in player_hand])}".center(WIDTH))
        print(f"(value: {self.hands['player'].value})".center(WIDTH))

    def show_dealer_upcard(self):
        """Displays only the second card of the dealer during the first two-card deal in blackjack."""
        dealer_hand = self.hands["dealer"].cards
        print(f"DEALER: (??), ({dealer_hand[-1].display_card()})".center(WIDTH))

    def show_dealer_full(self):
        """
        Displays all cards in the dealer's hand and its total value. Used to reveal
        the dealer's hand after the player decides to stand or busts after hitting.
        """
        dealer_hand = self.hands["dealer"].cards
        print(f"DEALER: {', '.join([f'({card.display_card()})' for card in dealer_hand])}".center(WIDTH))
        print(f"(value: {self.hands['dealer'].value})".center(WIDTH))

    def display_table(self, reveal_dealer=False):
        """
        Display the full blackjack game table which are the player's and dealer's hands.
        reveal_dealer (bool) arg used to reveal the dealer's hand after player's turn.
        """
        print("\n" + "".center(WIDTH, CHAR))
        if reveal_dealer:
            self.show_dealer_full()
            print("".center(WIDTH, CHAR))
        else:
            self.show_dealer_upcard()
            print("".center(WIDTH, CHAR))
        self.show_player_hand()
        print("".center(WIDTH, CHAR))

    @staticmethod
    def hit_or_stand():
        """
        Asks the player (user) to hit or stand.
        "h" (hit) -> returns str: will continue the game sub-loop to give the player to hit
        again given they haven't busted.
        "s" (stand) -> returns str: will exit the game sub-loop to finish the player's turn.
        """
        while True:
            action = input("\nHit or stand? (h/s): ").lower()
            if action in ["h", "s"]:
                return action
            print("Error: invalid input.")

    def hit(self):
        """
        Handles the player action of hitting by removing the top card from the deck and adding it to the player's hand.
        """
        player_hand = self.hands["player"]
        player_hand.draw_card(self.deck)
        player_hand.adjust_aces()

    def player_bust(self):
        """
        Checks if the player has busted (total hand value exceeded 21) after each hit action.
        If so, returns True to exit an inner-game loop and terminate the current round.
        """
        if self.hands["player"].value > 21:
            self.rounds += 1
            self.player_chips.bet_lost()
            return True
        return False

    def dealer_draws(self):
        """
        Dealer draws cards, if applicable, until the dealer's hand total is 17 or greater.
        The top card from the deck is dealt to the dealer and the hand is adjusted for aces each draw
        """
        dealer_hand, flag = self.hands["dealer"], False
        while dealer_hand.value < 17:       # dealer must draw cards hand value is 17 or higher:
            dealer_hand.draw_card(self.deck)
            dealer_hand.adjust_aces()
            flag = True
        return flag

    def dealer_bust(self):
        """
        Checks if the dealer busts (hand total exceeding 21) after drawing cards
        until the total hand value was 17 or greater. If so, round is terminated.
        """
        if self.hands["dealer"].value > 21:
            if self.hands["player"].value == 21:
                self.blackjacks += 1
                print("\nDealer busts! You win this round with a blackjack!")
            else:
                print("\nDealer busts! You win this round.")
            print(f"(Chips won: {self.player_chips.current_bet})")
            self.rounds += 1
            self.player_wins += 1
            self.player_chips.bet_won()
            return True
        return False

    def determine_winner(self):
        """
        Compares the total hand values of the player and dealer given both did not bust in the first stage of the game.
        Displays the event and chips outcome for each scenario:
        PUSH -> both hand values were equal.
        WIN -> player's hand value was greater.
        BLACKJACK -> if a WIN outcome was from a hand total of 21 (highest achievable score)
        LOSS -> dealer's hand value was greater.
        Updates the game statistics with chips and no. of rounds played.
        """
        player_score, dealer_score = self.hands["player"].value, self.hands["dealer"].value
        if player_score == dealer_score:    # PUSH
            self.pushes += 1
            if player_score == 21:  # if both scores 21
                print("PUSH! You and the dealer both got 21!")
            else:
                print("\nPUSH! Both hand totals equal.")
            print(f"(Chips returned: {self.player_chips.current_bet})")
        elif player_score > dealer_score:   # WIN
            self.player_chips.bet_won()
            self.player_wins += 1
            if player_score == 21:
                self.blackjacks += 1
                print("\nBLACKJACK! You got 21!")
            else:
                print("\nWIN! You beat the dealer's hand.")
            print(f"(Chips won: {self.player_chips.current_bet})")
        elif player_score < dealer_score:   # LOSS
            self.player_chips.bet_lost()
            if dealer_score == 21:
                print("LOSS! The Dealer got 21!")
            else:
                print("\nLOSS! Dealer's hand is higher")
            print(f"(Chips lost: {self.player_chips.current_bet})")
        self.rounds += 1

    def display_statistics(self):
        """Displays a table of game statistics throughout all played rounds, given at least one round was played."""
        if self.rounds > 0:
            print("\n" + "".center(WIDTH, CHAR))
            print(f"***  GAME STATISTICS  ***".center(WIDTH, CHAR))
            print("" + "".center(WIDTH, CHAR))
            # games played, no. of wins etc. :
            print(f"{CHAR * 2}| Rounds played: {self.rounds} |".ljust(WIDTH, CHAR))
            win_perc = (self.player_wins / self.rounds) * 100    # win percentage
            print(f"{CHAR * 2}| Wins: {self.player_wins} ({win_perc :.1f}%) |".ljust(WIDTH, CHAR))
            print(f"{CHAR * 2}| Blackjacks: {self.blackjacks} |".ljust(WIDTH, CHAR))
            print(f"{CHAR * 2}| Pushes: {self.pushes} |".ljust(WIDTH, CHAR))
            print(f"{CHAR * 2}| Busts: {self.busts} |".ljust(WIDTH, CHAR))
            # bet winnings, returns etc. :
            print("".center(WIDTH, CHAR))
            chips = self.player_chips
            print(f"{CHAR * 2}| Starting chips: {self.starting_chips} |".ljust(WIDTH, CHAR))
            print(f"{CHAR * 2}| Leaving chips: {chips.total} |".ljust(WIDTH, CHAR))
            diff = chips.total - self.starting_chips
            print(f"{CHAR * 2}| Returns: {diff} ({(diff / self.starting_chips) * 100 :.1f}%) |".ljust(WIDTH, CHAR))
            print("".center(WIDTH, CHAR))
            print(f"{CHAR * 2}| Chips bet: {chips.total_bets} |".ljust(WIDTH, CHAR))
            print(f"{CHAR * 2}| Total winnings: {chips.winnings} |".ljust(WIDTH, CHAR))
            print(f"{CHAR * 2}| Biggest win: {chips.biggest_bet_won} |".ljust(WIDTH, CHAR))
            print(f"{CHAR * 2}| Biggest loss: {chips.biggest_bet_loss} |".ljust(WIDTH, CHAR))
            print("" + "".center(WIDTH, CHAR))
