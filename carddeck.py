import random


def get_deck_value(deck):
    table = {"2": [2, 2], "3": [3, 3], "4": [4, 4], "5": [5, 5], "6": [6, 6], "7": [7, 7], "8": [8, 8],
             "9": [9, 9], "10": [10, 10], "J": [10, 10], "Q": [10, 10], "K": [10, 10], "A": [1, 10]}

    total_value = 0
    num_aces = 0
    for card in deck:
        value = table[card[1]][0]

        if card[1] == 'A':
            num_aces += 1

        total_value += value

    while num_aces > 0 and total_value + 10 <= 21:
        total_value += 10
        num_aces -= 1

    return total_value


class Carddeck:
    def __init__(self):
        liste = list()
        for name in ["Pik", "Karo", "Kreuz", "Herz"]:
            for value in ["2", "3", "4", "5", "6", "7", "8", "9", "J", "Q", "K", "A"]:
                liste.append([name, value])
        self.cards = liste

    def get_cards(self):
        return self.cards

    def shuffle(self):
        random.shuffle(self.cards)

    def take(self):
        value = self.cards.pop(0)
        return value
