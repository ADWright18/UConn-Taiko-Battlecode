import battlecode as bc
import random
import sys
import traceback
import os
import pathing

class Manager():
    '''Manager class to distribute the GameController'''

    game_controller = bc.GameController()

    # Lists for pathing

    directions = [bc.Direction.North, bc.Direction.Northeast, bc.Direction.East, bc.Direction.Southeast, bc.Direction.South, bc.Direction.Southwest, bc.Direction.West, bc.Direction.Northwest]
    tryRotate = [0,-1,1,-2,2]

    num_worker = 0
    num_factory = 0
    num_mage = 0
    num_ranger = 0

    yourStart = []
    enemyStart = []
    earthMap = None


    def __init__(self):
        print("Hello")

    def countWorker(self):
        self.num_worker += 1
        print('Worker Count: ' + str(self.num_worker))

    def locateEnemy(self):
        pathing.findEnemy(self.game_controller,self.earthMap, self.yourStart, self.enemyStart)

    def fuzzygoto(self, unit, dest):
        pathing.fuzzygoto(self.game_controller, unit, dest)
