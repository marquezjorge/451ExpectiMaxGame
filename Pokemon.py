# Import necessary libraries
import Constants
import random

# Pokemon class
class Pokemon:
    def __init__(self, health: int, moves: tuple, attack: int, speed: int):
        self._health = health
        self._moves = {moveName: Move(*Constants.MOVES[moveName]) for moveName in moves}
        self._attack = attack
        self._speed = speed

    # Return health
    def getHealth(self):
        return self._health

    # Return speed
    def getSpeed(self):
        return self._speed

    # Return moves
    def getMoves(self):
        return self._moves

    # Return attack damage
    def getAttackDamage(self, move: str):
        move = self._moves[move]
        move.use()
        if move.getPP() <= 0:
            move_name = None
            for key, value in self._moves.items():
                if value == move:
                    move_name = key
                    break
            if move_name is not None:
                self._moves.pop(move_name)
        didMiss = random.random() > move.getHitChance()
        self._updateMoveSet()
        if didMiss:
            return 0

        critMultiplier = 2 if random.random() < move.getCritChance() else 1
        return ((move.getDamage() * self._attack) / 100) * critMultiplier

    # Implement damage from an attack
    def takeDamage(self, damage: int):
        self._health -= damage
        return self._health

    # Update moves list
    def _updateMoveSet(self):
        self._moves = {moveName: move for moveName, move in self._moves.items() if move.getPP() > 0}

    # Return string of class information
    def __str__(self):
        # Part of string fix if you guys wanted to do it
        moveDict = {name: str(move) for name, move in self._moves.items()}
        return f'Health: {self._health}\nMoves: {moveDict}'

# Move class
class Move:
    def __init__(self, damage: int, critChance: int, hitChance: int, PP: int):
        self._damage = damage
        self._critChance = critChance / 100
        self._hitChance = hitChance / 100
        self._PP = PP

    # Return damage
    def getDamage(self):
        return self._damage

    # Return critical chance
    def getCritChance(self):
        return self._critChance

    # Return hit chance
    def getHitChance(self):
        return self._hitChance

    # Return pp
    def getPP(self):
        return self._PP

    # Update move usage
    def use(self):
        self._PP -= 1

    # Return string of class information
    def __str__(self):
        # Also part of it
        return f'Damage: {self._damage} | Accuracy: {int(self._hitChance * 100)} | PP: {self._PP}\n'