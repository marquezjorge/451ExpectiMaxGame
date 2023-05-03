from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtCore import Qt
from Pokemon import *
from Trainer import Trainer
from AI import ai_move
import Constants
import random


def updateGameState(gameState, player, rival, playerAllMon, rivalAllMon, playerCurrentMon, rivalCurrentMon,
                    playerRemainingMon, rivalRemainingMon, playerRemainingHealth, rivalRemainingHealth, moveHistory,
                    turn):
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


class MainWindow(QMainWindow):
    # Max 4
    POKEMON_PER_TRAINER = 4

    def __init__(self):
        super().__init__()
        self.setAutoFillBackground(True)

        palette = self.palette()
        palette.setColor(QPalette.Window, QColor(141, 178, 247))
        self.setPalette(palette)

        self.setWindowTitle("ExpectiMax Battle")
        self.setWindowIcon(QIcon(Constants.BACKGROUND))
        self.setFixedSize(QSize(700, 450))
        self.setStyleSheet("font-family: 'Open Sans', sans-serif;")

        self.battleOptions = BattleOptions()
        self.battleScreen = BattleScreen()

        layout = QVBoxLayout()
        layout.addWidget(self.battleScreen)
        layout.addWidget(self.battleOptions)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        centralWidget = QWidget()
        centralWidget.setLayout(layout)
        self.setCentralWidget(centralWidget)
        centralWidget.setStyleSheet('height: 100%;'
                                    'width: 100%'
                                    )
        self.show()
        self.turn = 0
        self.loop = None
        self.selectedOption = None
        self.currentMon = None
        self.gameState = {}
        self.moveHistory = []
        self.rivalName = None
        self.rival = None
        self.player = None
        self.showStartScreen()

    def showStartScreen(self):
        self.loop = QEventLoop()
        self.battleOptions.showStartButton(self)
        self.loop.exec()

        self.initializeAndStartGameLoop()

    def showBattleAgainScreen(self):
        self.loop = QEventLoop()
        self.battleOptions.showBattleButton(self)
        self.loop.exec()

        self.initializeAndStartGameLoop()

    def initializeAndStartGameLoop(self):
        self.player = Trainer('You', tuple(random.sample(Constants.POKEMON_LIST, k=self.POKEMON_PER_TRAINER)))

        if self.rivalName.capitalize() in Constants.TRAINERS_LIST:
            # Maybe showText here to show special trainer
            self.rival = Trainer(self.rivalName, tuple(random.sample(Constants.TRAINERS[self.rivalName.capitalize()],
                                                                     k=self.POKEMON_PER_TRAINER)))
        else:
            self.rival = Trainer(self.rivalName, tuple(random.sample(Constants.POKEMON_LIST,
                                                                     k=self.POKEMON_PER_TRAINER)))

        self.gameState = {
            'player': self.player,
            'rival': self.rival,
            'player_all_pokemon': self.player.getAllPokemon(),
            'rival_all_pokemon': self.rival.getAllPokemon(),
            'player_current_pokemon': self.player.getCurrentPokemon(),
            'rival_current_pokemon': self.rival.getCurrentPokemon(),
            'player_remaining_pokemon': len(self.player.getPokemon()),
            'rival_remaining_pokemon': len(self.rival.getPokemon()),
            'player_remaining_health': 0,
            'rival_remaining_health': 0,
            'move_history': self.moveHistory,
            'turn': self.turn
        }

        self.GameLoop()

    def GameLoop(self):
        self.updatePlayerStatus(f'You sent out {self.player.getCurrentPokemonName()}',
                                self.player.getCurrentPokemonName(),
                                self.player.getPokemon()[self.player.getCurrentPokemonName()]
                                )
        loop = QEventLoop()
        QTimer.singleShot(3000, loop.quit)
        loop.exec()

        self.updateEnemyStatus(f'{self.rival.getName()} sent out {self.rival.getCurrentPokemonName()}',
                               self.rival.getCurrentPokemonName(),
                               self.rival.getPokemon()[self.rival.getCurrentPokemonName()]
                               )
        loop = QEventLoop()
        QTimer.singleShot(3000, loop.quit)
        loop.exec()

        playerRemainingMonHealth = self.player.getPokemon()[self.player.getCurrentPokemonName()].getHealth()
        rivalRemainingMonHealth = self.rival.getPokemon()[self.rival.getCurrentPokemonName()].getHealth()

        while self.player.canContinue() and self.rival.canContinue():
            if self.turn == 0:

                self.loop = QEventLoop()
                self.updatePlayerMoves(self.player.getPokemon()[self.player.getCurrentPokemonName()])
                self.loop.exec()

                selectedMove = self.selectedOption.split('\n')[0]
                self.updateMoveHistoryAndGameState('player', selectedMove, playerRemainingMonHealth,
                                                   rivalRemainingMonHealth)

                self.currentMon = self.rival.getPokemon()[self.rival.getCurrentPokemonName()]
                damageDealt = self.player.getAttackDamage(selectedMove)
                rivalRemainingMonHealth = self.rival.takeDamage(damageDealt)

                if rivalRemainingMonHealth == 0:
                    if not self.rival.canContinue():
                        break

                    self.updateEnemyStatus(f'{self.player.getCurrentPokemonName()} used {selectedMove}\n'
                                           f'Look at that! {self.rival.getName()}\'s {self.rival.getCurrentPokemonName()} is down!',
                                           self.rival.getCurrentPokemonName(),
                                           self.currentMon
                                           )
                    loop = QEventLoop()
                    QTimer.singleShot(3000, loop.quit)
                    loop.exec()

                    self.rival.setCurrentPokemon(self.rival.getSpecificPokemon(0))
                    self.updateEnemyStatus(f'{self.rival.getName()} sent out {self.rival.getCurrentPokemonName()}',
                                           self.rival.getCurrentPokemonName(),
                                           self.rival.getPokemon()[self.rival.getCurrentPokemonName()]
                                           )
                    loop = QEventLoop()
                    QTimer.singleShot(3000, loop.quit)
                    loop.exec()

                    self.turn += 1
                    continue

                if damageDealt > 0:
                    self.updateEnemyStatus(f'{self.player.getCurrentPokemonName()} used {selectedMove}\n'
                                           f'WOW! {self.player.getCurrentPokemonName()} dealt {damageDealt} to {self.rival.getName()}\'s {self.rival.getCurrentPokemonName()}\n'
                                           f'{self.rival.getName()}\'s {self.rival.getCurrentPokemonName()} only has {rivalRemainingMonHealth} HP left!',
                                           self.rival.getCurrentPokemonName(),
                                           self.currentMon
                                           )
                    loop = QEventLoop()
                    QTimer.singleShot(3000, loop.quit)
                    loop.exec()

                else:
                    self.updateEnemyStatus(f'{self.player.getCurrentPokemonName()} used {selectedMove}\n'
                                           f'HAHA he missed.\n{self.rival.getName()}\'s {self.rival.getCurrentPokemonName()} still has {rivalRemainingMonHealth} HP left!',
                                           self.rival.getCurrentPokemonName(),
                                           self.currentMon
                                           )
                    loop = QEventLoop()
                    QTimer.singleShot(3000, loop.quit)
                    loop.exec()

                self.turn += 1
                continue

            # Here AI will choose next move to make
            aiMove = ai_move(self.gameState)
            cpuMove = aiMove
            self.updateMoveHistoryAndGameState('rival', cpuMove, playerRemainingMonHealth, rivalRemainingMonHealth)

            self.currentMon = self.player.getPokemon()[self.player.getCurrentPokemonName()]
            damageDealt = self.rival.getAttackDamage(cpuMove)
            playerRemainingMonHealth = self.player.takeDamage(damageDealt)

            if playerRemainingMonHealth == 0:
                if not self.player.canContinue():
                    break

                self.updatePlayerStatus(f'{self.rival.getCurrentPokemonName()} used {cpuMove}\n'
                                        f'Oh no! Your {self.player.getCurrentPokemonName()} is down!',
                                        self.player.getCurrentPokemonName(),
                                        self.currentMon
                                        )
                loop = QEventLoop()
                QTimer.singleShot(3000, loop.quit)
                loop.exec()

                self.loop = QEventLoop()
                self.showPlayerAvailablePokemon(self.player.getPokemon())
                self.loop.exec()

                selectedPokemon = self.selectedOption.split('\n')[0]

                self.player.setCurrentPokemon(selectedPokemon)
                self.updatePlayerStatus(f'You sent out {self.player.getCurrentPokemonName()}',
                                        self.player.getCurrentPokemonName(),
                                        self.player.getPokemon()[self.player.getCurrentPokemonName()]
                                        )
                loop = QEventLoop()
                QTimer.singleShot(3000, loop.quit)
                loop.exec()

                self.turn = 0
                continue

            if damageDealt > 0:
                self.updatePlayerStatus(f'{self.rival.getCurrentPokemonName()} used {cpuMove}\n'
                                        f'WOW! {self.rival.getCurrentPokemonName()} dealt {damageDealt} to your {self.player.getCurrentPokemonName()}\n'
                                        f'Your {self.player.getCurrentPokemonName()} only has {playerRemainingMonHealth} HP left!',
                                        self.player.getCurrentPokemonName(),
                                        self.currentMon
                                        )
                loop = QEventLoop()
                QTimer.singleShot(3000, loop.quit)
                loop.exec()
            else:
                self.updatePlayerStatus(f'{self.rival.getCurrentPokemonName()} used {cpuMove}\n'
                                        f'HAHA he missed.\nYour {self.player.getCurrentPokemonName()} still has {playerRemainingMonHealth} HP left!',
                                        self.player.getCurrentPokemonName(),
                                        self.currentMon
                                        )
                loop = QEventLoop()
                QTimer.singleShot(3000, loop.quit)
                loop.exec()

            self.turn = 0

        if self.player.canContinue():
            pass
            # Show Win Text
        else:
            pass
            # Show Lose Text

        self.showBattleAgainScreen()

    def updateMoveHistoryAndGameState(self, agent: str, move: str, playerRemainingMonHealth: int,
                                      rivalRemainingMonHealth: int):
        self.moveHistory.append((agent, move))
        updateGameState(self.gameState, self.player, self.rival, self.player.getAllPokemon(),
                        self.rival.getAllPokemon(),
                        self.player.getCurrentPokemon(), self.rival.getCurrentPokemon(), len(self.player.getPokemon()),
                        len(self.rival.getPokemon()), playerRemainingMonHealth, rivalRemainingMonHealth,
                        self.moveHistory,
                        self.turn)

    def updatePlayerStatus(self, textToDisplay: str, pokeName: str, pokemon: Pokemon):
        self.battleOptions.showText(textToDisplay)
        self.battleScreen.setPlayerPokemonStatus(pokeName, int(pokemon.getHealth()),
                                                 pokemon.getHealth() / Constants.POKEMON[pokeName][0])

    def updatePlayerMoves(self, pokemon: Pokemon):
        self.battleOptions.updateMoveList(pokemon.getMoves())
        for i in range(self.battleOptions.layout().count()):
            button = self.battleOptions.layout().itemAt(i).widget()
            button.clicked.connect(self.clickedOption)

    def updateEnemyStatus(self, textToDisplay: str, pokeName: str, pokemon: Pokemon):
        self.battleOptions.showText(textToDisplay)
        self.battleScreen.setEnemyPokemonStatus(pokeName, pokemon.getHealth(),
                                                pokemon.getHealth() / Constants.POKEMON[pokeName][0])

    def showPlayerAvailablePokemon(self, pokeDict: dict):
        self.battleOptions.updatePokemonList(pokeDict, self)

    def clickedOption(self):
        sender = self.sender()
        self.selectedOption = sender.text()
        self.loop.quit()

    def getRivalName(self):
        sender = self.sender()
        self.rivalName = sender.rivalNameTextBox.text()
        self.loop.quit()


