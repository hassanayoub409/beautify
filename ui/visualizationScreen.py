#########################################################
#   Written by  :   Hassan Ayoub                        #
#   Date        :   December 2, 2025                    #
#   Purpose     :   Implementing Graph visualization    # 
#                   Screen                              #
#########################################################

# Imports
from PyQt5.QtWidgets import (
    QWidget, QHBoxLayout, QVBoxLayout, QLabel, QPushButton, 
    QGroupBox, QRadioButton, QFormLayout, QDialog, 
    QDoubleSpinBox, QSizePolicy
)

from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QPixmap

from ui.graphInputScreen import GraphInputScreen

import os

import core.algorithms.eades
import core.algorithms.fruchtermanReingold
import core.algorithms.tutte
import ui.styles

from ui.graphCanvas import GraphCanvas
from core.graphController import getGraph

# class for graphVisualizationScreen
class GraphVisualizationScreen(QWidget):
    '''
    This class represents the main visualization screen of the Beautify application.

    Attributes:
        graphName : str
            Name of the graph selected or created by the user.
        selectedAlgo : str or None
            The name of the currently selected algorithm.
        customGraph : Graph
            The graph object being visualized.
        visualArea : GraphCanvas
            The canvas widget that draws and animates the graph.
        optionsPanel : QWidget
            The right-hand control panel containing algorithm and parameter controls.
        algorithms : dict
            Mapping of algorithm names to their parameter definitions and defaults.
        paramWidgets : dict
            Dictionary storing QDoubleSpinBox widgets for the selected algorithm's parameters.
        radioButtons : list
            List of QRadioButton objects representing available algorithms.
        paramBox : QGroupBox
            Group box containing dynamic parameter controls.
        paramForm : QFormLayout
            Layout that dynamically holds parameter spinboxes.
        btnStart : QPushButton
            Button to start the selected algorithm animation.
        btnStop : QPushButton
            Button to stop/reset the animation.

    Methods:
        buildOptionsPanel()
            Builds and returns the control panel widget for algorithm options.
        
        wrapAsGroup(layout)
            Wraps a layout inside a styled QWidget container.
        
        onBack()
            Handles Back button click and emits `backRequested`.
        
        onAlgorithmChange()
            Triggered when a radio button is toggled; loads parameters accordingly.
        
        loadParameters(algoName)
            Dynamically populates the parameter form for the chosen algorithm.
        
        startAnimation()
            Collects parameters, initializes the selected algorithm, and starts animation.
        
        stopAnimation()
            Stops the graph animation and re-enables UI controls.
        
        showAlgoExplanation()
            Opens a dialog displaying explanatory images of the selected algorithm.
        
        setImages(layout)
            Loads and displays algorithm-related images inside the explanation dialog.
'''

    # Emits when user presses Back
    backRequested = pyqtSignal()

    # Constructor
    def __init__(self, graphName):
        super().__init__()

        self.setStyleSheet('background-color: #FDE4A9;')
        self.graphName = graphName
        self.selectedAlgo = None

        # the key of this dictionary would be an algo's name and value would be a spinbox 
        self.paramWidgets = {}
        self.algorithms = {
            # Some good values:
            # l, delta
            # For Desargue Graph:
            # 232, 0.97
            # 232, 0.99
            # For Karate Club Graph:
            # 300, 0.99
            # For Icosahedral Graph:
            # 400, 0.99
            # For Dodecahedral Graph:
            # 120, 0.99
            # For Florentine Families Graph:
            # 150, 0.99
            ui.styles.FRUCHTERMAN_REINGOLD_ALGO: {
                'l': ('Edge Length', 110, 0.1, float('inf')),
                'delta': ('Cooling Factor', 0.97, 0.1, 1.0)
            },
            # Some good values:
            # radius, delta
            # For Desargue Graph
            # 520, 1.0
            # For Karate Club Graph:
            # 1000, 0.99
            # For Icosahedral Graph:
            # 420, 0.90
            # For Dodecahedral Graph:
            # 500, 0.70
            # For Florentine Families Graph:
            # No good values could be found
            ui.styles.TUTTE_DRAWING: {
                'radius': ('Radius', 300, 1, float('inf')),
                'delta': ('Cooling Factor', 0.7, 0.1, 1.0)
            },
            # Some good values:
            # l, cSpring, cRep, delta
            # For Desargue Graph:
            # 112, 45, 10000, 0.99
            # 150, 10, 10000, 0.99
            # For Karate Club Graph:
            # No good values could be found
            # For Icosahedral Graph:
            # No good values could be found
            # For Dodecahedral Graph:
            # No good values could be found
            # For Florentine Families Graph:
            # No good values could be found: 670, 40, 12000, 0.99
            ui.styles.EADES_SPRING_EMBEDDER: {
                'l': ('Edge Length', 110, 0.1, float('inf')),
                'cSpring': ('Spring Constant', 40, 0.1, float('inf')),
                'cRep': ('Repulsion Constant', 8000, 0.1, float('inf')),
                'delta': ('Cooling Factor', 0.99, 0.1, 1.0),
            }
        }

        self.setWindowTitle('Beautify')
        self.setFixedSize(ui.styles.SCREEN_WIDTH, ui.styles.SCREEN_HEIGHT)

        mainLayout = QHBoxLayout()
        mainLayout.setContentsMargins(10, 10, 10, 10)

        canvasWidth = int(ui.styles.SCREEN_WIDTH * 0.72)
        canvasHeight = ui.styles.SCREEN_HEIGHT - 20

        self.visualArea = GraphCanvas(canvasWidth, canvasHeight)

        if graphName == ui.styles.INPUT_GRAPH:
            
            inputScreen = GraphInputScreen(canvasWidth, canvasHeight)
            result = inputScreen.exec_()
            
            if result == QDialog.Accepted:
                self.customGraph = inputScreen.getGraph()
                self.graphName = 'Your Graph'
            else:
                # Exception is raised to stop __init__ to complete
                raise Exception('Graph input cancelled by user.') 
        elif graphName is not None:
            self.customGraph = getGraph(canvasWidth, canvasHeight, self.graphName)
        else:
            raise Exception

        self.visualArea.drawGraph(self.customGraph)
        self.visualArea.fitToGraph()

        self.visualArea.setAlignment(Qt.AlignCenter)
        self.visualArea.setStyleSheet('''
            background-color: #000000;
            border-radius: 15px;
            color: #FFFF00;
            font-size: 24px;
        ''')
        self.visualArea.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Expanding)
        self.visualArea.setFixedWidth(int(ui.styles.SCREEN_WIDTH * 0.72))

        self.optionsPanel = self.buildOptionsPanel()
        self.optionsPanel.setFixedWidth(int(ui.styles.SCREEN_WIDTH * 0.25))

        mainLayout.addWidget(self.visualArea)
        mainLayout.addWidget(self.optionsPanel)

        self.setLayout(mainLayout)

    def buildOptionsPanel(self):
        '''
            Builds the control panel of Visualization Screen
        '''
        panel = QVBoxLayout()
        panel.setAlignment(Qt.AlignTop | Qt.AlignHCenter)
        panel.setSpacing(25)
        panel.setContentsMargins(15, 15, 15, 15)

        # Title
        title = QLabel(f'Options\n')
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet('font-size: 28px; font-weight: bold; color: #000000; text-decoration: underline')
        panel.addWidget(title)

        # Algorithm selection
        # QGroupBox groups similar widgets together
        algoBox = QGroupBox('Choose Algorithm')
        algoBox.setStyleSheet('''
            QGroupBox {
                font-size: 22px;
                font-weight: bold;
                color: #000000;
                border: 2px solid #000000;
                border-radius: 10px;
                padding: 10px;
            }
        ''')
        algoLayout = QVBoxLayout()
        algoLayout.setSpacing(20)
        algoLayout.setContentsMargins(0, 25, 0, 0)

        self.radioButtons = []
        for algoName in self.algorithms.keys():
            rb = QRadioButton(algoName)
            rb.setStyleSheet('font-size: 20px;')
            rb.toggled.connect(self.onAlgorithmChange)
            self.radioButtons.append(rb)
            algoLayout.addWidget(rb)

        algoBox.setLayout(algoLayout)
        panel.addWidget(algoBox)

        # Parameter Section
        self.paramBox = QGroupBox('Parameters')
        self.paramBox.setStyleSheet('''
            QGroupBox {
                font-size: 22px;
                font-weight: bold;
                color: #000000;
                border: 2px solid #000000;
                border-radius: 10px;
                padding: 10px;
            }
        ''')
        
        # Used to create form-type layouts
        self.paramForm = QFormLayout()
        self.paramForm.setContentsMargins(0, 25, 0, 0)
        self.paramForm.setLabelAlignment(Qt.AlignLeft)
        self.paramForm.setFormAlignment(Qt.AlignTop)
        self.paramForm.setHorizontalSpacing(15)
        self.paramForm.setVerticalSpacing(10)

        self.paramBox.setLayout(self.paramForm)
        panel.addWidget(self.paramBox)

        # Buttons
        btnUnderstand = QPushButton('Understand Algorithm')
        btnUnderstand.setStyleSheet('''
            QPushButton{
                background-color: #FF6B1A;
                color: #1A0D00;
                font-size: 18px;
                padding: 8px;    
                border: 2px solid #000000;                                
            }
            QPushButton:hover {
                background-color: #E85D04;
                color: #FFFFFF;
            }
        ''')
        btnUnderstand.clicked.connect(self.showAlgoExplanation)
        panel.addWidget(btnUnderstand)

        self.btnStart = QPushButton('Start')
        self.btnStart.clicked.connect(self.startAnimation)
        panel.addWidget(self.btnStart)

        self.btnStart.setStyleSheet('''
            QPushButton{
                background-color: #FF6B1A;
                color: #1A0D00;
                font-size: 18px;
                padding: 8px;
                border: 2px solid #000000;                
            }
            QPushButton:hover {
                background-color: #E85D04;
                color: #FFFFFF;
            }
        ''')

        self.btnStop = QPushButton('Reset')
        self.btnStop.clicked.connect(self.stopAnimation)
        panel.addWidget(self.btnStop)

        self.btnStop.setStyleSheet('''
            QPushButton{
                background-color: #FF6B1A;
                color: #1A0D00;
                font-size: 18px;
                padding: 8px;
                border: 2px solid #000000;                
            }
            QPushButton:hover {
                background-color: #E85D04;
                color: #FFFFFF;
            }
        ''')

        btnBack = QPushButton('Back')
        btnBack.clicked.connect(self.onBack)
        btnBack.setStyleSheet('''
            QPushButton{
                background-color: #FF6B1A;
                color: #1A0D00;
                font-size: 18px;
                padding: 8px;
                border: 2px solid #000000;             
            }
            QPushButton:hover {
                background-color: #E85D04;
                color: #FFFFFF;
            }
        ''')
        panel.addWidget(btnBack)

        panel.addStretch()
        return self.wrapAsGroup(panel)

    def wrapAsGroup(self, layout):
        w = QWidget()
        w.setLayout(layout)
        w.setStyleSheet('background-color: #FDE4A9; border-radius: 15px;')
        return w

    def onBack(self):
        self.backRequested.emit()
        self.close()

    def onAlgorithmChange(self):
        clickedRb = self.sender()
        if clickedRb.isChecked():
            self.selectedAlgo = clickedRb.text()
            self.loadParameters(self.selectedAlgo)

    def loadParameters(self, algoName):
        while self.paramForm.rowCount() > 0:
            self.paramForm.removeRow(0)
        self.paramWidgets.clear()

        paramDefs = self.algorithms[algoName]
        for key, (label, default, minv, maxv) in paramDefs.items():
            spin = QDoubleSpinBox()
            spin.setStyleSheet('border: 2px solid black;')
            spin.setRange(minv, maxv)
            spin.setValue(default)
            spin.setMinimumWidth(120)
            self.paramWidgets[key] = spin
            self.paramForm.addRow(label, spin)

    def startAnimation(self):
        if not self.selectedAlgo:
            return

        # Collect parameters
        params = {key: widget.value() for key, widget in self.paramWidgets.items()}

        # Disable UI while animating
        for rb in self.radioButtons:
            rb.setEnabled(False)
        for w in self.paramWidgets.values():
            w.setEnabled(False)
        self.btnStart.setEnabled(False)

        # run selected algorithm
        if self.selectedAlgo == ui.styles.EADES_SPRING_EMBEDDER:
            algo = core.algorithms.eades.Eades(
                self.customGraph,
                l=params['l'],
                cSpring=params['cSpring'], 
                cRep=params['cRep'], 
                delta=params['delta'], 
            )
        elif self.selectedAlgo == ui.styles.FRUCHTERMAN_REINGOLD_ALGO:
            algo = core.algorithms.fruchtermanReingold.FruchtermanReingold(
                self.customGraph,
                l = params['l'],
                delta = params['delta'],
            )
        elif self.selectedAlgo == ui.styles.TUTTE_DRAWING:
            algo = core.algorithms.tutte.Tutte(self.customGraph, 
            radius=params['radius'],
            dampingRate=params['delta'])
            
        self.visualArea.startAnimation(algo)

    def stopAnimation(self):
        for rb in self.radioButtons:
            rb.setEnabled(True)
        for w in self.paramWidgets.values():
            w.setEnabled(True)
        self.btnStart.setEnabled(True)

        self.visualArea.stopAnimation()

    def showAlgoExplanation(self):
        '''
            Handles the dialog box which opens when user clicks Understand Algorithm
        '''
        if not self.selectedAlgo:
            return

        dlg = QDialog(self) 
        dlg.setWindowTitle(f'{self.selectedAlgo} — Explanation')
        dlg.setMinimumSize(700, 700)

        layout = QVBoxLayout()

        self.setImages(layout)

        closeBtn = QPushButton('Close')
        closeBtn.clicked.connect(dlg.close)
        closeBtn.setStyleSheet('''
            QPushButton {
                background-color: #E85D04; 
                color: #FFFFFF;            
                font-size: 18px;           
                font-weight: bold;         
                padding: 10px 20px;         
                border: none;               
                border-radius: 8px;        
                min-width: 120px;           
                margin-top: 15px;           
            }
            QPushButton:hover {
                background-color: #FF8B3D; 
                border: 2px solid #CC4D00; 
            }
            QPushButton:pressed {
                background-color: #CC4D00; 
            }
        ''')
        layout.addWidget(closeBtn)

        dlg.setLayout(layout)
        dlg.exec_()

    def setImages(self, layout):
        '''
            Load the images and display in dialog box 
        '''
        currentDir = os.path.dirname(os.path.abspath(__file__))
        projectDir = os.path.dirname(currentDir)
        basePath = os.path.join(projectDir, 'assets', 'images')

        imgPath1 = os.path.join(basePath, 'forcedirected.png') 

        if self.selectedAlgo == ui.styles.EADES_SPRING_EMBEDDER:
            imgPath2 = os.path.join(basePath, 'eades.png') 
        elif self.selectedAlgo == ui.styles.FRUCHTERMAN_REINGOLD_ALGO:
            imgPath2 = os.path.join(basePath, 'fruchtermanreingold.png') 
        elif self.selectedAlgo == ui.styles.TUTTE_DRAWING:
            imgPath2 = os.path.join(basePath, 'tutte.png')

        imageLabel = QLabel()
        pixmap = QPixmap(imgPath1)     

        imageLabel.setScaledContents(True)
        imageLabel.setSizePolicy(
            QSizePolicy.Policy.Expanding, 
            QSizePolicy.Policy.Expanding
        )
        imageLabel.setPixmap(pixmap)
        layout.addWidget(imageLabel)

        imageLabel2 = QLabel()
        pixmap2 = QPixmap(imgPath2)     

        imageLabel2.setScaledContents(True)
        imageLabel2.setSizePolicy(
            QSizePolicy.Policy.Expanding, 
            QSizePolicy.Policy.Expanding
        )
        imageLabel2.setPixmap(pixmap2)
        layout.addWidget(imageLabel2)