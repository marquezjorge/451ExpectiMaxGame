import Constants
import random

class Pokemon:
    def __init__(self, health: int, moves: tuple, attack: int, speed: int):
        self._health = health
        self._moves = {moveName: Move(*Constants.MOVES[moveName]) for moveName in moves}
        self._attack = attack
        self._speed = speed

    def getHealth(self):
        return self._health

    def getSpeed(self):
        return self._speed

    def getMoves(self):
        return self._moves

    def getAttackDamage(self, move: str):
        move = self._moves[move]
        move.use()
        if move.getPP() <= 0:
            self._moves.pop(move)
        didMiss = random.random() > move.getHitChance()
        if didMiss:
            return 0

        critMultiplier = 2 if random.random() < move.getCritChance() else 1
        return ((move.getDamage() * self._attack) / 100) * critMultiplier

    def takeDamage(self, damage: int):
        self._health -= damage
        return self._health

    def __str__(self):
        # Part of string fix if you guys wanted to do it
        moveDict = {name: str(move) for name, move in self._moves.items()}
        return f'Health: {self._health}\nMoves: {moveDict}'

class Move:
    def __init__(self, damage: int, critChance: int, hitChance: int, PP: int):
        self._damage = damage
        self._critChance = critChance / 100
        self._hitChance = hitChance / 100
        self._PP = PP

    def getDamage(self):
        return self._damage

    def getCritChance(self):
        return self._critChance

    def getHitChance(self):
        return self._hitChance

    def getPP(self):
        return self._PP

    def use(self):
        self._PP -= 1

    def __str__(self):
        # Also part of it
        return f'Damage: {self._damage} | Accuracy: {int(self._hitChance * 100)} | PP: {self._PP}\n'


# Test code:
# pikachu = Pokemon(*Constants.POKEMON[Constants.PIKACHU])
# print(f'Pikachu \n{pikachu}\n')
