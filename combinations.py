class Combinations:

    def __init__(self):
        self.card_value = dict(zip('2 3 4 5 6 7 8 9 T J Q K A'.split(), range(2, 15)))
        self.all_combinations = {"0": "High Card", "1": "Pair", "2": "Two Pair", "3": "Three of a Kind",
                                 "4": "Straight",
                                 "5": "Flush", "6": "Full House", "7": "Four of a Kind", "8": "Straight Flush",
                                 "9": "Flush Royal"}

    def check_combination(self, hand: list, table: list) -> tuple:
        """Check combination. input: player card, table, return: equal number of combination"""

        card_value = dict(zip('2 3 4 5 6 7 8 9 T J Q K A'.split(), range(2, 15)))
        result = []
        result_suit = []
        for i in hand:
            result.append(i[0])
            result_suit.append(i[1])
        for i in table:
            result.append(i[0])
            result_suit.append(i[1])

        max_suits = max([result_suit.count(i) for i in result_suit])
        card_nums = sorted([card_value[i] for i in result])
        hand_nums = [card_value[i] for i in result[:3]]

        same_cards = []
        rep = []
        for i in result:
            count = result.count(i)
            if i not in rep:
                rep.append(i)
                same_cards.append(count)

        def is_straight(cards):
            diff = cards[-1] - cards[0]
            if diff == 4:
                return True
            elif diff == 12:
                if cards[-2] - cards[0] == 3:
                    return True
            return False

        if max_suits >= 5:
            if is_straight(card_nums):
                if card_nums[0] == 10:
                    return 9, sum(card_nums)
                return 8, sum(card_nums)
            return 5, sum(card_nums)

        elif len(same_cards) == len(result) - 3:
            if max(same_cards) == 4:
                return 7, sum(card_nums)
            elif max(same_cards) == 3:
                return 6, sum(card_nums)
        elif len(same_cards) == len(result) - 2:
            if max(same_cards) == 3:
                return 3, sum(card_nums)
            else:
                return 2, sum(card_nums)
        elif len(same_cards) == len(result) - 1:
            return 1, sum(card_nums)
        else:
            if is_straight(card_nums):
                return 4, sum(card_nums)
            return 0, max(hand_nums)

    def check_players_cards(self, players_profile: dict) -> dict:
        """checking players combination, return dict with players and value of combination"""
        players_hand = {}
        for player in players_profile:
            players_hand[player] = self.card_value[players_profile[player][0][0][0]] + self.card_value[
                players_profile[player][0][1][0]]
        return players_hand

    def check_players_combinations(self, players_hand: dict) -> dict:
        """return all players combinations"""
        players_combinations = {}
        for players in players_hand:
            players_combinations[players] = self.all_combinations[str(players_hand[players][0])]
        return players_combinations

    def winner(self, players_hand: dict) -> list:
        """define the winner by combination value and value of hand and table"""
        winners = ["winner", "0", "0"]
        winner_with_combination = []
        for player, value in players_hand.items():
            if value[0] > int(winners[1]):
                winners[0] = player
                winners[1] = str(value[0])
                winners[2] = str(value[1])
        for player, value in players_hand.items():
            if value[0] == int(winners[1]) and value[1] > int(winners[2]):
                winners[0] = player
                winners[1] = str(value[0])
                winners[2] = str(value[1])
        winner_with_combination.append(winners[0])
        winner_with_combination.append(self.all_combinations[str(winners[1])])
        return winner_with_combination


