from Trainer import Trainer
import random
import Constants

# Max 4
POKEMON_PER_TRAINER = 2

turn = 0
playerName = input('Input your name: ')
rivalName = input('Input my grandson\'s name: ')

rivalIsSpecialTrainer = False
if rivalName.capitalize() in Constants.TRAINERS_LIST:
    rivalName = rivalName.capitalize()
    print(f'You\'ve called special trainer {rivalName}')
    rivalIsSpecialTrainer = True

option = 'p'
while option == 'p':
    player = Trainer(playerName, tuple(random.sample(Constants.POKEMON_LIST, k=POKEMON_PER_TRAINER)))
    if rivalIsSpecialTrainer:
        rival = Trainer(rivalName, tuple(random.sample(Constants.TRAINERS[rivalName], k=POKEMON_PER_TRAINER)))
    else:
        rival = Trainer(rivalName, tuple(random.sample(Constants.POKEMON_LIST, k=POKEMON_PER_TRAINER)))

    print('-'* 100)
    print(str(player))
    print('-' * 100)
    print(str(rival))
    print('-' * 100)
    print('\n')

    while player.canContinue() and rival.canContinue():
        if turn == 0:
            print('Your Rival\'s Current Pokemon:')
            print(rival.getCurrentPokemon())
            print('\n')
            print('Your Current Pokemon:')
            print(player.getCurrentPokemon())

            playerMove = input('What move do you use?\n')

            damageDealt = player.getAttackDamage(playerMove)
            rivalRemainingMonHealth = rival.takeDamage(damageDealt)

            if rivalRemainingMonHealth == 0:
                if not rival.canContinue():
                    break

                print(f'Look at that! {rivalName}\'s {rival.getCurrentPokemonName()} is down!')
                # Here let AI choose next mon, for now manually chosen
                rival.setCurrentPokemon(input('Select new mon for the CPU, scroll to top if you really need to\n'))
                turn += 1
                continue

            if damageDealt > 0:
                print(f'WOW! {player.getCurrentPokemonName()} dealt {damageDealt} to {rivalName}\'s {rival.getCurrentPokemonName()}')
                print(f'{rivalName}\'s {rival.getCurrentPokemonName()} only has {rivalRemainingMonHealth} HP left!')
            else:
                print(f'HAHA he missed.')
                print(f'{rivalName}\'s {rival.getCurrentPokemonName()} still has {rivalRemainingMonHealth} HP left!')
            print('\n')

            turn += 1
            continue

        # Here AI will choose next move to make, for now manually entered
        cpuMove = input('Select a move for the CPU\n')

        damageDealt = rival.getAttackDamage(cpuMove)
        playerRemainingMonHealth = player.takeDamage(damageDealt)
        if playerRemainingMonHealth == 0:
            if not player.canContinue():
                break

            print(f'Oh no! Your {player.getCurrentPokemonName()} is down!')
            print(player.getAllPokemon())
            print('\n')
            player.setCurrentPokemon(input('What Pokemon are you going to send out next?!\n'))
            turn = 0
            continue

        if damageDealt > 0:
            print(
                f'WOW! {rival.getCurrentPokemonName()} dealt {damageDealt} to your {player.getCurrentPokemonName()}')
            print(f'Your {player.getCurrentPokemonName()} only has {playerRemainingMonHealth} HP left!')
        else:
            print(f'HAHA he missed.')
            print(f'Your {player.getCurrentPokemonName()} still has {playerRemainingMonHealth} HP left!')
        print('\n')

        turn = 0

    if player.canContinue():
        print('You did it! You beat your rival!')
    else:
        print('Smell ya later, loser')
    print('\n')

    option = input('Enter P to play again: ').lower()
