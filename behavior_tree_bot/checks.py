from planet_wars import *
def if_neutral_planet_available(state):
    return any(state.neutral_planets())

def have_largest_fleet(state):
    # return sum(planet.num_ships for planet in state.my_planets()) \
    #          + sum(fleet.num_ships for fleet in state.my_fleets()) \
    #        > sum(planet.num_ships for planet in state.enemy_planets()) \
    #          + sum(fleet.num_ships for fleet in state.enemy_fleets())

    my_planets = state.my_planets()
    enemy_planets = state.enemy_planets()
    for my_planet in my_planets:
        for enemy_planet in enemy_planets:
            if not my_planet or not enemy_planets:
                # No legal source or destination
                return False
            if state.distance(my_planet.ID, enemy_planet.ID) < 22:
            	return True
    return False
                

def if_neutral_proper(state):
    my_planets = state.my_planets()
    neutral_planets = state.neutral_planets()
    for my_planet in my_planets:
        for neutral_planet in neutral_planets:
            if state.distance(my_planet.ID,neutral_planet.ID) < 10:
                if neutral_planet.num_ships < my_planet.num_ships * 3/4:
                    return True
    return False

def if_enemy_attacking(state):
    my_planets = state.my_planets()
    # enemy_planets = state.enemy_planets()
    for my_planet in my_planets:
       if any (fleet.destination_planet == my_planet.ID for fleet in state.enemy_fleets()):
           return True
    return False