class BattleOptions(QFrame):
    def __init__(self):
        super().__init__()
        self.moveList = []

        self.setStyleSheet("background-color: rgb(235, 235, 230);"
                           "border-width: 6;"
                           "border-radius: 7;"
                           "border-style: solid;"
                           "border-color: rgb(0, 0, 0);"
                           )
        self.setFixedSize(QSize(700, 160))

        self.setLayout(self.OptionLayout())

    def clearLayout(self):
        for i in reversed(range(self.layout().count())):
            self.layout().itemAt(i).widget().setParent(None)

    def showText(self, text: str):
        self.clearLayout()
        self.layout().addWidget(self.TextLabel(text))

    def updateMoveList(self, moveList: dict):
        self.clearLayout()
        for count, (moveName, move) in enumerate(moveList.items()):
            position = [int(i) for i in f'{count:02b}']
            self.layout().addWidget(self.AttackButton(moveName, move), *position)

    def updatePokemonList(self, pokemonList: dict, parent: MainWindow):
        self.clearLayout()
        for count, (moveName, move) in enumerate(pokemonList.items()):
            position = [int(i) for i in f'{count:02b}']
            pokeButton = self.PokemonButton(moveName, move)
            pokeButton.clicked.connect(parent.clickedOption)
            self.layout().addWidget(pokeButton, *position)

    def showStartButton(self, parent: MainWindow):
        self.clearLayout()
        self.layout().addWidget(self.EnterRivalNameLabel(), 0, 0)

        rivalNameTextBox = self.RivalNameTextBox()
        startButton = self.StartButton(rivalNameTextBox)
        startButton.clicked.connect(parent.getRivalName)

        self.layout().addWidget(rivalNameTextBox, 1, 0)
        self.layout().addWidget(startButton, 2, 0)

    def showBattleButton(self, parent: MainWindow):
        self.clearLayout()

        battleAgain = self.BattleAgainButton()
        battleAgain.clicked.connect(parent.clickedOption)

        self.layout().addWidget(battleAgain, 0, 0)

    class OptionLayout(QGridLayout):
        def __init__(self):
            super().__init__()
            self.setContentsMargins(1, 1, 1, 1)
            self.setSpacing(3)

    class AttackButton(QPushButton):
        def __init__(self, moveName: str, move: Move):
            super().__init__()
            self.setStyleSheet("border-radius: 1;"
                               "padding: 17px 0;"
                               "width: 100%;"
                               "height: 100%;"
                               "border-width: 2px;"
                               "text-transform: uppercase;"
                               "letter-spacing: 2px;"
                               "color: white;"
                               "font-size: 14px;"
                               "text-align: center;"
                               "background-color: rgb(210, 50, 50);"
                               )
            self.setText(
                f'''{moveName}
PWR: {move.getDamage()} | HIT: {int(move.getHitChance() * 100)}% | PP:{move.getPP()}
''')

    class PokemonButton(QPushButton):
        def __init__(self, pokeName: str, pokemon: Pokemon):
            super().__init__()
            self.setStyleSheet("border-radius: 1;"
                               "padding: 17px 0;"
                               "width: 100%;"
                               "height: 100%;"
                               "border-width: 2px;"
                               "text-transform: uppercase;"
                               "letter-spacing: 2px;"
                               "color: white;"
                               "font-size: 14px;"
                               "text-align: center;"
                               "background-color: rgb(90, 90, 220);"
                               )
            self.setText(
                f'''{pokeName}
HP:{pokemon.getHealth()}
''')

    class TextLabel(QLabel):
        def __init__(self, text: str):
            super().__init__()
            self.setStyleSheet("border: none;"
                               "padding-bottom: 110px;"
                               "padding-left: 5px;"
                               "vertical-align: top;"
                               "width: 100%;"
                               "height: 100%;"
                               "text-transform: uppercase;"
                               "letter-spacing: 3px;"
                               "color: black;"
                               "font-size: 17px;"
                               "text-align: left;"
                               )
            self.setText('- ' + text)

    class EnterRivalNameLabel(QLabel):
        def __init__(self):
            super().__init__()
            self.setStyleSheet("border: none;"
                               "letter-spacing: 3px;"
                               "color: black;"
                               "font-size: 16px;"
                               "text-align: center;"
                               )
            self.setFixedSize(200, 20)
            self.setAlignment(Qt.AlignCenter)
            self.setText('Enter Rival\'s Name:')

    class RivalNameTextBox(QLineEdit):
        def __init__(self):
            super().__init__()
            self.setStyleSheet("vertical-align: top;"
                               "border-width: 2px;"
                               "text-transform: uppercase;"
                               "letter-spacing: 3px;"
                               "color: black;"
                               "font-size: 12px;"
                               "text-align: center;"
                               )
            self.setAlignment(Qt.AlignHCenter)
            self.setFixedSize(200, 18)

    class StartButton(QPushButton):
        def __init__(self, rivalNameTextBox):
            super().__init__()
            self.rivalNameTextBox = rivalNameTextBox
            self.setStyleSheet("border-radius: 6;"
                               "border-width: 2px;"
                               "text-transform: uppercase;"
                               "letter-spacing: 3px;"
                               "color: white;"
                               "font-size: 18px;"
                               "text-align: center;"
                               "background-color: rgb(90, 90, 220);"
                               )
            self.setFixedSize(200, 50)
            self.setText('Start')

    class BattleAgainButton(QPushButton):
        def __init__(self):
            super().__init__()
            self.setStyleSheet("border-radius: 6;"
                               "border-width: 2px;"
                               "text-transform: uppercase;"
                               "letter-spacing: 3px;"
                               "color: white;"
                               "font-size: 18px;"
                               "text-align: center;"
                               "background-color: rgb(90, 90, 220);"
                               )
            self.setFixedSize(200, 50)
            self.setText('Battle Again')


