import random

SUIT_HEARTS = "Hearts"
SUIT_DIAMONDS = "Diamonds"
SUIT_CLUBS = "Clubs"
SUIT_SPADES = "Spades"

class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
    
    def get_score(self):
        score = self.rank
        match self.rank:
            case 1: score = 11
            case 11: score = 10
            case 12: score = 10
            case 13: score = 10
        return score

    def __str__(self):
        rank_name = self.rank
        match self.rank:
            case 1: rank_name = "Ace"
            case 11: rank_name = "Jack"
            case 12: rank_name = "Queen"
            case 13: rank_name = "King"
        return f"{rank_name} of {self.suit}"

deck = []
my_hand = []

for suit in [SUIT_HEARTS, SUIT_DIAMONDS, SUIT_CLUBS, SUIT_SPADES]:
    for i in range(13):
        card = Card(suit, i + 1)
        deck.append(card)

random.shuffle(deck)

def draw(amount):
    for i in range(amount):
        selected_card = deck.pop(0)
        my_hand.append(selected_card)

draw(2)

my_hand = sorted(my_hand, key=lambda card: card.rank)

def show_hand():
    score = 0
    for c in my_hand:
        print(c)
        score = score + c.get_score()
    print(f"Score: {score}")

show_hand()

if my_hand[0].rank == 1:
    # first is ace
    if my_hand[1].rank >= 10:
        print("Black Jack!")