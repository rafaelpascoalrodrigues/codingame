import sys
import math


DRAFT_TURNS = 30


def main():
    draft(DRAFT_TURNS)
    game_loop()


def game_loop():
    while True:
        players = get_players()
        board = get_board()

        play(players, board)

        # send a PASS in the end to prevent crash if no action was made
        print("PASS")


def play(players, board):
    # use itens
    for card in board['player_hand']:
        if card['cost'] <= players['player']['mana']:

            # green item
            if card['card_type'] == 1:
                if len(board['player_battlefield']) > 0 and board['player_battlefield'][0]['card_type'] == 0:
                    players['player']['mana'] -= card['cost']
                    print("USE", card['instance_id'], board['player_battlefield'][0]['instance_id'] ,";", end="")

            # red item
            elif card['card_type'] == 2:
                if len(board['opponent_battlefield']) > 0 and board['opponent_battlefield'][0]['card_type'] == 0:
                    players['player']['mana'] -= card['cost']
                    print("USE", card['instance_id'], board['opponent_battlefield'][0]['instance_id'] ,";", end="")

            # blue item
            elif card['card_type'] == 3:
                players['player']['mana'] -= card['cost']
                print("USE", card['instance_id'], "-1" ,";", end="")


    # summon creatures
    for card in  board['player_hand']:
        # battlefield card limit
        if len(board['player_battlefield']) >= 6:
            print("can't summon more cards.", file=sys.stderr)
            break

        if card['cost'] <= players['player']['mana']:
            if card['card_type'] == 0:
                players['player']['mana'] -= card['cost']
                print("SUMMON", card['instance_id'], ";", end="")


    # attack
    for card in  board['player_battlefield']:
        target = -1
        for enemy in board['opponent_battlefield']:
            if enemy['abilities']['guard'] and enemy['defense'] > 0:
                target = enemy['instance_id']
                if not enemy['abilities']['ward']:
                    enemy['defense'] -= card['attack']
        print("ATTACK", card['instance_id'], target, ";", end="")


def draft(cards_to_pick):
    for _ in range(cards_to_pick):
        get_players()
        board = get_board()

        pick = 0
        eval0 = board['player_hand'][0]['evaluation']
        eval1 = board['player_hand'][1]['evaluation']
        eval2 = board['player_hand'][2]['evaluation']
        if eval0 > eval1 and eval0 > eval2:
            pick = 0
        elif eval1 > eval2:
            pick = 1
        else:
            pick = 2
        
        print("PICK", pick, [x['evaluation'] for x in board['player_hand']])


def get_players():
    players = {
        'player'   : get_player(),
        'opponent' : get_player(),
    }

    input_splitted = input().split()
    players['opponent']['hand']    = int(input_splitted[0])
    players['opponent']['actions'] = int(input_splitted[1])

    for _ in range(players['opponent']['actions']):
        input()

    return players


def get_player():
    input_splitted = input().split()

    return {
        'health'  : int(input_splitted[0]),
        'mana'    : int(input_splitted[1]),
        'deck'    : int(input_splitted[2]),
        'rune'    : int(input_splitted[3]),
        'draw'    : int(input_splitted[4]),

        'hand'    : -1,
        'actions' : -1,
    }


def get_board():
    board = {
        'card_count'           : int(input()),
        'player_hand'          : [],
        'player_battlefield'   : [],
#       'opponent_hand'        : [],  # no information about opponent's hand
        'opponent_battlefield' : [],
    }

    for _ in range(board['card_count']):
        card = get_card()

        if card['location'] == 0:     # card in player hand
            board['player_hand'] += [card]
        elif card['location'] == 1:   # card in player's side of battlefield
            board['player_battlefield'] += [card]
        elif card['location'] == -1:  # card in opponent's side of battlefield
            board['opponent_battlefield'] += [card]
        else:                         # something wrong happen
            pass

    return board


def get_card():
    input_splitted = input().split()

    card = {
        'evaluation'             : 1,
        'card_number'            : int(input_splitted[0]),
        'instance_id'            : int(input_splitted[1]),
        'location'               : int(input_splitted[2]),
        'card_type'              : int(input_splitted[3]),
        'cost'                   : int(input_splitted[4]),
        'attack'                 : int(input_splitted[5]),
        'defense'                : int(input_splitted[6]),
        'player_health_change'   : int(input_splitted[8]),
        'opponent_health_change' : int(input_splitted[9]),
        'card_draw'              : int(input_splitted[10]),
        'abilities'              : {
            'string'       : input_splitted[7],
            'breakthrough' : True if input_splitted[7].find('B') != -1 else False,
            'charge'       : True if input_splitted[7].find('C') != -1 else False,
            'guard'        : True if input_splitted[7].find('G') != -1 else False,
            'drain'        : True if input_splitted[7].find('D') != -1 else False,
            'lethal'       : True if input_splitted[7].find('L') != -1 else False,
            'ward'         : True if input_splitted[7].find('W') != -1 else False
        },
    }

    card['evaluation'] = evaluate_card(card)

    return card


def evaluate_card(card):
    evaluation = 1

    if card['cost'] == 0:
        evaluation = 1

    elif card['card_type'] == 0:
        attack_per_cost  = card['attack']  / card['cost']
        defense_per_cost = card['defense'] / card['cost']

        if card['abilities']['breakthrough']:
            pass

        if card['abilities']['charge']:
            pass

        if card['abilities']['guard']:
            attack_per_cost *= 1.25

        if card['abilities']['drain']:
            attack_per_cost *= 1.25
            pass

        if card['abilities']['lethal']:
            defense_per_cost *= 1.25
            pass

        if card['abilities']['ward']:
            attack_per_cost *= 1.15
            defense_per_cost *= 1.15

    evaluation = attack_per_cost if attack_per_cost > defense_per_cost else defense_per_cost

    return evaluation


# Start the execution if it's the main script
if __name__ == "__main__":
    main()
