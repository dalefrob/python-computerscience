from enum import Enum
import random

STATE_WAITING = 0
STATE_STAY = 1
STATE_BUST = 2
STATE_BLACKJACK = 3
STATE_WIN = 4
STATE_LOSE = 5

class Suit(Enum):
    HEARTS = 0
    DIAMONDS = 1
    SPADES = 2
    CLUBS = 3

class Rank(Enum):
    ACE = 1
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6
    SEVEN = 7
    EIGHT = 8
    NINE = 9
    TEN = 10
    JACK = 11
    QUEEN = 12
    KING = 13

suitimage = {
    Suit.DIAMONDS: "♦",
    Suit.HEARTS: "♥",
    Suit.SPADES: "♠",
    Suit.CLUBS: "♣"
}

class Card:
    def __init__(self, suit : Suit, rank : Rank):
        self.suit = suit    
        self.rank = rank
        self.value = int(self.rank.value)
        if self.value > 10:
            self.value = 10
        elif self.rank == Rank.ACE: # ACE
            self.value = 11

    def __str__(self):
        return f"{self.rank.name}({self.value}) of {suitimage[self.suit]}" #####


class Player:
    def __init__(self, name = "Default", dealer = False):
        self.name = name
        self.is_dealer = dealer
        self.money = 100
        self.hand : list[Card] = []
        self.state = STATE_WAITING
    
    def draw(self, amount = 1):
        drawstring = f"{self.name} draws: "
        for i in range(amount):
            card = deck.pop(0)
            drawstring += f"{card}, "
            self.hand.append(card)
        print(drawstring)
    
    def getTotalCardValue(self) -> int:
        return add_card_values(self.hand)   ######


deck : list[Card] = []

for suit in Suit:
    for rank in Rank:
        new_card = Card(suit, rank)
        deck.append(new_card)


# ENTRY POINT

player = Player("Bob")
player2 = Player("Harry")
dealer = Player("Dealer", True)
allplayers : list[Player] = [player, player2, dealer]


def add_card_values(cards : list[Card]) -> int:
    total = 0
    for c in cards:
        total += c.value
    return total

# Game loop
random.shuffle(deck)

for p in allplayers:
    p.draw(2)
    p.state = STATE_WAITING

# players_staying : list[Player] = []
players_staying = {}

def checkForWin(player : Player) -> bool:
    return add_card_values(player.hand) == 21

def checkForBust(player : Player) -> bool:
    return add_card_values(player.hand) > 21

def getDealerMove():
    _choice = "S"
    for p in players_staying:
        if dealer.getTotalCardValue() < p.getTotalCardValue():
            _choice = "H"
            break
    return _choice

# LOOP THROUGH ALL PLAYERS - Going around the table
for p in allplayers:
    while p.state == STATE_WAITING:
        # Check for win
        if checkForWin(p):
            p.state = STATE_WIN
            continue
        
        choice = "S"

        # Ask player for choice
        if not p.is_dealer:
            choice = str(input(f"{p.name}: (H)it or (S)tay?"))
        else:
            choice = getDealerMove()

        match choice.capitalize():
            case "H":
                print(f"{p.name} Hits!")
                p.draw(1)
                if checkForBust(p):
                    p.state = STATE_BUST
                    print(f"{p.name} Busts! Total:{p.getTotalCardValue()}")
                elif checkForWin(p):
                    p.state = STATE_WIN
                    print(f"{p.name} got 21! Total:{p.getTotalCardValue()}")
            case "S":
                print(f"{p.name} Stays")
                p.state = STATE_STAY
                players_staying[p] = p.getTotalCardValue()
            case _:
                pass

# CHECK STAYERS
for sp in players_staying:
    print(f"{sp.name}: {sp.getTotalCardValue()}")