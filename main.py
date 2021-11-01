import time

from table import Table
from players import Players
from combinations import Combinations

table = Table()
players = Players()
comb = Combinations()

round_circle = 0

def game():
    global round_circle
    name = input("name: ")
    balance = int(input("balance: "))
    quantity_players = int(input("quantity_players: "))

    deck = table.build_deck()
    small_blind = balance / 10
    big_blind = balance / 5
    if round_circle > quantity_players - 1:
        round_circle = 0
    players_list = players.build_players(quantity_players, name)
    players_profiles = players.players_prifile(balance, players_list)
    # blind round
    print("Round 1")

    blinds = players.blinds(balance, round_circle, players_list)

    players_profiles = players.make_bet(blinds, players_profiles)
    players_profiles = players.players_with_cards(players_profiles, deck)
    players.get_info(bank=0, players_profile=players_profiles, cards_on_table=[], name=name)
    players_hand = comb.check_players_cards(players_profiles)
    players_bet = players.check_bet_blind_round(name, players_hand, blinds, big_blind, small_blind)
    players_profiles = players.make_bet(players_bet, players_profiles)
    bank = table.bank(bank=0, bet_dict=players_bet)
    #     flop - final
    print("Next Round")
    cards_on_table = [table.get_card(deck) for _ in range(3)]
    for round in range(3):
        if round > 0:
            print("Next Round")
        if 0 < round < 3:
            cards_on_table.append(table.get_card(deck))
        players.get_info(bank, players_profiles, cards_on_table, name)
        players_hand = players.check_combination(players_profiles, cards_on_table)
        players_bet = players.players_move(players_hand, small_blind, name, round_circle)
        players_profiles = players.make_bet(players_bet, players_profiles)
        bank = table.bank(bank, players_bet)
        players.get_info(bank, players_profiles, cards_on_table, name)
    # Showdown
    print("Showdown")
    players_hand = players.check_combination(players_profiles, cards_on_table)
    players_combinations = comb.check_players_combinations(players_hand)
    winners = comb.winner(players_hand)
    for player in players_profiles:
        time.sleep(1)
        print(f"Player: {player}, cards: {players_profiles[player][0]}, combination: {players_combinations[player]}")

    print(f"Winner is {winners[0]}, with cards {players_profiles[winners[0]][0]}, combination {winners[1]}")

game()

