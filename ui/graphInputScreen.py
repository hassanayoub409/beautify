#########################################################
#   Written by  :   Hassan Ayoub                        #
#   Date        :   December 11, 2025                   #
#   Purpose     :   Implementing Graph Input Screen     #
#########################################################

# imports
from PyQt5.QtWidgets import (
    QDialog, QHBoxLayout, QVBoxLayout, QLabel, QPushButton, 
    QMessageBox, QLineEdit, QWidget, QSizePolicy, QRadioButton, QFrame, QFileDialog
)

from PyQt5.QtCore import Qt
import random

from core.graphModel import Graph 
from ui.graphCanvas import GraphCanvas
import ui.styles

# GraphInput Screen
class GraphInputScreen(QDialog):
    '''
        GraphInputScreen:
        This class represents the main graph-editing screen of the Beautify application.
        It allows the user to build, modify, and validate a graph before sending it to the
        animation window.

        Attributes:
            canvasWidth : int
                Width of the canvas where the graph is displayed.

            canvasHeight : int
                Height of the canvas.

            canvas : GraphCanvas
                Custom drawing widget where nodes and edges are rendered.

            customGraph : Graph
                The underlying graph model being edited.

            finalGraph : Graph or None
                Stores the completed graph when the user presses the Animate button.

            nodeButton : QPushButton
                Button used to add a new node.

            deleteNodeButton : QPushButton
                Button used to delete the selected node.

            addEdgeButton : QPushButton
                Button used to add an edge between the specified nodes.

            deleteEdgeButton : QPushButton
                Button used to remove an existing edge.

            edgeSourceInput : QLineEdit
                Input field where the user enters the source node ID for edge creation.

            edgeTargetInput : QLineEdit
                Input field where the user enters the target node ID for edge creation.

            loadButton : QPushButton
                Button used to trigger graph loading from a file.

            interpretationBox : QComboBox
                Dropdown for selecting the input format (u-v pairs / adjacency list).

            animationButton : QPushButton
                Button that finalizes the graph and closes the dialog.

            cancelButton : QPushButton
                Button that cancels the dialog and discards the graph.

        Methods:
            _addNode()
                Creates a new node with a unique ID and random position.

            _deleteNode()
                Deletes the node currently selected on the canvas.

            _addEdge()
                Adds an edge between two nodes after validating the IDs and preventing duplicates.

            _deleteEdge()
                Removes an existing edge between two specified nodes.

            _loadGraph()
                Loads a complete graph from a file using the selected interpretation.

            _updateCanvas()
                Forces the canvas to redraw the graph.

            _showMessage(text: str)
                Displays a warning dialog using QMessageBox.

            accept()
                Stores the graph as finalGraph and closes the dialog with Accepted status.

            reject()
                Discards changes and closes the dialog with Rejected status.

            getGraph()
                Returns the finalized graph after the dialog closes.
    '''

    # Constructor
    def __init__(self, canvasWidth, canvasHeight):
        super().__init__()

        self.setWindowFlags(Qt.WindowMinimizeButtonHint)

        self.setWindowTitle(ui.styles.INPUT_GRAPH)
        self.setFixedSize(ui.styles.SCREEN_WIDTH, ui.styles.SCREEN_HEIGHT)
        self.setStyleSheet('background-color: #FDE4A9;')

        self.customGraph = Graph()
        self.nextNodeId = 0
        self.finalGraph = None
        
        self.canvasWidth = canvasWidth
        self.canvasHeight = canvasHeight
        
        mainLayout = QHBoxLayout(self)
        mainLayout.setContentsMargins(10, 10, 10, 10)

        self.visualArea = GraphCanvas(canvasWidth, canvasHeight)
        self.visualArea.setAlignment(Qt.AlignCenter)
        self.visualArea.setStyleSheet('''
            background-color: #000000;
            border-radius: 15px;
            color: #FFFF00;
            font-size: 24px;
        ''')
        self.visualArea.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Expanding)
        self.visualArea.setFixedWidth(int(ui.styles.SCREEN_WIDTH * 0.72))

        mainLayout.addWidget(self.visualArea)

        self.fileFormat = ui.styles.EDGE_PAIR
        self.controlPanel = self.buildControlPanel()
        self.controlPanel.setFixedWidth(int(ui.styles.SCREEN_WIDTH * 0.25))

        mainLayout.addWidget(self.controlPanel)
        self._updateCanvas()

    def wrapAsGroup(self, layout):
        w = QWidget()
        w.setLayout(layout)
        w.setStyleSheet('background-color: #FDE4A9; border-radius: 15px;')
        return w

    def buildControlPanel(self):
        '''
        Build the control panel on Graph input screen
        '''
        panel = QVBoxLayout()
        panel.setAlignment(Qt.AlignTop | Qt.AlignHCenter)
        panel.setSpacing(25)
        panel.setContentsMargins(15, 15, 15, 15)

        # Title
        title = QLabel('Graph Editor')
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet('font-size: 28px; font-weight: bold; color: #000000; text-decoration: underline')
        panel.addWidget(title)

        self.btnAddNode = self.createAddNodeButton()
        panel.addWidget(self.btnAddNode)

        deleteNodeSectionLayout = self.createDeleteNodeSection()
        panel.addLayout(deleteNodeSectionLayout)

        addEdgeSectionLayout = self.createAddEdgeSection()
        panel.addLayout(addEdgeSectionLayout)
        
        deleteEdgeSection = self.createDeleteEdgeSection()
        panel.addLayout(deleteEdgeSection)
        
        line1 = self.getHorizontalLine()
        panel.addWidget(line1)

        fileReadingSection = self.createFileSection()
        panel.addLayout(fileReadingSection)

        panel.addStretch()
        
        line2 = self.getHorizontalLine()
        panel.addWidget(line2)
        
        btnAnimate = QPushButton('Animate')
        btnAnimate.clicked.connect(self._finalizeGraph)
        btnAnimate.setStyleSheet('''
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
        panel.addWidget(btnAnimate)
        
        btnCancel = QPushButton('Cancel')
        btnCancel.clicked.connect(self.reject) 
        btnCancel.setStyleSheet('''
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
        panel.addWidget(btnCancel)
        
        return self.wrapAsGroup(panel)

    def getHorizontalLine(self):
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setStyleSheet("QFrame { border: 2px solid #000000; }")
        return line

    def _updateCanvas(self):
        '''
        Redraws the graph on the canvas
        '''
        self.visualArea.drawGraph(self.customGraph)
        self.visualArea.fitToGraph()
        
    def _addNode(self):
        '''
        Adds a new node at a random position using the Graph model's method.
        '''
        nodeId = str(self.nextNodeId)
    
        # Use the Graph model's method
        self.customGraph.addNode(nodeId, random.uniform(50, self.canvasWidth - 50), random.uniform(50, self.canvasHeight - 50))
        
        self.nextNodeId += 1
        self._updateCanvas()
        
    def _addEdge(self):
        '''
        Adds an edge between two existing nodes using the Graph model's method.
        '''
        uId = self.edgeSourceInput.text().strip()
        vId = self.edgeTargetInput.text().strip()
        
        # Check if nodes exist and are not the same
        if uId in self.customGraph.nodes and vId in self.customGraph.nodes and uId != vId:
            # Check if edge already exists to prevent duplication
            if vId not in self.customGraph.adjList[uId]:
                self.customGraph.addEdge(uId, vId)
                
                self.edgeSourceInput.clear()
                self.edgeTargetInput.clear()
                self._updateCanvas()
        else:
            self._showMessage('Error: Invalid node ID(s) or same node selected for edge creation.')

    def _deleteNode(self):
        '''
        Deletes a node and all connected edges.
        '''
        nodeId = self.nodeToDelete.text().strip()
        
        if nodeId in self.customGraph.nodes:
            
            # 1. Remove all references to this node in its neighbors' adjacency lists
            neighbors = list(self.customGraph.adjList.get(nodeId, []))
            for neighborId in neighbors:
                if nodeId in self.customGraph.adjList[neighborId]:
                    self.customGraph.adjList[neighborId].remove(nodeId)
            
            # 2. Delete the node and its adjacency list entry
            del self.customGraph.nodes[nodeId]
            del self.customGraph.adjList[nodeId]
            
            self.nodeToDelete.clear()
            self._updateCanvas()
        else:
            self._showMessage(f'Error: Node ID {nodeId} not found.')

    def _showMessage(self, text):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)
        msg.setText(text)
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()

    def _finalizeGraph(self):
        if not self.customGraph.nodes:
            self._showMessage('Empty Graph')
            return
            
        self.finalGraph = self.customGraph
        self.accept()

    def getGraph(self):
        '''
        Returns the finalized Graph object.
        '''
        return self.finalGraph
    

    def createAddNodeButton(self):
        button = QPushButton(f'Create a Node')
        button.clicked.connect(self._addNode)
        button.setStyleSheet('''
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
        return button

    def createAddEdgeSection(self):
        edgeSectionLayout = QVBoxLayout()

        edgeHorizontalLayout = QHBoxLayout()
        edgeHorizontalLayout.setSpacing(5)
        edgeHorizontalLayout.setContentsMargins(0, 15, 0, 0)

        self.edgeSourceInput = QLineEdit()
        self.edgeTargetInput = QLineEdit()

        self.edgeSourceInput.setStyleSheet('''
            border: 2px solid black;
        ''')
        self.edgeTargetInput.setStyleSheet('''
            border: 2px solid black;
        ''')

        labelSource = QLabel('u:')
        labelTarget = QLabel('v:')
        
        labelSource.setStyleSheet('''
            font-size: 18px; 
            font-weight: bold; 
            color: #000000;
        ''')
        labelTarget.setStyleSheet('''
            font-size: 18px; 
            font-weight: bold; 
            color: #000000;
        ''')

        btnAddEdge = QPushButton('Add Edge')
        btnAddEdge.clicked.connect(self._addEdge)
        btnAddEdge.setStyleSheet('''
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
        edgeHorizontalLayout.addWidget(btnAddEdge) 

        edgeHorizontalLayout.addWidget(labelSource)
        edgeHorizontalLayout.addWidget(self.edgeSourceInput)
        edgeHorizontalLayout.addWidget(labelTarget)
        edgeHorizontalLayout.addWidget(self.edgeTargetInput)

        edgeSectionLayout.addLayout(edgeHorizontalLayout)
        return edgeSectionLayout
    
    def createDeleteNodeSection(self):
        deleteSectionLayout = QVBoxLayout()

        deleteHorizontalLayout = QHBoxLayout()
        deleteHorizontalLayout.setContentsMargins(0, 0, 0, 0)

        self.nodeToDelete = QLineEdit()
        self.nodeToDelete.setStyleSheet('''
            border: 2px solid black;
        ''')
        
        btnDeleteNode = QPushButton('Delete Node')
        btnDeleteNode.clicked.connect(self._deleteNode)
        btnDeleteNode.setStyleSheet('''
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
        
        id = QLabel('Id:')
        id.setStyleSheet('''
            font-size: 18px; 
            font-weight: bold; 
            color: #000000;
        ''')

        deleteHorizontalLayout.addWidget(btnDeleteNode)
        deleteHorizontalLayout.addWidget(id)
        deleteHorizontalLayout.addWidget(self.nodeToDelete)

        deleteSectionLayout.addLayout(deleteHorizontalLayout)
        return deleteSectionLayout
    
    def createDeleteEdgeSection(self):
        edgeSectionLayout = QVBoxLayout()

        edgeHorizontalLayout = QHBoxLayout()
        edgeHorizontalLayout.setSpacing(5)
        edgeHorizontalLayout.setContentsMargins(0, 0, 0, 0)

        self.edgeSourceInputDel = QLineEdit()
        self.edgeTargetInputDel = QLineEdit()

        self.edgeSourceInputDel.setStyleSheet('''
            border: 2px solid black;
        ''')
        self.edgeTargetInputDel.setStyleSheet('''
            border: 2px solid black;
        ''')

        labelSource = QLabel('u:')
        labelTarget = QLabel('v:')
        
        labelSource.setStyleSheet('''
            font-size: 18px; 
            font-weight: bold; 
            color: #000000;
        ''')
        labelTarget.setStyleSheet('''
            font-size: 18px; 
            font-weight: bold; 
            color: #000000;
        ''')

        btnDeleteEdge = QPushButton('Delete Edge')
        btnDeleteEdge.clicked.connect(self._deleteEdge)
        btnDeleteEdge.setStyleSheet('''
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
        edgeHorizontalLayout.addWidget(btnDeleteEdge) 

        edgeHorizontalLayout.addWidget(labelSource)
        edgeHorizontalLayout.addWidget(self.edgeSourceInputDel)
        edgeHorizontalLayout.addWidget(labelTarget)
        edgeHorizontalLayout.addWidget(self.edgeTargetInputDel)

        edgeSectionLayout.addLayout(edgeHorizontalLayout)
        return edgeSectionLayout
    
    def _deleteEdge(self):
        '''
        Deletes an edge between two nodes if it exists.
        '''
        uId = self.edgeSourceInputDel.text().strip()
        vId = self.edgeTargetInputDel.text().strip()
        
        if uId == '' or vId == '':
            self._showMessage('Error: Both Source (u) and Target (v) IDs must be entered.')
            return

        if uId not in self.customGraph.nodes or vId not in self.customGraph.nodes:
            self._showMessage(f'Error: One or both nodes ({uId}, {vId}) do not exist.')
            return

        # Check if the edge exists in the adjacency list
        # Since the graph is undirected, checking one direction is enough (vId in adjList[uId])
        if vId in self.customGraph.adjList.get(uId, []):
            
            # Remove the edge from both directions
            self.customGraph.adjList[uId].remove(vId)
            self.customGraph.adjList[vId].remove(uId)
            
            # Clear the input boxes and update UI
            self.edgeSourceInputDel.clear()
            self.edgeTargetInputDel.clear()
            self._updateCanvas()
        else:
            self._showMessage(f'Error: Edge between {uId} and {vId} does not exist.')
    
    def createFileSection(self):
        '''
        Create File Section in Control Panel
        '''
        section = QVBoxLayout()

        fileFormatUV = self.getRadioButton(ui.styles.EDGE_PAIR)
        fileFormatUV.setChecked(True)
        section.addWidget(fileFormatUV)

        fileFormatAdjList = self.getRadioButton(ui.styles.ADJACENCY_LIST)
        section.addWidget(fileFormatAdjList)

        loadFileButton = QPushButton('Load File')
        loadFileButton.clicked.connect(self.openFileDialog)
        loadFileButton.setStyleSheet('''
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
        section.addWidget(loadFileButton)

        return section


    def getRadioButton(self, text):
        '''
        Returns a radio button with the text label
        '''
        button = QRadioButton(text)
        button.toggled.connect(self.onToggle)
        button.setStyleSheet('font-size: 15px; font-weight: bold')
        return button
    
    def onToggle(self):
        button = self.sender()

        if button.isChecked():
            self.fileFormat = button.text()

    def openFileDialog(self):
        '''
        Handle File Dialog in Control Panel
        '''

        filterString = "Graph Input Files (*.txt)"

        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getOpenFileName(
            self, 
            'Load Graph Input File', 
            '', 
            filterString,
            options=options
        )
        
        if fileName:
            try:
                with open(fileName, 'r') as f:
                    rawData = f.read()
                
                if self.fileFormat == ui.styles.EDGE_PAIR:
                    newGraph = self._parse_format1_uv_pairs(rawData)
                elif self.fileFormat == ui.styles.ADJACENCY_LIST:
                    newGraph = self._parse_format2_adj_list(rawData)

                self.customGraph = newGraph
                
                # Reset nextNodeId for manual editing if the loaded nodes were integers
                try:
                    max_id = max(int(k) for k in self.customGraph.nodes.keys())
                    self.nextNodeId = max_id + 1
                except ValueError:
                    # Node IDs were strings (e.g., 'A', 'B'), keep nextNodeId counter as is
                    self.nextNodeId = 0 
                    
                self._updateCanvas()

            except Exception as e:
                self._showMessage(
                    f'An unexpected error occurred during file loading: {e}'
                )

    def _parse_format1_uv_pairs(self, fileContent):
        '''
        Parses Format 1: 
        Line 1: Total number of nodes (N, e.g., '5')
        Lines 2+: U, V edge pairs (e.g., '0 1' or '2,3')
        '''
        
        lines = [line.strip() for line in fileContent.strip().split('\n') if line.strip()]
        if not lines:
            raise ValueError("File is empty.")

        # Get the number of nodes from the first line
        try:
            numNodes = int(lines[0])
        except ValueError:
            raise ValueError("Line 1 must contain a single integer: the number of nodes.")

        if numNodes <= 0:
            raise ValueError("Number of nodes must be positive.")

        g = Graph()
        
        for i in range(numNodes):
            nodeId = str(i)
            g.addNode(nodeId, random.uniform(50, self.canvasWidth - 50), random.uniform(50, self.canvasHeight - 50))
            
        # 2. Process edge pairs from the remaining lines
        for i, line in enumerate(lines[1:]):
            # Split by any whitespace or comma
            parts = line.replace(',', ' ').split()
            
            if len(parts) != 2:
                raise ValueError(f"Line {i+2}: Edge must be a pair of IDs (e.g., '0 1').")
            
            try:
                u_id_int = int(parts[0])
                v_id_int = int(parts[1])
            except ValueError:
                raise ValueError(f"Line {i+2}: Edge IDs must be integers.")

            uId, vId = str(u_id_int), str(v_id_int)
            
            if u_id_int >= numNodes or v_id_int >= numNodes or u_id_int < 0 or v_id_int < 0:
                raise ValueError(f"Line {i+2}: Node ID must be between 0 and {numNodes - 1}.")
            
            if uId != vId:
                if vId not in g.adjList.get(uId, []):
                    g.addEdge(uId, vId)
        return g
    
    def _parse_format2_adj_list(self, file_content: str) -> Graph:
        '''
        Parses Format 2: 
        Line 1: Total number of nodes (N, e.g., '5')
        Lines 2+: [ID]: [Neighbor1, Neighbor2,...] (e.g., '0: [1, 2]')
        '''

        g = Graph()
        
        lines = [line.strip() for line in file_content.strip().split('\n') if line.strip()]
        if not lines:
            raise ValueError('File is empty.')

        # READ TOTAL NUMBER OF NODES 
        try:
            numNodes = int(lines[0])
        except ValueError:
            raise ValueError('Line 1 must contain a single integer: the total number of nodes (N).')

        if numNodes <= 0:
            raise ValueError('Number of nodes must be positive.')
        
        for i in range(numNodes):
            nodeId = str(i)
            g.addNode(nodeId, random.uniform(50, self.canvasWidth - 50), random.uniform(50, self.canvasHeight - 50))
            
        # Process Adjacency List entries from the remaining lines
        for i, line in enumerate(lines[1:]): 
            # Basic format check
            if ':' not in line or '[' not in line or ']' not in line:
                raise ValueError(f'Line {i+2}: Invalid adjacency list format (expected ID: [N1, N2]).')
            
            try:
                sourcePart, targetsPart = line.split(':', 1)
                sourceId = sourcePart.strip()
                
                # Check if source node ID is within the declared range
                if int(sourceId) >= numNodes or int(sourceId) < 0:
                    raise ValueError(f'Line {i+2}: Source ID {sourceId} is outside the declared range [0, {numNodes - 1}].')
            
                # Clean targetsPart: remove brackets, strip whitespace, split by comma
                targetsList = targetsPart.replace('[', '').replace(']', '').split(',')
                targets = [t.strip() for t in targetsList if t.strip()]

                for targetId in targets:
                    # Check if target node ID is within the declared range
                    if int(targetId) >= numNodes or int(targetId) < 0:
                        raise ValueError(f'Line {i+2}: Target ID {targetId} is outside the declared range [0, {numNodes - 1}].')
                    
                    # Add edge
                    if sourceId != targetId:
                        # addEdge is called knowing both nodes exist from step 2
                        if targetId not in g.adjList.get(sourceId, []):
                            g.addEdge(sourceId, targetId)
            except Exception as e:
                raise ValueError(f'Line {i+2}: Parsing error near {sourcePart}: {e}')

        if not g.nodes and numNodes == 0:
            raise ValueError('No valid nodes found in the file.')
            
        return g