class BattleScreen(QFrame):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("background-color: rgb(141, 178, 247);")
        self.setFixedSize(QSize(700, 290))

        layout = QVBoxLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)

        background = QLabel()
        pixmap = QPixmap(Constants.BACKGROUND)
        background.setPixmap(pixmap)
        layout.addWidget(background)

        backgroundLayout = QGridLayout()
        backgroundLayout.setSpacing(15)

        self.enemyStatusBar = QLabel()
        self.enemyStatusBar.setFixedSize(290, 70)
        self.enemyStatusBar.setStyleSheet("background-color: rgb(220, 220, 240);"
                                          "border-width: 6;"
                                          "border-radius: 5;"
                                          "border-style: solid;"
                                          "border-color: rgb(20, 20, 90);"
                                          )
        self.playerStatusBar = QLabel()
        self.playerStatusBar.setFixedSize(290, 70)
        self.playerStatusBar.setStyleSheet("background-color: rgb(220, 220, 240);"
                                           "border-width: 6;"
                                           "border-radius: 5;"
                                           "border-style: solid;"
                                           "border-color: rgb(20, 20, 90);"
                                           )
        backgroundLayout.addWidget(self.enemyStatusBar, 0, 0)
        backgroundLayout.addWidget(self.playerStatusBar, 1, 1)
        background.setLayout(backgroundLayout)
        self.enemyStatusBar.setLayout(self.StatusBarLayout('', 100, 1))
        self.playerStatusBar.setLayout(self.StatusBarLayout('', 100, 1))

        self.setLayout(layout)

    def setEnemyPokemonStatus(self, name: str, health: int, percent: float):
        self.enemyStatusBar.layout().updateStatus(name, health, percent)

    def setPlayerPokemonStatus(self, name: str, health: int, percent: float):
        self.playerStatusBar.layout().updateStatus(name, health, percent)

    class StatusBarLayout(QVBoxLayout):
        HEALTH_BAR_MAX_SIZE = 260
        RED = '(199, 17, 4)'
        YELLOW = '(214, 210, 79)'
        GREEN = '(35, 166, 63)'

        def __init__(self, name: str, health: int, percent: float):
            super().__init__()
            self.setAlignment(Qt.AlignHCenter)
            self.setContentsMargins(0, 0, 0, 5)
            self.setSpacing(0)

            self.nameLabel = QLabel()
            self.nameLabel.setText(name)
            self.nameLabel.setFixedSize(270, 20)
            self.nameLabel.setStyleSheet("border: none;")

            healthBarContainer = QWidget()
            healthBarContainer.setFixedSize(self.HEALTH_BAR_MAX_SIZE, 15)

            healthBarContainer.setStyleSheet("border-style: solid;"
                                             "border-width: 1px;"
                                             "display: inline-block;"
                                             )
            healthBarContainerLayout = QHBoxLayout()
            healthBarContainerLayout.setContentsMargins(0, 0, 0, 0)
            healthBarContainerLayout.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)

            self.healthBar = QLabel()
            if percent > .15:
                self.healthBar.setText(str(health))
            self.healthBar.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
            self.healthBar.setFixedSize(int(self.HEALTH_BAR_MAX_SIZE * percent), 13)
            color = self.GREEN if percent > .5 else self.YELLOW if percent > .25 else self.RED
            self.healthBar.setStyleSheet("border: none;"
                                         f"background-color: rgb{color};"
                                         )
            healthBarContainerLayout.addWidget(self.healthBar)
            healthBarContainer.setLayout(healthBarContainerLayout)

            self.addWidget(self.nameLabel)
            self.addWidget(healthBarContainer)

        def updateStatus(self, name: str, health: int, percent: float):
            self.nameLabel.setText(name)

            self.healthBar.setFixedSize(int(self.HEALTH_BAR_MAX_SIZE * percent), 13)
            color = self.GREEN if percent > .5 else self.YELLOW if percent > .25 else self.RED
            self.healthBar.setStyleSheet(f"background-color: rgb{color};")
            if percent > .15:
                self.healthBar.setText(str(int(health)))
            else:
                self.healthBar.setText('')


def startMainWindow(sysArgV: list):
    app = QApplication(sysArgV)
    window = MainWindow()
    app.exec()
