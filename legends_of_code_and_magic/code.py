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
            'card_draw' : int(card_draw)
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
        print("PICK", 0)

        draft += [card]
        continue

    # battle phase
    for card in player_hand:
        # battlefield card limit
        if len(player_battlefield) >= 6:
            print("can't summon more cards.", file=sys.stderr)
            break

        if card['cost'] <= player_mana:
            if card['card_type'] == 0:
                player_mana -= card['cost']
                print("SUMMON", card['instance_id'], ";", end="")


    # send a PASS in the end to prevent crash if no action was made
    print("PASS")
