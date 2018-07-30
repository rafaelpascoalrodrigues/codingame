import sys
import math


draft = []

# game loop
while True:
    player_hand = []
    player_battlefield = []
    opponent_battlefield = []


    for i in range(2):
        player_health, player_mana, player_deck, player_rune = [int(j) for j in input().split()]
    opponent_hand = int(input())
    card_count = int(input())
    for i in range(card_count):
        card_number, instance_id, location, card_type, cost, attack, defense, abilities, my_health_change, opponent_health_change, card_draw = input().split()
        card = {
            'card_number' : int(card_number),
            'instance_id' : int(instance_id),
            'location' : int(location),
            'card_type' : int(card_type),
            'cost' : int(cost),
            'attack' : int(attack),
            'defense' : int(defense),
            'player_health_change' : int(my_health_change),
            'opponent_health_change' : int(opponent_health_change),
            'card_draw' : int(card_draw),
            'abilities' : {
                'string' : abilities,
                'breakthrough' : True if abilities.find('B') != -1 else False,
                'charge' : True if abilities.find('C') != -1 else False,
                'guard' : True if abilities.find('G') != -1 else False,
                'drain' : True if abilities.find('D') != -1 else False,
                'lethal' : True if abilities.find('L') != -1 else False,
                'ward' : True if abilities.find('W') != -1 else False
            },
            'evaluation': 1
        }

        if card['location'] == 0:     # card in player hand
            player_hand += [card]
        elif card['location'] == 1:   # card in player's battlefield
            player_battlefield += [card]
        elif card['location'] == -1:  # card in player hand
            opponent_battlefield += [card]
        else:                         # something wrong happen
            pass


    # draft phase
    if len(draft) < 30:
        # Evaluate Cards
        evaluation_show = ""
        for card in player_hand:
            evaluation = 1
            if card['cost'] == 0:
                evaluation = 1
            elif card['card_type'] == 0:
                attack_per_cost = card['attack'] / card['cost']
                defense_per_cost = card['defense'] / card['cost']

                if card['abilities']['breakthrough']:
                    pass

                if card['abilities']['charge']:
                    pass

                if card['abilities']['guard']:
                    attack_per_cost *= 0.25

                if card['abilities']['drain']:
                    attack_per_cost *= 0.25
                    pass

                if card['abilities']['lethal']:
                    defense_per_cost *= 0.25
                    pass

                if card['abilities']['ward']:
                    attack_per_cost *= 0.15
                    defense_per_cost *= 0.15

                evaluation = attack_per_cost if attack_per_cost > defense_per_cost else defense_per_cost

            card['evaluation'] = evaluation
            evaluation_show +=  str(evaluation) + ", "

        pick = 0
        if player_hand[0]['evaluation'] > player_hand[1]['evaluation'] and player_hand[0]['evaluation'] > player_hand[2]['evaluation']:
            pick = 0
        elif player_hand[1]['evaluation'] > player_hand[2]['evaluation']:
            pick = 1
        else:
            pick = 2
        
        print("PICK", pick, evaluation_show)

        draft += [player_hand[0]]
        continue

    # battle phase

    # use itens
    for card in player_hand:
        if card['cost'] <= player_mana:

            # green item
            if card['card_type'] == 1:
                if len(player_battlefield) > 0 and player_battlefield[0]['card_type'] == 0:
                    player_mana -= card['cost']
                    print("USE", card['instance_id'], player_battlefield[0]['instance_id'] ,";", end="")

            # red item
            elif card['card_type'] == 2:
                if len(opponent_battlefield) > 0 and opponent_battlefield[0]['card_type'] == 0:
                    player_mana -= card['cost']
                    print("USE", card['instance_id'], opponent_battlefield[0]['instance_id'] ,";", end="")

            # blue item
            elif card['card_type'] == 3:
                player_mana -= card['cost']
                print("USE", card['instance_id'], "-1" ,";", end="")


    # summon creatures
    for card in player_hand:
        # battlefield card limit
        if len(player_battlefield) >= 6:
            print("can't summon more cards.", file=sys.stderr)
            break

        if card['cost'] <= player_mana:
            if card['card_type'] == 0:
                player_mana -= card['cost']
                print("SUMMON", card['instance_id'], ";", end="")


    # attack
    for card in player_battlefield:
        target = -1
        for enemy in opponent_battlefield:
            if enemy['abilities']['guard']:
                target = enemy['instance_id']
        print("ATTACK", card['instance_id'], target, ";", end="")



    # send a PASS in the end to prevent crash if no action was made
    print("PASS")
