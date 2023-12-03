class Player:
    def __init__(self, name, money=0):
        self.player_name = name
        self.player_balance = money
        self.card_list = list()

    def get_balance(self):
        return self.player_balance

    def get_name(self):
        return self.player_name

    def add_card(self, list_of_card):
        return self.card_list.append(list_of_card)

    def add_money(self, value):
        if value < 0:
            return "Error, below 0"
        self.player_balance += value

    def remove_money(self, value):
        if value < 0:
            return "Error, below 0"
        if value > self.player_balance:
            return "Error, balance too low"
        self.player_balance -= value

    def get_cards(self):
        return self.card_list

    def get_cards_value(self):
        cards_value = 0
        for liste in self.card_list:
            cards_value += liste[1]
        return cards_value

    def is_dead(self):
        return self.get_cards_value() > 21

    def is_under_16(self):
        return self.get_cards_value() < 16
