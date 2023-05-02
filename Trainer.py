# Import necessary libraries
from Pokemon import Pokemon
import Constants
import json

# Trainer class 
class Trainer:
    def __init__(self, name: str, pokemon: tuple):
        self._name = name
        self._pokemon = {pokeName: Pokemon(*Constants.POKEMON[pokeName]) for pokeName in pokemon}
        self._currentPokemon = list(self._pokemon.keys())[0]

    # Return name
    def getName(self):
        return self._name
    
    # Return specific pokemon
    def getSpecificPokemon(self, n: int):
        return list(self._pokemon)[n]
    
    # Return pokemon moves
    def getPokemonMoves(self, pokemon_name: str):
        return list(self._pokemon[pokemon_name].getMoves())
    
    # Return pokemon in dictionary
    def getPokemon(self):
        return self._pokemon

    # Return string of all pokemons
    def getAllPokemon(self):
        # Can maybe fix this, I wont tho lol
        pokeDict = {pokeName: str(pokemon) for pokeName, pokemon in self._pokemon.items()}
        pokeDictString = json.dumps(pokeDict, indent=4).replace("\\n", "\n    ").replace("\\", "'").replace("',", "")
        return f'Pokemon:\n{pokeDictString}'

    # Implement damage from an attack
    def takeDamage(self, attackDamage: int):
        # Update the health
        currentPokemonHealth = self._pokemon[self._currentPokemon].takeDamage(attackDamage)

        # Update the current pokemon
        if currentPokemonHealth <= 0:
            self._pokemon.pop(self._currentPokemon)
            return 0
         
        return currentPokemonHealth

    # Return the damage of an attack
    def getAttackDamage(self, move: str):
        return self._pokemon[self._currentPokemon].getAttackDamage(move)

    # Set new current pokemon
    def setCurrentPokemon(self, pokemon: str):
        self._currentPokemon = pokemon

    # Return string of current pokemon
    def getCurrentPokemon(self):
        # Can Maybe fix this, I wont tho lol
        currentPokemonString = json.dumps(str(self._pokemon[self._currentPokemon]), indent=4)\
            .replace("\\n", "\n    ").replace("\\", "'").replace("',", "")
        return f'{self._currentPokemon}:\n{currentPokemonString}'

    # Return current pokemon name
    def getCurrentPokemonName(self):
        return self._currentPokemon

    # Return whether pokemon still alive
    def canContinue(self):
        return bool(self._pokemon)

    # Return string of class information
    def __str__(self):
        # Can maybe fix this, I wont tho lol
        pokeDict = {pokeName: str(pokemon) for pokeName, pokemon in self._pokemon.items()}
        pokeDictString = json.dumps(pokeDict, indent=4).replace("\\n", "\n    ").replace("\\", "'").replace("',", "")
        return f'{self._name}:\nPokemon:\n{pokeDictString}'
