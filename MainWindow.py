from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtCore import Qt
import sys

from Pokemon import *
from Trainer import Trainer
import Constants


def quitLoopAndReturnMoveName(button: QPushButton):
    return button.text()


class MainWindow(QMainWindow):
    # Max 4
    POKEMON_PER_TRAINER = 2

    def __init__(self):
        super().__init__()
        self.setAutoFillBackground(True)

        palette = self.palette()
        palette.setColor(QPalette.Window, QColor(141, 178, 247))
        self.setPalette(palette)

        self.setWindowTitle("ExpectiMax Battle")
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

        self.turn = 0
        playerName = input('Input your name: ')
        rivalName = input('Input my grandson\'s name: ')
        rivalIsSpecialTrainer = False
        if rivalName.capitalize() in Constants.TRAINERS_LIST:
            rivalName = rivalName.capitalize()
            print(f'You\'ve called special trainer {rivalName}')
            rivalIsSpecialTrainer = True

        self.player = Trainer(playerName, tuple(random.sample(Constants.POKEMON_LIST, k=self.POKEMON_PER_TRAINER)))
        if rivalIsSpecialTrainer:
            self.rival = Trainer(rivalName,
                                 tuple(random.sample(Constants.TRAINERS[rivalName], k=self.POKEMON_PER_TRAINER)))
        else:
            self.rival = Trainer(rivalName, tuple(random.sample(Constants.POKEMON_LIST, k=self.POKEMON_PER_TRAINER)))

        self.show()
        self.startGameLoop()

    def startGameLoop(self):
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

        while self.player.canContinue() and self.rival.canContinue():
            if self.turn == 0:

                self.loop = QEventLoop()
                self.updatePlayerMoves(self.player.getPokemon()[self.player.getCurrentPokemonName()])
                self.loop.exec()

                sys.exit()

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
                    print(
                        f'WOW! {player.getCurrentPokemonName()} dealt {damageDealt} to {rivalName}\'s {rival.getCurrentPokemonName()}')
                    print(f'{rivalName}\'s {rival.getCurrentPokemonName()} only has {rivalRemainingMonHealth} HP left!')
                else:
                    print(f'HAHA he missed.')
                    print(
                        f'{rivalName}\'s {rival.getCurrentPokemonName()} still has {rivalRemainingMonHealth} HP left!')
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

    def updatePlayerStatus(self, textToDisplay: str, pokeName: str, pokemon: Pokemon):
        self.battleOptions.showText(textToDisplay)
        self.battleScreen.setPlayerPokemonStatus(pokeName, pokemon.getHealth(),
                                                 pokemon.getHealth() / Constants.POKEMON[pokeName][0])

    def updatePlayerMoves(self, pokemon: Pokemon):
        self.battleOptions.updateMoveList(pokemon.getMoves())
        for i in range(self.battleOptions.layout().count()):
            button = self.battleOptions.layout().itemAt(i).widget()
            button.clicked.connect(self.clickedAttackOption)

    def updateEnemyStatus(self, textToDisplay: str, pokeName: str, pokemon: Pokemon):
        self.battleOptions.showText(textToDisplay)
        self.battleScreen.setEnemyPokemonStatus(pokeName, pokemon.getHealth(),
                                                pokemon.getHealth() / Constants.POKEMON[pokeName][0])

    def showPlayerAvailablePokemon(self, pokeDict: dict):
        self.battleOptions.updatePokemonList(pokeDict)

    def clickedAttackOption(self):
        sender = self.sender()
        print(sender.text())
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
            self.layout().addWidget(self.AttackButton(moveName, move), position[0], position[1])

    def updatePokemonList(self, pokemonList: dict):
        self.clearLayout()
        for count, (moveName, move) in enumerate(pokemonList.items()):
            position = [int(i) for i in f'{count:02b}']
            self.layout().addWidget(self.PokemonButton(moveName, move), position[0], position[1])

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
                self.healthBar.setText(str(health))


app = QApplication(list())
#
window = MainWindow()
window.show()
#
# #window.battleOptions.showText('WOW, His charizard fucked yours up my god...')
#
# pikachu = Pokemon(*Constants.POKEMON[Constants.PIKACHU])
# window.battleOptions.updateMoveList(pikachu.getMoves())
#
# # jose = Trainer('Jose', tuple(random.sample(Constants.POKEMON_LIST, 3)))
# # window.battleOptions.updatePokemonList(jose.getPokemon())
#
# #window.battleScreen.setEnemyPokemonStatus('Pikachu', 100, 1)
# #window.battleScreen.setPlayerPokemonStatus('Machop', 200, 1)
#
# window.battleScreen.setEnemyPokemonStatus('Pikachu', 50, .5)
# window.battleScreen.setPlayerPokemonStatus('Machop', 49, .17)
#
app.exec()
