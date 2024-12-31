# WITH UI

import tkinter as tk
from tkinter import messagebox
import random

# Add card suits here for reference
HEARTS   = chr(9829) # '♥'
DIAMONDS = chr(9830) # '♦'
SPADES   = chr(9824) # '♠'
CLUBS    = chr(9827) # '♣'
BACKSIDE = 'backside'

def main():
    # Initialize the main game window
    root = tk.Tk()
    root.title("Blackjack")
    root.geometry("800x600")
    app = BlackjackApp(root)
    root.mainloop()

class BlackjackApp:
    def __init__(self, root):
        self.root = root
        self.money = 5000  # Starting money for the player
        self.bet = 0
        self.deck = []
        self.dealer_hand = []
        self.player_hand = []
        self.create_widgets()
        self.reset_game()

    def create_widgets(self):
        # Create and position widgets like labels, buttons, and text areas
        self.title_label = tk.Label(self.root, text="♥♦♣♠ BLACKJACK ♠♣♦♥", font=("Consolas", 24, "bold"))
        self.title_label.pack(pady=10)

        self.rules_label = tk.Label(self.root, text=(
            "Rules:\n"
            "§ Try to get as close to 21 without going over.\n"
            "§ Kings, Queens, Jacks = 10 points; Aces = 1 or 11 points.\n"
            "§ (H)it to draw a card, (S)tand to stop.\n"
            "§ On first play, you can (D)ouble down to increase your bet."
        ), justify="left", font=("Consolas", 12))
        self.rules_label.pack()

        self.money_label = tk.Label(self.root, text=f"Money: ${self.money}", font=("Consolas", 16))
        self.money_label.pack(pady=10)

        self.bet_label = tk.Label(self.root, text="Place your bet:", font=("Consolas", 12))
        self.bet_label.pack()

        self.bet_entry = tk.Entry(self.root, font=("Consolas", 12), width=10)
        self.bet_entry.pack()

        self.bet_button = tk.Button(self.root, text="Place Bet", font=("Consolas", 12), command=self.start_game)
        self.bet_button.pack(pady=5)

        self.cards_frame = tk.Frame(self.root)
        self.cards_frame.pack(pady=10)

        self.player_label = tk.Label(self.cards_frame, text="Player's Hand:", font=("Consolas", 14))
        self.player_label.grid(row=0, column=0, padx=10)

        self.dealer_label = tk.Label(self.cards_frame, text="Dealer's Hand:", font=("Consolas", 14))
        self.dealer_label.grid(row=0, column=1, padx=10)

        self.player_cards = tk.Label(self.cards_frame, text="", font=("Consolas", 14))
        self.player_cards.grid(row=1, column=0, padx=10)

        self.dealer_cards = tk.Label(self.cards_frame, text="", font=("Consolas", 14))
        self.dealer_cards.grid(row=1, column=1, padx=10)

        self.action_frame = tk.Frame(self.root)
        self.action_frame.pack(pady=10)

        self.hit_button = tk.Button(self.action_frame, text="Hit", font=("Consolas", 12), command=self.hit)
        self.hit_button.grid(row=0, column=0, padx=5)

        self.stand_button = tk.Button(self.action_frame, text="Stand", font=("Consolas", 12), command=self.stand)
        self.stand_button.grid(row=0, column=1, padx=5)

        self.double_button = tk.Button(self.action_frame, text="Double Down", font=("Consolas", 12), command=self.double_down)
        self.double_button.grid(row=0, column=2, padx=5)

    def reset_game(self):
        self.bet = 0
        self.deck = getDeck()
        self.dealer_hand = [self.deck.pop(), self.deck.pop()]
        self.player_hand = [self.deck.pop(), self.deck.pop()]
        self.update_display()
        self.bet_button.config(state=tk.NORMAL)
        self.bet_entry.config(state=tk.NORMAL)
        self.hit_button.config(state=tk.DISABLED)
        self.stand_button.config(state=tk.DISABLED)
        self.double_button.config(state=tk.DISABLED)

    def update_display(self):
        # Update displayed cards and money
        self.money_label.config(text=f"Money: ${self.money}")
        self.player_cards.config(text=self.format_hand(self.player_hand))
        self.dealer_cards.config(text="???, " + self.format_hand(self.dealer_hand[1:]))

    def format_hand(self, hand):
        return ", ".join(f"{rank}{suit}" for rank, suit in hand)

    def start_game(self):
        try:
            bet = int(self.bet_entry.get())
            if bet <= 0 or bet > self.money:
                raise ValueError
            self.bet = bet
            self.money -= bet
            self.update_display()
            self.bet_button.config(state=tk.DISABLED)
            self.bet_entry.config(state=tk.DISABLED)
            self.hit_button.config(state=tk.NORMAL)
            self.stand_button.config(state=tk.NORMAL)
            self.double_button.config(state=tk.NORMAL)
        except ValueError:
            messagebox.showerror("Invalid Bet", "Please enter a valid bet amount.")

    def hit(self):
        new_card = self.deck.pop()
        self.player_hand.append(new_card)
        self.update_display()

        if getHandValue(self.player_hand) > 21:
            messagebox.showinfo("Bust", "You went over 21! You lose.")
            self.money -= self.bet  # Player loses the bet
            self.end_round()
        else:
            # Keep allowing the player to hit
            pass

    def stand(self):
        self.dealer_turn()
        self.compare_hands()

    def double_down(self):
        new_bet = self.bet
        if self.money >= new_bet:
            self.bet *= 2
            self.money -= new_bet
            new_card = self.deck.pop()
            self.player_hand.append(new_card)
            self.update_display()
            self.dealer_turn()
            self.compare_hands()
        else:
            messagebox.showerror("Error", "You don't have enough money to double down.")

    def dealer_turn(self):
        # Dealer's turn: draw cards until the dealer has 17 or more
        while getHandValue(self.dealer_hand) < 17:
            self.dealer_hand.append(self.deck.pop())
            self.update_display()

    def compare_hands(self):
        player_value = getHandValue(self.player_hand)
        dealer_value = getHandValue(self.dealer_hand)

        if dealer_value > 21:
            messagebox.showinfo("Dealer Busts", f"Dealer busts! You win ${self.bet}")
            self.money += self.bet
        elif player_value > 21:
            messagebox.showinfo("You Bust", "You bust! You lose.")
            self.money -= self.bet
        elif player_value > dealer_value:
            messagebox.showinfo("You Win", f"You win ${self.bet}")
            self.money += self.bet
        elif player_value < dealer_value:
            messagebox.showinfo("You Lose", "You lose!")
            self.money -= self.bet
        else:
            messagebox.showinfo("Tie", "It's a tie! Your bet is returned.")

        self.end_round()

    def end_round(self):
        self.reset_game()


# Blackjack helper functions (e.g., getDeck, getHandValue) go here

def getDeck():
    """Returns a shuffled deck of cards."""

    deck = []
    for suit in (HEARTS, DIAMONDS, SPADES, CLUBS):
        for rank in range(2, 11):
            deck.append((str(rank), suit))  # Add the numbered cards.
        for rank in ('J', 'Q', 'K', 'A'):
            deck.append((rank, suit))  # Add the face and ace cards.
    random.shuffle(deck)
    return deck


def getHandValue(cards):
    """Returns the value of the cards. Face cards are worth 10, aces are worth 11 or 1."""

    value = 0
    number_of_aces = 0

    for card in cards:
        rank = card[0]
        if rank == 'A':
            number_of_aces += 1
        elif rank in ('K', 'Q', 'J'):
            value += 10
        else:
            value += int(rank)

    for _ in range(number_of_aces):
        if value + 11 <= 21:
            value += 11
        else:
            value += 1

    return value


if __name__ == '__main__':
    main()