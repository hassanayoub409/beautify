#########################################################
#   Written by  :   Hassan Ayoub                        #
#   Date        :   December 3, 2025                    #
#   Purpose     :   Implementing Graph Canvas of visual-# 
#                   ization Screen                      #
#########################################################

# imports
from PyQt5.QtWidgets import QGraphicsView, QGraphicsScene, QGraphicsEllipseItem, QGraphicsLineItem, QShortcut
from PyQt5.QtCore import Qt, QTimer, QRectF
from PyQt5.QtGui import QPen, QBrush, QColor, QPainter, QKeySequence

from ui.components import Node

# GraphCanvas class 
class GraphCanvas(QGraphicsView):
    '''
        GraphCanvas
        This class provides the graphical canvas used to display and animate graphs in 
        the Beautify application.

        Attributes:
            scene : QGraphicsScene
                Graphics scene where all nodes and edges are drawn.

            nodeItems : dict[str, Node]
                Maps node IDs to their corresponding QGraphicsEllipseItem (custom Node widget).

            edgeItems : list[tuple[QGraphicsLineItem, str, str]]
                Stores each edge item along with source and target node IDs.

            timer : QTimer
                Timer controlling the animation steps for the force-directed algorithm.

            algo : object or None
                Reference to the active graph layout algorithm. The algorithm must provide
                a `step()` method returning `(positions, finished)`.

            animationInterval : int
                Refresh rate (in ms) for animation updates (default: 16ms ≈ 60 FPS).

            scaleFactor : float
                Multiplier used during zoom operations.

            currentScale : float
                Current zoom level applied to the view.

            minScale, maxScale : float
                Bounds that restrict how far the user can zoom in/out.

        Methods:
            zoomIn()
                Zooms in by applying `scaleFactor`.

            zoomOut()
                Zooms out by applying 1 / `scaleFactor`.

            _applyZoom(factor)
                Internal method to apply zooming while preserving limits and centering.

            drawGraph(graph)
                Clears the canvas and redraws all nodes and edges from the provided Graph object.

            fitToGraph()
                Adjusts the viewport to fully display the drawn graph while keeping aspect ratio.

            _animateStep()
                Executes one frame of the layout algorithm, updating node and edge positions.
                Stops animation when the algorithm signals completion.

            startAnimation(algo)
                Starts animation using the provided algorithm object.

            stopAnimation()
                Stops animation and resets the algorithm state.
    '''

    def __init__(self, width, height):
        super().__init__()

        # Antialiasing for smooth edges
        self.setRenderHint(QPainter.Antialiasing)
        self.setFixedSize(width, height)

        self.scene = QGraphicsScene()
        self.setScene(self.scene)
        self.setBackgroundBrush(QBrush(QColor("#000000")))

        # They key of this dictionary is nodeId and value would be a QGraphicsEllipseItem
        self.nodeItems = {}  

        # This list will store tuples of (QGraphicsLineItem, nodeId1, nodeId2)
        self.edgeItems = []  

        # For animations
        self.timer = QTimer()
        self.timer.timeout.connect(self._animateStep)

        # Eades animation
        self.algo = None
        self.animationInterval = 16

        # Zoom
        self.scaleFactor = 1.2
        self.currentScale = 1.0
        self.minScale = 0.2
        self.maxScale = 5.0

        QShortcut(QKeySequence("+"), self, activated=self.zoomIn)
        QShortcut(QKeySequence("="), self, activated=self.zoomIn)
        QShortcut(QKeySequence("-"), self, activated=self.zoomOut)

    # These methods are implemented to provide zooming feature
    def zoomIn(self):
        self._applyZoom(self.scaleFactor)

    def zoomOut(self):
        self._applyZoom(1 / self.scaleFactor)

    def _applyZoom(self, factor):
        newScale = self.currentScale * factor
        if self.minScale <= newScale <= self.maxScale:
            center = self.mapToScene(self.viewport().rect().center())
            self.scale(factor, factor)
            self.currentScale = newScale
            self.centerOn(center)

    # Method to draw a graph on visualArea
    def drawGraph(self, graph):
        self.scene.clear()

        self.nodeItems.clear()
        self.edgeItems.clear()

        # Draw nodes
        for nodeId, pos in graph.nodes.items():
            ellipse = Node(nodeId, radius=15)
 
            # Use setPos to move the item to the initial graph coordinate
            ellipse.setPos(pos['x'], pos['y'])
            self.scene.addItem(ellipse)

            self.nodeItems[nodeId] = ellipse

        # Draw edges
        drawnEdges = set()
        for u, neighbors in graph.adjList.items():
            for v in neighbors:
                edgeKey = (u, v)
                if edgeKey not in drawnEdges:
                    drawnEdges.add(edgeKey)
                    
                    x1, y1 = graph.nodes[u]['x'], graph.nodes[u]['y']
                    x2, y2 = graph.nodes[v]['x'], graph.nodes[v]['y']
                    
                    line = QGraphicsLineItem(x1, y1, x2, y2)
                    line.setPen(QPen(Qt.white, 2))
                    self.scene.addItem(line)
                    self.edgeItems.append((line, u, v))

    def fitToGraph(self):
        rect = self.scene.itemsBoundingRect()
        if not rect.isNull():
            self.fitInView(rect, Qt.KeepAspectRatio)
    
    def _animateStep(self):
        if self.algo is None:
            return
        
        # Perform a single step of the algorithm
        positions, finished = self.algo.step()

        # Update node positions
        for nodeId, pos in positions.items():
            if nodeId in self.nodeItems:
                self.nodeItems[nodeId].setPos(pos['x'], pos['y'])

        # Update edges
        for line, u, v in self.edgeItems:
            if u in positions and v in positions:
                x1, y1 = positions[u]['x'], positions[u]['y']
                x2, y2 = positions[v]['x'], positions[v]['y']
                line.setLine(x1, y1, x2, y2)
        
        if finished:
            
            self.timer.stop()

    def startAnimation(self, algo):
        self.algo = algo
        self.timer.start(self.animationInterval)

    def stopAnimation(self):
        self.timer.stop()

        if self.algo:
            self.algo.reset()
            self.algo = None