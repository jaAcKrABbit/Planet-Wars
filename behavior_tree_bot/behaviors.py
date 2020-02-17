import sys
import logging
sys.path.insert(0, '../')
from planet_wars import issue_order
from math import ceil, sqrt


def attack_weakest_enemy_planet(state):
    # (1) If we currently have a fleet in flight, abort plan.
    if len(state.my_fleets()) >= 1:
        return False

    # (2) Find my strongest planet.
    strongest_planet = max(
        state.my_planets(), key=lambda t: t.num_ships, default=None)

    # (3) Find the weakest enemy planet.
    weakest_planet = min(state.enemy_planets(),
                         key=lambda t: t.num_ships, default=None)

    if not strongest_planet or not weakest_planet:
        # No legal source or destination
        return False
    else:
        # (4) Send half the ships from my strongest planet to the weakest enemy planet.
        return issue_order(state, strongest_planet.ID, weakest_planet.ID, strongest_planet.num_ships / 2)

def attackClosestEnemy(state):
    my_planets = state.my_planets()
    enemy_planets = state.enemy_planets()
    for my_planet in my_planets:
        for enemy_planet in enemy_planets:
            logging.info(state.distance(my_planet.ID, enemy_planet.ID))
            logging.info("HEREEE %d %d",my_planet.num_ships, enemy_planet.num_ships)
            if (state.distance(my_planet.ID, enemy_planet.ID) < 15):
                if (my_planet.num_ships > enemy_planet.num_ships + (enemy_planet.growth_rate+1)*state.distance(my_planet.ID, enemy_planet.ID)):
                    logging.info("okay, second step")
                    if any (fleet.destination_planet == enemy_planet.ID for fleet in state.my_fleets()):
                        logging.info("already heading to %d!", enemy_planet.ID)
                        break
                    else:
                        issue_order(state, my_planet.ID, enemy_planet.ID, enemy_planet.num_ships + (1+enemy_planet.growth_rate)*state.distance(my_planet.ID, enemy_planet.ID))
                        break
            else:
                break





# def spread_to_weakest_neutral_planet(state):
#     # (1) If we currently have a fleet in flight, just do nothing.
#     if len(state.my_fleets()) >= 1:
#         return False

#     # (2) Find my strongest planet.
#     strongest_planet = max(
#         state.my_planets(), key=lambda p: p.num_ships, default=None)

#     # (3) Find the weakest neutral planet.
#     weakest_planet = min(state.neutral_planets(), key=lambda p: p.num_ships, default=None)

#     if not strongest_planet or not weakest_planet:
#         # No legal source or destination
#         return False
#     else:
#         # (4) Send half the ships from my strongest planet to the weakest enemy planet.
#         return issue_order(state, strongest_planet.ID, weakest_planet.ID, strongest_planet.num_ships / 2)






# def spread_to_proper_neutral_planets(state):
#     my_planets = state.my_planets()
#     neutral_planets = state.neutral_planets()
#     for my_planet in my_planets:
#         for neutral_planet in neutral_planets:
#             if not my_planet or not neutral_planet:
#                 # No legal source or destination
#                 return False
#             #

#             if state.distance(my_planet.ID, neutral_planet.ID) < 10:
#                 if neutral_planet.num_ships < my_planet.num_ships * 3/4:
#                     num_send = neutral_planet.num_ships + 1
#                     #no fleets flying (start state)
#                     if not state.my_fleets():
#                         issue_order(state, my_planet.ID,
#                                    neutral_planet.ID, num_send)
#                         logging.info("Nothing flying")
#                     else:
#                         # #fleets flying
#                             if any (fleet.destination_planet == neutral_planet.ID for fleet in state.my_fleets()):
#                                 logging.info("already heading to %d!",neutral_planet.ID)
#                                 break
#                             else:
#                                 if my_planet.num_ships > num_send: 
#                                     issue_order(
#                                         state, my_planet.ID, neutral_planet.ID, num_send)
#                                     logging.info("heading to : %d",
#                                                 neutral_planet.ID)
#                                 else:
#                                     break
#     return False    

