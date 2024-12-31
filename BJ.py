# Just a simple blackjack sript
#Just run and after the game is over you will have to restart
# Gotta add a way to give an option to restart the game afterwards
import random

class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

    def __str__(self):
        return f"{self.rank['rank']} of {self.suit}"


class Deck:
    def __init__(self):
        self.cards = []
        suits = ["hearts", "clubs", "spades", "diamonds"]
        ranks = [
            {"rank": "2", "value": 2},
            {"rank": "3", "value": 3},
            {"rank": "4", "value": 4},
            {"rank": "5", "value": 5},
            {"rank": "6", "value": 6},
            {"rank": "7", "value": 7},
            {"rank": "8", "value": 8},
            {"rank": "9", "value": 9},
            {"rank": "10", "value": 10},
            {"rank": "Jack", "value": 10},
            {"rank": "Queen", "value": 10},
            {"rank": "King", "value": 10},
            {"rank": "Ace", "value": 11},  # Can also be 1 depending on the game
        ]
        for suit in suits:
            for rank in ranks:
                self.cards.append(Card(suit, rank))

    def shuffle(self):
        if len(self.cards) > 1:
            random.shuffle(self.cards)

    def deal(self, number):
        cards_dealt = []
        for _ in range(number):
            if len(self.cards) > 0:
                card = self.cards.pop()
                cards_dealt.append(card)
        return cards_dealt


class Hand:
    def __init__(self, dealer=False):
        self.cards = []
        self.value = 0
        self.dealer = dealer

    def add_card(self, card_list):
        self.cards.extend(card_list)

    def calculate_value(self):
        self.value = 0
        has_ace = False

        for card in self.cards:
            card_value = int(card.rank["value"])
            self.value += card_value
            if card.rank["rank"] == "Ace":
                has_ace = True

        if has_ace and self.value > 21:
            self.value -= 10

    def get_value(self):
        self.calculate_value()
        return self.value

    def is_blackjack(self):
        return self.get_value() == 21

    def display(self, show_all_dealer_cards=False):
        print(f'''{"Dealer's" if self.dealer else "Your"} Hand:''')
        for index, card in enumerate(self.cards):
            if index == 0 and self.dealer and not show_all_dealer_cards:
                print("hidden")
            else:
                print(card)

        if not self.dealer:
            print("Value:", self.get_value())
        print()


class Game:
    def check_winner(self, player_hand, dealer_hand, game_over=False):
        if not game_over:
            if player_hand.get_value() > 21:
                print("You Busted. Dealer Wins")
                return True
            elif dealer_hand.get_value() > 21:
                print("Dealer Busted. You Win!!")
                return True
            elif dealer_hand.is_blackjack() and player_hand.is_blackjack():
                print("You Both have Blackjack. Push")
                return True
            elif player_hand.is_blackjack():
                print("Blackjack!!! You win!!")
                return True
            elif dealer_hand.is_blackjack():
                print("Dealer has Blackjack!!! You lose!!")
                return True
        else:
            if player_hand.get_value() > dealer_hand.get_value():
                print("You Win!!")
            elif player_hand.get_value() == dealer_hand.get_value():
                print("It's a Tie! Push")
            else:
                print("Dealer Wins.")
            return True
        return False

    def play(self):
        game_number = 0
        games_to_play = 0

        # Ask the user how many games to play
        while games_to_play <= 0:
            try:
                games_to_play = int(input("How many games would you like to play? "))
            except ValueError:
                print("You must enter a valid number.")

        # Loop for each game
        while game_number < games_to_play:
            game_number += 1

            # Initialize deck and hands
            deck = Deck()
            deck.shuffle()

            player_hand = Hand()
            dealer_hand = Hand(dealer=True)

            for _ in range(2):
                player_hand.add_card(deck.deal(1))
                dealer_hand.add_card(deck.deal(1))

            print()
            print("*" * 30)
            print(f"Game {game_number} of {games_to_play}")
            print("*" * 30)
            player_hand.display()
            dealer_hand.display()

            # Check for winner after dealing initial cards
            if self.check_winner(player_hand, dealer_hand):
                continue

            # Player's turn
            while player_hand.get_value() < 21:
                choice = input("Would you like to 'Hit' or 'Stand': ").lower()
                if choice in ["hit", "h"]:
                    player_hand.add_card(deck.deal(1))
                    player_hand.display()
                elif choice in ["stand", "s"]:
                    break
                else:
                    print("Invalid input. Please choose 'Hit' or 'Stand'.")

            # Check for winner after player's turn
            if self.check_winner(player_hand, dealer_hand):
                continue

            # Dealer's turn
            while dealer_hand.get_value() < 17:
                dealer_hand.add_card(deck.deal(1))

            dealer_hand.display(show_all_dealer_cards=True)

            # Final check for winner
            if self.check_winner(player_hand, dealer_hand):
                continue

            # Display final results
            print("Final Results")
            print("Your Hand:", player_hand.get_value())
            print("Dealer's Hand:", dealer_hand.get_value())
            self.check_winner(player_hand, dealer_hand, True)

        print("Thanks for playing!")


# Start the game
g = Game()
g.play()
