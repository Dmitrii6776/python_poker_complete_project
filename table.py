import random


class Table:

    def build_deck(self) -> list:
        """build deck of 52 card"""
        cards = [card for card in range(2, 10)]
        suits = ["♠", "♤", "♡", "♥", "♣", "♧", "♢", "♦"]
        characters = ["T", "J", "Q", "K", "A"]
        all_cards = []
        for card in cards:
            for suit in suits:
                all_cards.append(f"{card}{suit}")

        for character in characters:
            for suit in suits:
                all_cards.append(f"{character}{suit}")
        return all_cards

    def get_card(self, deck: list) -> str:
        """return 1 random card from deck, cards do not repeat"""
        issued_cards = []
        card = random.choice(deck)
        if card not in issued_cards:
            issued_cards.append(card)
            return card
        else:
            self.get_card(deck)

    def bank(self, bank: int, bet_dict: dict) -> int:
        """summarise the players bet, returned total amount"""
        for bet in bet_dict:
            if bet_dict[bet] == 'fold':
                continue
            bank += int(bet_dict[bet])
        return bank

