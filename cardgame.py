# Card Game API

import random

def fresh_deck():
    suits = {"Spade", "Heart", "Diamond", "Club"}
    ranks = {"A", 2, 3, 4, 5, 6, 7, 8, 9, 10, "J", "Q", "K"}
    deck = []
    for s in suits:
        for r in ranks:
            card = (s, r)
            deck.append(card)
    random.shuffle(deck)
    return deck

# deck = fresh_deck()
# print(deck)

def hit(deck):
    if deck == []:
        deck = fresh_deck()
    return deck[0], deck[1:]

# card, deck = hit(deck)
# print(card)

def count_score(cards):
    score = 0
    number_of_aces = 0
    for card in cards:
        rank = card[1]
        if rank == 'A':
            score += 11
            number_of_aces += 1
        elif rank in {'J', 'Q', 'K'}:
            score += 10
        else:
            score += rank
    while score > 21 and number_of_aces > 0:
        score -= 10
        number_of_aces -= 1
    if score > 21:
        score = 0
    return score

def count_baccarat(cards):
    score = 0
    for card in cards:
        rank = card[1]
        if rank == 'A':
            score = score + 1
        elif rank in {'J', 'Q', 'K'}:
            score = score
        else:
            score += rank
    return score%10

def show_cards(cards, message):
    for card in cards:
        message = message + '\n' + str(card[0]) + ' '+ str(card[1])
    return message