def defend_enemy(state):
    my_planets = state.my_planets()
    for attacked_planet in my_planets:
        # if any(fleet.destination_planet == attacked_planet.ID for fleet in state.enemy_fleets()):
        for fleet in state.enemy_fleets():
            if(fleet.destination_planet == attacked_planet.ID):
                if attacked_planet.num_ships > fleet.num_ships:
                    return False
                else:
                    num_difference = fleet.num_ships - attacked_planet.num_ships
                    #pick a helper or may a few
                    for helper in my_planets:
                        if state.distance(helper.ID,attacked_planet.ID) < fleet.turns_remaining:
                            # if any(my_fleet.destination_planet == attacked_planet.ID for my_fleet in state.my_fleets()):
                            #     break
                            # else:
                                if helper.num_ships > num_difference + 1:
                                    logging.info("Helper num ships: %d", helper.num_ships)
                                    logging.info("How many helper send: %d", num_difference+1)
                                    logging.info("attacked planet score:  %d", attacked_planet.num_ships)
                                    logging.info("attacker num ships: %d", fleet.num_ships)
                                    return issue_order(state,helper.ID,attacked_planet.ID,num_difference+1)
    return False

def spread_everywhere(state):
    my_planets = iter(sorted(state.my_planets(), key=lambda p: p.num_ships))
    # all except mine
    target_planets = [planet for planet in state.not_my_planets() 
                        if not any(fleet.destination_planet == planet.ID for fleet in state.my_fleets())]
    target_planets = iter(sorted(target_planets, key=lambda p: p.num_ships))

    try:
        my_planet = next(my_planets)
        target_planet = next(target_planets)
        while True:
            #if enemy
            if target_planet.owner == 2:
                required_ships = target_planet.num_ships + \
                    state.distance(my_planet.ID, target_planet.ID) * \
                    target_planet.growth_rate + 1
            #neutral
            else:
                required_ships = target_planet.num_ships + 1
            # if enough ships to take that planet over
            if required_ships * 3/4 < my_planet.num_ships:
                issue_order(state, my_planet.ID,
                            target_planet.ID, required_ships)
                my_planet = next(my_planets)
                target_planet = next(target_planets)
            else:
                target_planet = next(target_planets)

    except StopIteration:
        return 


def defend_attacking(state):
    my_planets = [planet for planet in state.my_planets()]
    if not my_planets:
        return

    def strength(p):
        return p.num_ships \
            + sum(fleet.num_ships for fleet in state.my_fleets() if fleet.destination_planet == p.ID) \
            - sum(fleet.num_ships for fleet in state.enemy_fleets()
                  if fleet.destination_planet == p.ID)

    avg = sum(strength(planet) for planet in my_planets) / len(my_planets)

    weak_planets = [planet for planet in my_planets if strength(planet) < avg]
    strong_planets = [
        planet for planet in my_planets if strength(planet) > avg]

    if (not weak_planets) or (not strong_planets):
        return

    weak_planets = iter(sorted(weak_planets, key=strength))
    strong_planets = iter(sorted(strong_planets, key=strength, reverse=True))

    try:
        weak_planet = next(weak_planets)
        strong_planet = next(strong_planets)
        while True:
            need = int(avg - strength(weak_planet))
            have = int(strength(strong_planet) - avg)

            if have >= need > 0:
                issue_order(state, strong_planet.ID, weak_planet.ID, need)
                weak_planet = next(weak_planets)
            elif have > 0:
                issue_order(state, strong_planet.ID, weak_planet.ID, have)
                strong_planet = next(strong_planets)
            else:
                strong_planet = next(strong_planets)

    except StopIteration:
        return

def aggressive_attack(state):
    my_planets = iter(sorted(state.my_planets(), key=lambda p: p.num_ships))

    enemy_planets = [planet for planet in state.enemy_planets()
                     if not any(fleet.destination_planet == planet.ID for fleet in state.my_fleets())]
    enemy_planets.sort(key=lambda p: p.num_ships)

    target_planets = iter(enemy_planets)

    try:
        my_planet = next(my_planets)
        target_planet = next(target_planets)
        while True:
            required_ships = target_planet.num_ships + \
                state.distance(my_planet.ID, target_planet.ID) * \
                target_planet.growth_rate + 1

            if my_planet.num_ships > required_ships:
                issue_order(state, my_planet.ID,
                            target_planet.ID, required_ships)
                my_planet = next(my_planets)
                target_planet = next(target_planets)
            else:
                my_planet = next(my_planets)

    except StopIteration:
        return
