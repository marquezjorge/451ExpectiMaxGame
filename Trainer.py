from Pokemon import Pokemon
import Constants
import json

class Trainer:
    def __init__(self, name: str, pokemon: tuple):
        self._name = name
        self._pokemon = {pokeName: Pokemon(*Constants.POKEMON[pokeName]) for pokeName in pokemon}
        self._currentPokemon = list(self._pokemon.keys())[0]

    def getName(self):
        return self._name

    def getAllPokemon(self):
        # Can maybe fix this, I wont tho lol
        pokeDict = {pokeName: str(pokemon) for pokeName, pokemon in self._pokemon.items()}
        pokeDictString = json.dumps(pokeDict, indent=4).replace("\\n", "\n    ").replace("\\", "'").replace("',", "")
        return f'Pokemon:\n{pokeDictString}'

    def takeDamage(self, attackDamage: int):
        currentPokemonHealth = self._pokemon[self._currentPokemon].takeDamage(attackDamage)

        if currentPokemonHealth <= 0:
            self._pokemon.pop(self._currentPokemon)
            return 0

        return currentPokemonHealth

    def getAttackDamage(self, move: str):
        return self._pokemon[self._currentPokemon].getAttackDamage(move)

    def setCurrentPokemon(self, pokemon: str):
        self._currentPokemon = pokemon

    def getCurrentPokemon(self):
        # Can Maybe fix this, I wont tho lol
        currentPokemonString = json.dumps(str(self._pokemon[self._currentPokemon]), indent=4)\
            .replace("\\n", "\n    ").replace("\\", "'").replace("',", "")
        return f'{self._currentPokemon}:\n{currentPokemonString}'

    def getCurrentPokemonName(self):
        return self._currentPokemon

    def canContinue(self):
        return bool(self._pokemon)

    def __str__(self):
        # Can maybe fix this, I wont tho lol
        pokeDict = {pokeName: str(pokemon) for pokeName, pokemon in self._pokemon.items()}
        pokeDictString = json.dumps(pokeDict, indent=4).replace("\\n", "\n    ").replace("\\", "'").replace("',", "")
        return f'{self._name}:\nPokemon:\n{pokeDictString}'

# Test Code:
#
# ash = Trainer('ash', (Constants.PIKACHU, Constants.MACHOP))
#
# print(ash.getAllPokemon())
# print(ash.takeDamage(170))
# ash.setCurrentPokemon('Machop')
# ash.getAttackDamage('Ice Punch')
# print(ash.getCurrentPokemon())
