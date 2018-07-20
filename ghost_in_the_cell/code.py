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
            'factory_id' : i,
            'distance' : -1
        } for i in range(factory_count)],
        'distance_order' : [],
        'capture' : {
            'holding' : 0,
            'attacking' : 0,
            'defending' : 0
        }
    }


# setup distance between factories
link_count = int(input())
for i in range(link_count):
    factory_1, factory_2, distance = [int(j) for j in input().split()]
    factory_list[factory_1]['links'][factory_2]['distance'] = distance
    factory_list[factory_2]['links'][factory_1]['distance'] = distance

# sort factory links by distance
for i in range(factory_count):
    distances = []
    for j in range(len(factory_list[i]['links'])):
        link = factory_list[i]['links'][j]
        for k in range(len(distances)):
            if link['distance'] < distances[k]['distance']:
                distances.insert(k, {'factory_id' : link['factory_id'], 'distance' : link['distance']})
                link = None
                break

        if link != None:
            distances.append({'factory_id' : link['factory_id'], 'distance' : link['distance']})

    factory_list[i]['distance_order'] = [ x['factory_id'] for x in distances ]


# game loop
while True:
    # clear data from troops on factories
    for factory_id in range(factory_count):
        factory = factory_list[factory_id]
        factory['capture']['holding'] = 0
        factory['capture']['attacking'] = 0
        factory['capture']['defending'] = 0

    # retrieve data from entities
    entity_count = int(input())
    for i in range(entity_count):
        entity_id, entity_type, arg_1, arg_2, arg_3, arg_4, arg_5 = input().split()

        if entity_type == 'FACTORY':
            factory = factory_list[int(entity_id)]
            factory['player'] = int(arg_1)
            factory['population'] = int(arg_2)
            factory['production'] = int(arg_3)
            int(arg_4)
            int(arg_5)


        elif entity_type == 'TROOP':
            player = int(arg_1)
            factory_from = int(arg_2)
            factory_destination = int(arg_3)
            troops_count = int(arg_4)
            int(arg_5)

            factory = factory_list[factory_destination]
            if player == -1:
                if factory['player'] == 1:
                    factory['capture']['attacking'] += troops_count
                else:
                    factory['capture']['defending'] += troops_count
            else:
                if factory['player'] == 1:
                    factory['capture']['defending'] += troops_count
                else:
                    factory['capture']['attacking'] += troops_count


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

        for production_rate in [3, 2, 1]:
            for factory_id in factory_owned['distance_order']:
                factory = factory_list[factory_id]

                # non owned factories
                if factory['player'] != 1 and factory['production'] == production_rate and factory_owned['links'][factory_id]['distance'] != -1:
                    to_capture = factory['population'] + factory['capture']['defending'] - factory['capture']['attacking'] + 1
                    if factory['player'] != 0:
                        to_capture += (factory_owned['links'][factory_id]['distance'] * factory['production'])
                    
                    to_capture = to_capture if to_capture > 0 else 0
                    if to_capture >= factory_owned['population']:
                        continue

                    print("MOVE", factory_owned_id, factory_id, to_capture, "; ", end="")

    # send a wait in the end to prevent crash if no move was made
    print("WAIT")
