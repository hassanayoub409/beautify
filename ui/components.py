#########################################################
#   Written by  :   Hassan Ayoub                        #
#   Date        :   November 30, 2025                   #
#   Purpose     :   Reusable Widgets like               #
#                   'SelectionCard', NodeClass          #
#########################################################

from PyQt5.QtWidgets import QFrame, QLabel, QVBoxLayout, QSizePolicy, QGraphicsEllipseItem
from PyQt5.QtGui import QFont, QFontDatabase, QBrush, QPen
from PyQt5.QtCore import Qt, pyqtSignal

import os
import ui.styles

# SeclectionCard class
class SelectionCard(QFrame):
    '''
    Reusable square card that emits a 'clicked' signal
    when the user presses on it.
    '''

    # signal definition
    clicked = pyqtSignal()

    def __init__(self, title: str, parent=None):
        super().__init__(parent)

        self.setFixedSize(ui.styles.CARD_WIDTH, ui.styles.CARD_HEIGHT)

        self.setStyleSheet('''
            QFrame {
                background: #FEF3C7;
                border-radius: 20px;
                border: 2px solid #FEE2B8;
            }
            QFrame:hover {
                background: #FDE4A9;           
                border-color: #999999;         
            }
                           
        ''')

        currentDir = os.path.dirname(os.path.abspath(__file__))
        projectDir = os.path.dirname(currentDir)
        fontPath = os.path.join(projectDir, "assets", "fonts", "Fragmentcore.otf")

        # The font we will be using
        fontId = QFontDatabase.addApplicationFont(fontPath)
        fontFamily = QFontDatabase.applicationFontFamilies(fontId)
        font = QFont(fontFamily[0], 25)

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)

        label = QLabel(title)
        label.setFont(font)
        label.setAlignment(Qt.AlignCenter)
        label.setWordWrap(True)
        label.setStyleSheet("border: none; color: #92400E; font-weight: bold")
        label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)

        layout.addWidget(label)
        self.setLayout(layout)

    def mousePressEvent(self, event):
        '''
        Emit clicked() when the user presses on the card.
        '''
        self.clicked.emit()

# class to represent a node
class Node(QGraphicsEllipseItem):
    '''
    It is a resusable node to be drawn on a cnavas
    '''

    # constructor
    def __init__(self, nodeId, radius=10):
        # Create the ellipse centered at (0, 0) of diameter radius
        super().__init__(-radius, -radius, 2*radius, 2*radius)

        self.nodeId = nodeId
        self.radius = radius
        self.setBrush(QBrush(Qt.yellow))
        self.setPen(QPen(Qt.black))
        self.setZValue(1)
    
    # Override paint method to draw text inside
    def paint(self, painter, option, widget=None):
        # Draw ellipse normally
        super().paint(painter, option, widget)

        # Draw text inside
        painter.setPen(Qt.black)
        painter.drawText(self.boundingRect(), Qt.AlignCenter, str(self.nodeId))