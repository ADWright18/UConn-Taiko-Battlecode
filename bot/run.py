import battlecode as bc
import random
import sys
import traceback
import workerlogic

import os
print(os.getcwd())

print("pystarting")

# A GameController is the main type that you talk to the game with.
# Its constructor will connect to a running game.
gc = bc.GameController()

# List of attack units
attack_unit = [bc.UnitType.Knight, bc.UnitType.Ranger, bc.UnitType.Mage]

switch = 0

# Number of workers
num_worker = 0

for unit in gc.my_units():
    if unit.unit_type == bc.UnitType.Worker:
        num_worker += 1
        print('Worker Count:' + str(num_worker))

print("pystarted")

# It's a good idea to try to keep your bots deterministic, to make debugging easier.
# determinism isn't required, but it means that the same things will happen in every thing you run,
# aside from turns taking slightly different amounts of time due to noise.
random.seed(6137)

# let's start off with some research!
# we can queue as much as we want.
gc.queue_research(bc.UnitType.Rocket)
gc.queue_research(bc.UnitType.Worker)
gc.queue_research(bc.UnitType.Knight)

my_team = gc.team()

# Pathing functions, logic, and variables
directions = [bc.Direction.North, bc.Direction.Northeast, bc.Direction.East, bc.Direction.Southeast, bc.Direction.South, bc.Direction.Southwest, bc.Direction.West, bc.Direction.Northwest]
tryRotate = [0,-1,1,-2,2]

def invert(loc):
    newx = earthMap.width - loc.x
    newy = earthMap.height - loc.y
    return bc.MapLocation(bc.Planet.Earth,newx ,newy)

def locToString(loc):
    return ' (' + str(loc.x) + ',' + str(loc.y) + ') '

if gc.planet() == bc.Planet.Earth:
    start_loc = []
    i = 0
    for unit in gc.my_units:
        start_loc[i] = gc.my_units()[i].location.map_location()
        i += 1

    earthMap = gc.starting_map(bc.Planet.Earth)

    enemyStart = []

    for loc in start_loc:
        enemyStart.append(invert(loc))

    for loc in start_loc:
        print('Worker starts at ' + locToString(loc))

    for enemyLoc in enemyStart:
        print('Enemy worker presumably at ' + locToString(enemyLoc))

def rotate(dir, amount):
    ind = directions.index(dir)
    return directions[(ind + amount)%8]

def goto(unit, dest):
    d = unit.location.map_location().direction_to(dest)
    if gc.can_move(unit.id, d):
        gc.move_robot(unit.id, d)

def fuzzygoto(unit, dest):
    toward = unit.location.map_location().direction_to(dest)
    if toward == bc.Direction.Center:
        print('At enemy location')
    else:
        for tilt in tryRotate:
            d = rotate(toward, tilt)
            if gc.can_move(unit.id, d):
                gc.move_robot(unit.id, d)
                break

while True:
    # We only support Python 3, which means brackets around print()
    print('pyround:', gc.round())

    # frequent try/catches are a good idea
    try:
        # walk through our units:
        for unit in gc.my_units():

            # first, factory logic
            if unit.unit_type == bc.UnitType.Factory:

                garrison = unit.structure_garrison()
                produce_unit = random.choice(attack_unit)

                if len(garrison) > 0:
                    d = random.choice(directions)
                    if gc.can_unload(unit.id, d):
                        print('Unloaded a unit!')
                        gc.unload(unit.id, d)
                        continue
                elif gc.can_produce_robot(unit.id, produce_unit):

                    gc.produce_robot(unit.id, produce_unit)

                    if produce_unit == bc.UnitType.Knight:
                        print('Produced a knight!')

                    elif produce_unit == bc.UnitType.Ranger:
                        print('Produced a ranger!')

                    elif produce_unit == bc.UnitType.Mage:
                        print('Produced a mage!')

                    continue

            # first, let's look for nearby blueprints to work on

            location = unit.location
            if location.is_on_map():

                d = random.choice(directions)
                if unit.unit_type == bc.UnitType.Worker:

                    nearby = gc.sense_nearby_units(location.map_location(), 2)

                    for other in nearby:
                        if num_worker < 5 and gc.can_replicate(unit.id, d):
                            gc.replicate(unit.id, d)
                            print('replicated a worker!')
                            num_worker += 1
                            print('Worker Count: ' + str(num_worker))
                            continue

                        if gc.can_build(unit.id, other.id):
                            gc.build(unit.id, other.id)
                            print('built a factory!')
                            # move onto the next unit
                            continue

                elif unit.unit_type == bc.UnitType.Knight:
                    nearby = gc.sense_nearby_units(location.map_location(), 2)
                    for other in nearby:
                        if other.team != my_team and gc.is_attack_ready(unit.id) and gc.can_attack(unit.id, other.id):
                            print('Knight attacked a thing!')
                            gc.attack(unit.id, other.id)
                        elif gc.is_move_ready(unit.id):
                            fuzzygoto(unit, enemyStart[switch])
                            continue
                elif unit.unit_type == bc.UnitType.Mage:
                    nearby = gc.sense_nearby_units(location.map_location(), unit.attack_range())
                    for other in nearby:
                        if other.team != my_team and gc.is_attack_ready(unit.id) and gc.can_attack(unit.id, other.id):
                            print('Mage attacked a thing!')
                            gc.attack(unit.id, other.id)
                            continue
                        elif gc.is_move_ready(unit.id):
                            fuzzygoto(unit, enemyStart[switch])
                            continue

                elif unit.unit_type == bc.UnitType.Ranger:
                    nearby = gc.sense_nearby_units(location.map_location(), unit.attack_range())
                    for other in nearby:
                        if other.team != my_team and gc.is_attack_ready(unit.id) and gc.can_attack(unit.id, other.id):
                            print('Ranger attacked a thing!')
                            gc.attack(unit.id, other.id)
                            continue
                        elif gc.is_move_ready(unit.id):
                            fuzzygoto(unit, enemyStart[switch])
                            continue

            switch += 1
            switch = switch % enemyStart.length

            # okay, there weren't any dudes around
            # pick a random direction:
            d = random.choice(directions)

            # or, try to build a factory:
            if gc.karbonite() > bc.UnitType.Factory.blueprint_cost() and gc.can_blueprint(unit.id, bc.UnitType.Factory, d):
                gc.blueprint(unit.id, bc.UnitType.Factory, d)
            # and if that fails, try to move
            elif gc.is_move_ready(unit.id) and gc.can_move(unit.id, d):
                gc.move_robot(unit.id, d)

    except Exception as e:
        print('Error:', e)
        # use this to show where the error was
        traceback.print_exc()

    # send the actions we've performed, and wait for our next turn.
    gc.next_turn()

    # these lines are not strictly necessary, but it helps make the logs make more sense.
    # it forces everything we've written this turn to be written to the manager.
    sys.stdout.flush()
    sys.stderr.flush()
