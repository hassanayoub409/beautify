#########################################################
#   Written by  :   Hassan Ayoub                        #
#   Date        :   November 30, 2025                   #
#   Purpose     :   Screen after Welcome is implemented #
#                   here, this screen alows user to se- #
#                   lect a card                         #
#########################################################

# imports
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QGridLayout
from PyQt5.QtGui import QFont, QFontDatabase
from PyQt5.QtCore import Qt, pyqtSignal

import os
from ui.components import SelectionCard
import ui.styles

# SelectionScreen class
class GraphSelectionScreen(QWidget):
    '''
        GraphSelectionScreen

        This class represents the second screen of the Beautify application. 

        Attributes:
            graphSelected : pyqtSignal(str)
                Signal emitted when a card is clicked, carrying the graph name or identifier.

            mainLayout : QVBoxLayout
                The main vertical layout managing the entire screen.

            title : QLabel
                The main header text reading "Select an Option" displayed at the top.

            grid : QGridLayout
                A grid layout used to arrange the selection cards in two rows and three columns.

            cardNames : list[str]
                List of identifiers representing available graph options, sourced from ui.styles.

            positions : list[tuple[int, int]]
                List of (row, column) coordinates for placing the six cards in the grid.

        Methods:
            __init__()
                Initializes the window, loads the custom font, builds the layout, creates 
                the six selection cards, and connects each card's click event to the 
                `graphSelected` signal.
    '''
    graphSelected = pyqtSignal(str)

    # Constructor
    def __init__(self):
        super().__init__()

        # window styling
        self.setWindowTitle('Beautify')
        self.setFixedSize(ui.styles.SCREEN_WIDTH, ui.styles.SCREEN_HEIGHT)
        self.setStyleSheet('background-color: #5BB450;')

        # Main layout
        mainLayout = QVBoxLayout()
        mainLayout.setAlignment(Qt.AlignTop | Qt.AlignHCenter)
        mainLayout.setSpacing(30)

        currentDir = os.path.dirname(os.path.abspath(__file__))
        projectDir = os.path.dirname(currentDir)
        fontPath = os.path.join(projectDir, 'assets', 'fonts', 'Rainbow After Rain.ttf')

        # The font we will be using
        fontId = QFontDatabase.addApplicationFont(fontPath)
        fontFamily = QFontDatabase.applicationFontFamilies(fontId)
        font = QFont(fontFamily[0], 70)

        # Title
        title = QLabel('Select an Option')
        title.setFont(font)
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet('color: #FFD700; margin-top: 30px;')
        mainLayout.addWidget(title)

        # Grid for cards
        grid = QGridLayout()
        grid.setContentsMargins(50, 10, 50, 20)
        grid.setHorizontalSpacing(40)
        grid.setVerticalSpacing(55)

        # 6 card names
        cardNames = [
            ui.styles.DESARGUES_GRAPH,
            ui.styles.KARATE_CLUB_GRAPH,
            ui.styles.ICOSAHEDRAL_GRAPH,
            ui.styles.DODECAHEDRAL_GRAPH,
            ui.styles.FLORENTINE_FAMILIES,
            ui.styles.INPUT_GRAPH
        ]

        positions = [(i, j) for i in range(2) for j in range(3)]

        for pos, name in zip(positions, cardNames):
            card = SelectionCard(name)

            card.clicked.connect(lambda n=name: self.graphSelected.emit(n))
            grid.addWidget(card, *pos)

        mainLayout.addLayout(grid)
        self.setLayout(mainLayout)