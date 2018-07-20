import sys
import math


# initialize factory list
factory_count = int(input())
factory_list = dict()
for i in range(factory_count):
    factory_list[i] = {
        'player' : 0,
        'population' : 0,
        'production' : 0,
        'links' : [{
            'distance' : -1
        } for i in range(factory_count)],
    }


# setup distance between factories
link_count = int(input())
for i in range(link_count):
    factory_1, factory_2, distance = [int(j) for j in input().split()]
    factory_list[factory_1]['links'][factory_2]['distance'] = distance
    factory_list[factory_2]['links'][factory_1]['distance'] = distance


# game loop
while True:
    # retrieve data from entities
    entity_count = int(input())
    for i in range(entity_count):
        entity_id, entity_type, arg_1, arg_2, arg_3, arg_4, arg_5 = input().split()

        if entity_type == 'FACTORY':
            entity = factory_list[int(entity_id)]
            entity['player'] = int(arg_1)
            entity['population'] = int(arg_2)
            entity['production'] = int(arg_3)
            int(arg_4)
            int(arg_5)


    """
    strategy:
        send new produced cyborgs to the non onwned factory with few population.
    """
    for factory_owned_id in range(factory_count):
        # owned factories
        if factory_list[factory_owned_id]['player'] != 1:
            # not onwned
            continue

        factory_owned = factory_list[factory_owned_id]

        target_id = -1
        target_population = float('Inf')
        for factory_id in range(factory_count):
            factory = factory_list[factory_id]

            # non owned factories
            if factory['player'] != 1:
                if factory['population'] < target_population:
                    target_population = factory['population']
                    target_id = factory_id

                    if factory_owned['production'] == 0:
                        deploy = 1 if factory_owned['population'] > 1 else 0
                    else:
                        deploy = factory_owned['production']

                    print("MOVE", factory_owned_id, target_id, deploy, ";", end="")

    # send a wait in the end to prevent crash if no move was made
    print("WAIT")
