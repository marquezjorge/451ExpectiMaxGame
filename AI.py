from copy import deepcopy

# The max depth of the search tree for the expectimax algorithm
SEARCH_DEPTH = 4

def ai_move(state):
    """
    Initiates the expectimax algorithm.
    
    Args:
        state (dict): The current game state.
        
    Return:
        A string containing the best move for the ai to use.
    """
    # Run the expectimax algorithm to find the best move
    _, bestMove = expectimax(state, SEARCH_DEPTH, True)
    return bestMove

def expectimax(state, depth, isMaximizingPlayer):
    """
    Performs a recursive depth-limited search of the game tree. 
    The function uses a maximizing player to look for the move with the highest expected utility value. 
    The function uses a minimizing player to compute the average utility value of all possible moves, as each move has a probability associated with it.
    Base Case: When search-depth reaches 0, the function returns the utility value
    Recursive Case: If the search depth is greater than zero, the function iterates through all possible moves for the current player.
    
    Args:
        state (dict): The current game state.
        depth (int): The current search depth.
        isMaximizingPlayer (bool): Whether the current player is maximizing or minimizing.
        
    Returns:
        The best ulility value and the best move for the ai to make.
    """
    # Base Case: When search-depth reaches 0, the function returns the utility value
    if depth == 0 or is_terminal(state):
        return utility(state), None

    # Initialize best value depending on player type
    bestValue = float('-inf') if isMaximizingPlayer else 0
    # Initialize the best move variable
    bestMove = None
    # Get all the possible moves the ai can make
    possible_moves = get_possible_moves(state)
    
    # Counter to keep track of the moves for the minimzing player
    numMoves = 0

    # Iterate through all the possible moves
    for move in possible_moves:
        # Generate a new state for each move
        new_state = perform_move(state, move)
        # Compute the utility value for each move and state
        value, _ = expectimax(new_state, depth - 1, not isMaximizingPlayer)
        
        # If it is maxmizing player (AI)
        if isMaximizingPlayer:
            if value > bestValue:
                bestValue = value
                bestMove = move
        else:
            bestValue += value
            numMoves += 1
            bestMove = move
        
        # Calculate the average utility for the minimxing player (human)
        if not isMaximizingPlayer:
                bestValue /= numMoves
        
    # Return value and move
    return bestValue, bestMove

def is_terminal(state):
    """
    Check if the game is terminal if any player has no remaining Pokemon.
    
    Args:
        state (dict): The current game state.
        
    Returns:
        True if the game is terminal, False otherwise.
    """
    return state['player_remaining_pokemon'] == 0 or state['rival_remaining_pokemon'] == 0

def utility(state):
    """
    Checks how desirable a game state is for the maxmiziing player (AI) vs the minimizing player (human).
    Uses two factors: The remaining pokemon and the pokemon's health.
    Uses weights to consider what is more important.
    Currently, AI focuses more on its own status than on the player's status.
    
    Args:
        state (dict): The current game state.
        
    Returns:
        A value that quantifies how good a specific game state is. 
    """
    # Weights
    aiPokemonWeight = 100
    playerPokemonWeight = -80
    aiHealthWeight = 2
    playerHealthWeight = -1.5

    # Get scores for AI and for player
    playerRemainingHealth = state['player_remaining_health']
    rivalRemainingHealth = state['rival_remaining_health']
    
    if playerRemainingHealth is None:
        playerRemainingHealth = 0
    if rivalRemainingHealth is None:
        rivalRemainingHealth = 0;
    
    aiPokemonScore = state['rival_remaining_pokemon'] * aiPokemonWeight
    playerPokemonScore = state['player_remaining_pokemon'] * playerPokemonWeight
    aiHealthScore = rivalRemainingHealth * aiHealthWeight
    playerHealthScore = playerRemainingHealth * playerHealthWeight

    # Calculate the score
    totalScore = aiPokemonScore + playerPokemonScore + aiHealthScore + playerHealthScore

    return totalScore
    
def get_possible_moves(state):
    """
    Generates the possible moves the AI can make for a game state.
    
    Args:
        state (dict): The current game state.
        
    Returns:
        A list of moves.
    """
    rival = state['rival']
    return rival.getPokemonMoves(rival.getCurrentPokemonName())

def perform_move(state, move):
    """
    Performs an attack move and creates a new game state in order to simulate different scenarios.
    
    Args:
        state (dict): The current game state.
        move (str): The move to perform.
        
    Returns:
        A new game state.
    """
    # Create a copy of the player and rival(AI)
    player = deepcopy(state['player'])
    rival = deepcopy(state['rival'])
    turn = state['turn']
    
    # Deal damage to the player
    if player.getCurrentPokemonName() in player._pokemon:
        damageDealt = rival.getAttackDamage(move)
        playerRemainingMonHealth = player.takeDamage(damageDealt)
    else:
        playerRemainingMonHealth = 0
    
    # Check status of the player's pokemon
    if playerRemainingMonHealth == 0:
        # If no more pokemon, then terminal state
        if not player.canContinue():
            new_state = state.copy()
            new_state['is_terminal'] = True
            return new_state
        
        # Send out new pokemon when one dies
        rival.setCurrentPokemon(rival.getSpecificPokemon(0))
    
    # Update turn flag
    new_turn = 1 - turn
    
    # Update new game state
    new_state = state.copy()
    new_state['player_remaining_health'] = playerRemainingMonHealth
    new_state['turn'] = new_turn
    new_state['is_terminal'] = False
    
    return new_state
