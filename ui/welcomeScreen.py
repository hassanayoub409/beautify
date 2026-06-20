#########################################################
#   Written by  :   Hassan Ayoub                        #
#   Date        :   November 29, 2025                   #
#   Purpose     :   Implementing Welcome Screen for     #
#                   application 'Beautify'              #
#########################################################


# Imports
from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QSizePolicy
from PyQt5.QtGui import QFont, QFontDatabase
from PyQt5.QtCore import Qt, QTimer, pyqtSignal

import os
import ui.styles

# WelcomeScreen class 
class WelcomeScreen(QWidget):
    '''
    This is the first screen of the Beautify application. It serves as the landing page.

    Attributes:
        titleText : str
            The full title text to display with typewriter effect ("Beautify").
        title : QLabel
            QLabel widget for the main title.
        subtitle : QLabel
            QLabel widget for the subtitle.
        nameLabel : QLabel
            QLabel widget for the creator's name at the bottom-right.
        timer : QTimer
            Timer controlling the typewriter animation of the title.
        current_index : int
            Index of the current character being displayed in the title.
    
    Methods:
        update_title()
            Updates the title label with the next character for the typewriter animation.
        showRemainingText()
            Shows the subtitle, name label and emits `animationFinished` signal.
    '''
    
    animationFinished = pyqtSignal()

    # Constructor
    def __init__(self):
        # Activating SuperClass
        super().__init__()

        # Window Properties
        self.setFixedSize(ui.styles.SCREEN_WIDTH, ui.styles.SCREEN_HEIGHT)
        self.setWindowTitle('Beautify')
        self.setStyleSheet("background-color: #5BB450;")

        # Path to font
        currentDir = os.path.dirname(os.path.abspath(__file__))
        projectDir = os.path.dirname(currentDir)
        fontPath = os.path.join(projectDir, "assets", "fonts", "bleedingCowboys.ttf")
        nameFontPath = os.path.join(projectDir, "assets", "fonts", "Rainbow After Rain.ttf")

        # The font we will be using
        fontId = QFontDatabase.addApplicationFont(fontPath)
        fontFamily = QFontDatabase.applicationFontFamilies(fontId)
        font = QFont(fontFamily[0], 120)

        fontId = QFontDatabase.addApplicationFont(nameFontPath)
        fontFamily = QFontDatabase.applicationFontFamilies(fontId)
        nameFont = QFont(fontFamily[0], 30)

        # The main Vertical layout
        self.mainLayout = QVBoxLayout()
        self.mainLayout.setAlignment(Qt.AlignCenter)

        # Creating required widgets
        self.titleText = 'Beautify'
        self.title = QLabel('')
        self.title.setFont(font)
        self.title.setAlignment(Qt.AlignCenter)
        self.title.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        self.title.setStyleSheet('color: #FFD700; padding-left: 40px; padding-bottom: 100px;')

        self.subtitle = QLabel('A force-directed graph visualizer')
        self.subtitle.setFont(QFont('Palatino', 20))
        self.subtitle.setAlignment(Qt.AlignCenter)
        self.subtitle.setStyleSheet('color: #000000;')
        self.subtitle.hide()

        self.nameLabel = QLabel('Created by Hassan Ayoub', self)
        self.nameLabel.setFont(nameFont)
        self.nameLabel.setStyleSheet('color: #000000;')
        self.nameLabel.adjustSize()
        self.nameLabel.move(self.width() - self.nameLabel.width() - 20, self.height() - self.nameLabel.height() - 20)
        self.nameLabel.hide()

        # Add to the main layout
        self.mainLayout.addWidget(self.title)
        self.mainLayout.addWidget(self.subtitle)

        # Set the window to the main layout
        self.setLayout(self.mainLayout)

        # Typewriter animation
        self.current_index = 0
        self.timer = QTimer()
        self.timer.setInterval(200)                     # milliseconds per letter
        self.timer.timeout.connect(self.update_title)
        self.timer.start()

    def update_title(self):
        '''
        Add next letter to title
        '''

        if self.current_index < len(self.titleText):
            self.title.setText(self.title.text() + self.titleText[self.current_index])
            self.current_index += 1
        else:
            self.timer.stop()
            QTimer.singleShot(1000, self.showRemainingText)
            

    def showRemainingText(self):
        '''
        This method prints the rest of text on screen

        The rest of text would be:
            - A force-directed graph visualizer
            - Created by Hassan Ayoub
        '''
        self.subtitle.show()
        self.nameLabel.show()
        QTimer.singleShot(1500, self.animationFinished.emit)