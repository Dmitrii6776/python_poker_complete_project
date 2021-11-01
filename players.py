from table import Table
from combinations import Combinations
import time
import random

table = Table()
comb = Combinations()


class Players:
    def build_players(self, quantity_players: int, name_of_user: str) -> list:
        """create list of players include user"""
        players = [name_of_user]
        for player in range(quantity_players):
            players.append(f"player{player}")
        return players

    def players_prifile(self, balance: int, players: list) -> dict:
        """create player_profile, return dict of profiles"""
        players_profiles = {}
        for player in players:
            players_profiles[player] = [[], {"balance": balance}]
        return players_profiles

    def players_with_cards(self, players_profile: dict, deck) -> dict:
        """distributes 2 cards to each player"""
        for player in players_profile:
            for card in range(2):
                players_profile[player][0].append(table.get_card(deck))
        return players_profile

    def blinds(self, balance: int, round_circle: int, players: list) -> dict:
        """return tuple with small blind and big blind: ((player, sb), (player, bb))"""
        blinds_bet = {}
        if round_circle == 0:
            small_blind = int(input(f"Please make your blind equal {balance / 10}$"))
            big_blind = balance / 5
        elif round_circle == len(players) - 1:
            small_blind = balance / 10
            big_blind = int(input(f"Please make your blind equal {balance / 5}$"))
        else:
            small_blind = balance / 10
            big_blind = balance / 5
        print(f"{players[round_circle]} make a small blind {small_blind}$\n"
              f"{players[round_circle + 1]} make a big blind {big_blind}$")
        for player in players:
            if player == players[round_circle]:
                blinds_bet[player] = small_blind
            elif player == players[round_circle + 1]:
                blinds_bet[player] = big_blind
            else:
                blinds_bet[player] = 0

        return blinds_bet

    def make_bet(self, bet_dict: dict, players_profile: dict) -> dict:
        """minus the bet from balance, delete players was folded, returned players profile"""
        for player in bet_dict:
            if bet_dict[player] == "fold":
                del players_profile[player]
                continue
            elif bet_dict[player] == 'check':
                continue
            else:
                bet = bet_dict[player]
                players_profile[player][1]['balance'] -= int(bet)

        return players_profile

    def get_info(self, bank: int, players_profile: dict, cards_on_table: list, name: str):
        """return info: bank, balance, cards on table"""
        if name in players_profile:
            if len(cards_on_table) == 0:
                print(f"{name}`s cards{players_profile[name][0]}, balance: {players_profile[name][1]['balance']}$")
            else:
                print(f"{name}`s cards{players_profile[name][0]}, balance: {players_profile[name][1]['balance']}$\n"
                      f"cards on table: {cards_on_table}\n"
                      f"bank: {bank}")
        else:
            print(f"cards on table: {cards_on_table}\n"
                  f"bank: {bank}")

    def check_bet_blind_round(self, name: str, players_hand: dict, blinds: dict, big_blind: float,
                              small_blind: float) -> dict:
        """returned dict of players with bets in blind round"""
        players_bet = {}
        max_bet = big_blind
        min_bet = small_blind

        for player in players_hand:
            time.sleep(random.randint(1, 3))
            if blinds[player] == min_bet:
                players_bet[player] = min_bet
            elif blinds[player] == max_bet:
                players_bet[player] = max_bet
            elif players_hand[player] <= 5:
                players_bet[player] = "fold"
                print(f"{player} just fold")
            elif max_bet > big_blind:
                players_bet[player] = max_bet
                print(f"{player} equalized the bet to {max_bet}$")
            else:
                players_bet[player] = max_bet
                print(f"{player} equalized the bet to {max_bet}$")

        for player in players_bet:

            if player == name and players_bet[player] < max_bet:
                user_bet = input(f"Please make your bet equal {max_bet - min_bet}$: ")
                players_bet[player] = user_bet
            elif players_bet[player] == 'fold':
                continue
            elif players_bet[player] < max_bet:
                players_bet[player] = max_bet - min_bet
        return players_bet

    def check_combination(self, players_profile: dict, cards_on_table: list) -> dict:
        """check players hand combination, returned dict of players combinations with value of combinations"""
        combination_value = {}
        for player in players_profile:
            combination_value[player] = comb.check_combination(players_profile[player][0], cards_on_table)

        return combination_value

    def players_move(self, players_hand: dict, min_bet: float, name: str, round_circle) -> dict:
        """make bet in flop, tern and final rounds by players hand with value of combination,
        returned dict of players bet"""
        players_bet = {key: 0 for key in players_hand}
        players_list = list(players_hand.keys())
        players_after_blinds = players_list[round_circle + 2::]
        players_without_user = players_list[1::]
        max_bet = int(min_bet)
        check = True

        def check_bet(check: bool, players_bet: dict, players_list: list, max_bet: int) -> tuple:
            """check players bet among users after blinds, return dict with bets"""
            for player in players_list:
                time.sleep(random.randint(1, 3))
                if players_bet[player] == "fold":
                    continue
                elif players_bet[player] == 'check' and not check:
                    players_bet[player] = max_bet
                elif 0 <= int(players_hand[player][0]) <= 2 and max_bet > min_bet * 2 and not check:
                    players_bet[player] = 'fold'
                    print(f"{player} just fold")

                elif players_bet[player] == max_bet:
                    continue
                elif players_hand[player][0] == 0 and players_hand[player][1] <= 7:
                    if check:
                        players_bet[player] = 'check'
                        print(f"{player}: check")
                    else:
                        players_bet[player] = "fold"
                        print(f"{player} just fold")

                elif 1 < int(players_hand[player][0]) == 1:
                    if check:
                        players_bet[player] = 'check'
                        print(f"{player}: check")
                    elif players_bet[player] < max_bet:
                        players_bet[player] = max_bet - players_bet[player]
                        check = False
                        print(f"{player} equalized the bet to {max_bet}$")

                elif 1 < players_hand[player][0] < 5:
                    if int(players_bet[player]) < max_bet:
                        players_bet[player] = max_bet
                        check = False
                        print(f"{player} equalized the bet to {max_bet}$")

                elif int(players_hand[player][0]) >= 3:
                    if players_bet[player] < max_bet:
                        players_bet[player] = max_bet * 2
                        max_bet = max_bet * 2
                        check = False
                        print(f"{player} raised the bet to {max_bet}$")
                    else:
                        continue
                else:
                    if players_bet[player] != 'check' or players_bet[player] != "fold":
                        players_bet[player] = max_bet - players_bet[player]
                        check = False
                        print(f"{player} equalized the bet to {max_bet}$")

            return players_bet, check, max_bet

        players_bet, check, max_bet = check_bet(players_bet=players_bet, players_list=players_after_blinds,
                                                max_bet=max_bet, check=True)
        if name in players_bet:
            if players_bet[name] < max_bet:
                if check:
                    user_bet = input(
                        f"Please make you bet equal {max_bet}$ or more or type 'check': "
                    )
                    players_bet[players_list[0]] = user_bet


                else:
                    user_bet = input(
                        f"Please make you bet equal {max_bet}$ "
                        f"or more or type 'fold' [Attention: You cannot check]: "
                    )
                    players_bet[name] = user_bet

                if user_bet == "check":
                    check = False
                elif user_bet == 'fold':
                    user_bet = max_bet
                    players_bet, check, max_bet = check_bet(check, players_bet, players_without_user, max_bet)

                else:
                    max_bet = int(user_bet)

                players_bet, check, max_bet = check_bet(check, players_bet, players_without_user, max_bet)
            return players_bet
        else:
            if players_bet[list(players_bet.keys())[0]] != max_bet:
                players_bet, check, max_bet = check_bet(check, players_bet, players_list, max_bet)
        return players_bet
