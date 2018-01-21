import battlecode as bc
import random
import sys
import traceback
import os



directions = [bc.Direction.North, bc.Direction.Northeast, bc.Direction.East, bc.Direction.Southeast, bc.Direction.South, bc.Direction.Southwest, bc.Direction.West, bc.Direction.Northwest]
tryRotate = [0,-1,1,-2,2]


def __init__(self):
    self.yourStart = []
    self.enemyStart = []
    self.earthMap = None

def invert(earthMap, loc):
    newx = earthMap.width - loc.x
    newy = earthMap.height - loc.y
    return bc.MapLocation(bc.Planet.Earth,newx ,newy)

    # Create string representation of a location
def locToString(loc):
    return ' (' + str(loc.x) + ',' + str(loc.y) + ') '

    # Identify enemy start location and store in enemyStart
def findEnemy(gc, earthMap, yourStart, enemyStart):

    if gc.planet() == bc.Planet.Earth:
        earthMap = gc.starting_map(bc.Planet.Earth)

    for i in range (len(gc.my_units())):
        yourStart.append(gc.my_units()[i].location.map_location())

    for loc in yourStart:
        enemyStart.append(invert(earthMap, loc))
        print('Worker starts at ' + locToString(loc))

    for enemyLoc in enemyStart:
        print('Enemy worker presumably at ' + locToString(enemyLoc))

def rotate(dir, amount):
    ind = directions.index(dir)
    return directions[(ind + amount)%8]

def goto(gc, unit, dest):
    d = unit.location.map_location().direction_to(dest)
    if gc.can_move(unit.id, d):
            gc.move_robot(unit.id, d)

def fuzzygoto(gc, unit, dest):
    toward = unit.location.map_location().direction_to(dest)
    if toward == bc.Direction.Center:
        print('At enemy location')
    else:
        for tilt in tryRotate:
            d = rotate(toward, tilt)
            if gc.can_move(unit.id, d):
                gc.move_robot(unit.id, d)
                break
