# Import necessay libraries
from Trainer import Trainer
from AI import ai_move
import random
import Constants

def updateGameState(gameState, player, rival, playerAllMon, rivalAllMon, playerCurrentMon, rivalCurrentMon, playerRemainingMon, rivalRemainingMon, playerRemainingHealth, rivalRemainingHealth, moveHistory, turn):
    """
    Update the game state after any changes.
    
    Args:
        gameState (dict): The facts about the game.
        player (Trainer): The current player.
        rival (Trainer): The current rival.
        playerAllMon (str): The player's pokemon.
        rivalAllMon (str): The rival's pokemon.
        playerCurrentMon (str): The player's current pokemon.
        rivalCurrentMon (str): The rival's current pokemon.
        playerRemainingMon (int): The player's remaining pokemon.
        rivalRemainingMon (int): The rivals's remaining pokemon.
        playerRemainingHealth (int): The player's remaining health.
        rivalRemainingHealth (int): The rival's remaining health.
        moveHistory (list): The history of moves
        turn (int): The turn flag.
        
    Returns:
        A dictionary containing the updated game state
    """    
    state = gameState
    state['player'] = player
    state['rival'] = rival
    state['player_all_pokemon'] = playerAllMon
    state['rival_all_pokemon'] = rivalAllMon
    state['player_current_pokemon'] = playerCurrentMon
    state['rival_current_pokemon'] = rivalCurrentMon
    state['player_remaining_pokemon'] = playerRemainingMon
    state['rival_remaining_pokemon'] = rivalRemainingMon
    state['player_remaining_health'] = playerRemainingHealth
    state['rival_remaining_health'] = rivalRemainingHealth
    state['move_history'] = moveHistory
    state['turn'] = turn
    
    return state

def printState(state):
    """
    Helper function to print the game state if needed.
    
    Args:
        state (dict): The game state.
        
    Returns:
        None
    """
    print('-'*100, '\n')
    print("GAME STATE\n")
    for key, value in state.items():
        print(key, " : " , value)
    print('-'*100, '\n')

# Max 4
POKEMON_PER_TRAINER = 2

# List to store move history
moveHistory = []

# Set turn to player and prompt for player and rival name
turn = 0
playerName = input('Input your name: ')
rivalName = input('Input my grandson\'s name: ')

# Check if rival is a special trainer
rivalIsSpecialTrainer = False
if rivalName.capitalize() in Constants.TRAINERS_LIST:
    rivalName = rivalName.capitalize()
    print(f'You\'ve called special trainer {rivalName}')
    rivalIsSpecialTrainer = True

