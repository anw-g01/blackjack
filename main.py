from gameplay import Blackjack
import os


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


def main():
    clear_screen()
    game = Blackjack()  # 1. user cashes in with starting chips
    clear_screen()

    while game.start_round():  # 2. user starts/continues round (given sufficient chips) or cashes-out
        clear_screen()
        game.handle_bet()  # 3. user places round bet

        clear_screen()
        game.handle_deck()  # 4. creates and new shuffled deck for a new round
        game.first_deal()  # 5. two cards dealt to player and dealer

        clear_screen()
        print("\nShuffling and dealing cards...")
        game.display_table()  # 6. display player hand with dealer's upcard

        # ====== PLAYER'S TURN ====== #
        while True:
            action = game.hit_or_stand()  # 7. player gets decision to hit (until busting) or stand
            if action == "h":
                game.hit()
                clear_screen()
                game.display_table()

                busted = game.player_bust()
                if busted:  # 8. if player busted during hitting, round is lost
                    break
            else:
                busted = False
                break  # player stands

        # ====== DEALER'S TURN ====== #
        if not busted:  # 9. after player stands, dealer manages their cards
            clear_screen()
            print("\nRevealing dealer's hand... ")
            game.display_table(reveal_dealer=True)  # 10. reveal dealer's hidden card

            if game.dealer_draws():  # 11. if permitted, dealer must draw cards until their hand is at least 17
                clear_screen()
                print("\nDealer's hand total below 17.\nDealer drawing cards...")
                game.display_table(reveal_dealer=True)  # display all cards across the table

            if game.dealer_bust():  # 12. whilst drawing cards, if dealer busts then player wins
                pass
            else:
                # ====== COMPARE HAND TOTALS ====== #
                game.determine_winner()  # 13. given no one busts, card hand totals are compared
        # 14. round complete, back to the start of the first "while" loop

        else:  # if player has busted (result from hitting loop)
            clear_screen()
            game.display_table(reveal_dealer=True)
            print("\nBUST! Your hand exceeded 21.")
            print(f"(Chips lost: {game.player_chips.current_bet})")

    if not game.has_chips():  # 14. game is over if user runs out of chips
        print("\nGame over. You ran out of chips.")

    # GAME OVER
    game.display_statistics()  # 15. game statistics are displayed if user quits or loses after at least one game
    print("\nThanks for playing!")


if __name__ == "__main__":
    main()