# Start the game
option = 'p'
while option == 'p':
    # Load random pokemon for the player and the rival
    player = Trainer(playerName, tuple(random.sample(Constants.POKEMON_LIST, k=POKEMON_PER_TRAINER)))
    if rivalIsSpecialTrainer:
        rival = Trainer(rivalName, tuple(random.sample(Constants.TRAINERS[rivalName], k=POKEMON_PER_TRAINER)))
    else:
        rival = Trainer(rivalName, tuple(random.sample(Constants.POKEMON_LIST, k=POKEMON_PER_TRAINER)))

    # Print the player's and the rival's pokemon
    print('-'* 100)
    print(str(player))
    print('-' * 100)
    print(str(rival))
    print('-' * 100)
    print('\n')
    
    # Initialize the game state
    gameState = {
        'player': player,
        'rival': rival,
        'player_all_pokemon': player.getAllPokemon(),
        'rival_all_pokemon': rival.getAllPokemon(),
        'player_current_pokemon': player.getCurrentPokemon(),
        'rival_current_pokemon': rival.getCurrentPokemon(),
        'player_remaining_pokemon': len(player._pokemon),
        'rival_remaining_pokemon': len(rival._pokemon),
        'player_remaining_health': 0,
        'rival_remaining_health': 0,
        'move_history': moveHistory,
        'turn': turn
    }
    
    # Start the battle
    while player.canContinue() and rival.canContinue():
        # Variables for health
        playerRemainingMonHealth = None
        rivalRemainingMonHealth = None
        # Flag for invalid input
        errorFlag = False
        
        # If it is players turn
        if turn == 0:
            # Print pokemon statuses
            print('Your Rival\'s Current Pokemon:')
            print(rival.getCurrentPokemon())
            print('\n')
            print('Your Current Pokemon:')
            print(player.getCurrentPokemon())
            print()
            
            try:
                # Prompt player to select an attack move
                playerMove = input('What move do you use?\n')
                # Calculate damage from attack
                damageDealt = player.getAttackDamage(playerMove)
                # Implement damage to the rival
                rivalRemainingMonHealth = rival.takeDamage(damageDealt)

                # If rival is killed, select new pokemon
                if rivalRemainingMonHealth == 0:
                    if not rival.canContinue():
                        print('Your rival has been defeated!')
                        break
                    
                    # Output message
                    print(f'Look at that! {rivalName}\'s {rival.getCurrentPokemonName()} is down!')
                    
                    # AI is given the next available pokemon
                    rival.setCurrentPokemon(rival.getSpecificPokemon(0))
                    
                    # Output message
                    print(f'{rivalName} is sending out {rival.getCurrentPokemonName()}!')
                    print("-"*100)
                    print()
                    
                    # Update turn flag
                    turn += 1
                    
                    # Update the game state after each move
                    moveHistory.append(('player', playerMove))
                    updateGameState(gameState, player, rival, player.getAllPokemon(), rival.getAllPokemon(), player.getCurrentPokemon(), rival.getCurrentPokemon(), len(player._pokemon), len(rival._pokemon), playerRemainingMonHealth, rivalRemainingMonHealth, moveHistory, turn)
                    
                    continue
            except KeyError as e:
                print('Invalid move')
                errorFlag = True
                break
            
            # If rival is still alive, print damage dealt
            if damageDealt > 0:
                print(f'WOW! {player.getCurrentPokemonName()} dealt {damageDealt} to {rivalName}\'s {rival.getCurrentPokemonName()}')
                print(f'{rivalName}\'s {rival.getCurrentPokemonName()} only has {rivalRemainingMonHealth} HP left!')
                print("-"*100)
            else:
                print(f'HAHA he missed.')
                print(f'{rivalName}\'s {rival.getCurrentPokemonName()} still has {rivalRemainingMonHealth} HP left!')
                print("-"*100)
            print('\n')

            # Update the turn flag
            turn += 1
            
            # Update the game state after each move
            moveHistory.append(('player', playerMove))
            updateGameState(gameState, player, rival, player.getAllPokemon(), rival.getAllPokemon(), player.getCurrentPokemon(), rival.getCurrentPokemon(), len(player._pokemon), len(rival._pokemon), playerRemainingMonHealth, rivalRemainingMonHealth, moveHistory, turn)
            
            continue
        
        # AI chooses next move they will make
        aiMove = ai_move(gameState)
        cpuMove = aiMove
        print(f'{rivalName}\'s {rival.getCurrentPokemonName()} used {aiMove}')

        # Calculate damage from attack
        damageDealt = rival.getAttackDamage(cpuMove)
        # Implement attack to player
        playerRemainingMonHealth = player.takeDamage(damageDealt)
        
        # If player is killed, select new pokemon
        if playerRemainingMonHealth == 0:
            if not player.canContinue():
                print(f'{rivalName}\'s has defeated you!')
                break
            
            # Prompt message
            print(f'Oh no! Your {player.getCurrentPokemonName()} is down!')
            print(player.getAllPokemon())
            print('\n')
            player.setCurrentPokemon(input('What Pokemon are you going to send out next?!\n'))
            print("-"*100)
            print()
            
            # Update turn flag
            turn = 0
            
            # Update game state
            moveHistory.append(('rival', cpuMove))
            updateGameState(gameState, player, rival, player.getAllPokemon(), rival.getAllPokemon(), player.getCurrentPokemon(), rival.getCurrentPokemon(), len(player._pokemon), len(rival._pokemon), playerRemainingMonHealth, rivalRemainingMonHealth, moveHistory, turn)
            
            continue
        
        # If player is still alive, print damage dealt
        if damageDealt > 0:
            print(f'WOW! {rival.getCurrentPokemonName()} dealt {damageDealt} to your {player.getCurrentPokemonName()}')
            print(f'Your {player.getCurrentPokemonName()} only has {playerRemainingMonHealth} HP left!')
            print("-"*100)
        else:
            print(f'HAHA he missed.')
            print(f'Your {player.getCurrentPokemonName()} still has {playerRemainingMonHealth} HP left!')
            print("-"*100)
        print('\n')

        # Update turn flag
        turn = 0
        
        # Update game state
        moveHistory.append(('rival', cpuMove))
        updateGameState(gameState, player, rival, player.getAllPokemon(), rival.getAllPokemon(), player.getCurrentPokemon(), rival.getCurrentPokemon(), len(player._pokemon), len(rival._pokemon), playerRemainingMonHealth, rivalRemainingMonHealth, moveHistory, turn)
        
    # Check for a winner
    if errorFlag:
        print('Try again.')
    elif player.canContinue():
        print('You did it! You beat your rival!')
    else:
        print('Smell ya later, loser')
    print('\n')

    # Prompt to start a new game
    option = input('Enter P to play again: ').lower()
    