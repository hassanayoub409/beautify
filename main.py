#########################################################
#   Written by  :   Hassan Ayoub                        #
#   Date        :   November 29, 2025                   #
#   Purpose     :   Entry point for Beautify app        #
#########################################################

from PyQt5.QtWidgets import QApplication
from ui.welcomeScreen import WelcomeScreen
from ui.graphSelectionScreen import GraphSelectionScreen
from ui.visualizationScreen import GraphVisualizationScreen

# Beautify class
class Beautify:
    '''
        This module contains the main entry point of the Beautify application.
        It manages screen transitions between the Welcome Screen, Graph Selection
        Screen, and Graph Visualization Screen.

        Attributes:
            app : QApplication
                The main Qt application instance.
            welcome : WelcomeScreen
                The initial animated welcome screen shown on launch.
            selection : GraphSelectionScreen
                The screen where the user selects which graph to visualize.
            visual : GraphVisualizationScreen
                The main visualization interface for drawing and animating graphs.

        Methods:
            __init__()
                Initializes the QApplication and displays the Welcome Screen.

            showWelcomeScreen()
                Creates and shows the Welcome Screen, and connects its completion
                signal to move to the Graph Selection Screen.

            showGraphSelectionScreen()
                Closes the Welcome Screen, opens the Graph Selection Screen, and
                connects its signal to proceed when a graph is chosen.

            onGraphSelected(graphName)
                Callback that receives the selected graph name and proceeds to
                open the Visualization Screen.

            showGraphVisualizationScreen(graphName)
                Closes the Selection Screen and opens the Visualization Screen.
                If graph creation fails (e.g., user cancels input), returns to
                the Selection Screen.

            run()
                Starts the Qt event loop for the application.
    '''


    # Constructor
    def __init__(self):
        self.app = QApplication([])

        # Show Welcome Screen
        self.showWelcomeScreen()

    def showWelcomeScreen(self):
        self.welcome = WelcomeScreen()
        # Connect the signal to move to the next screen
        self.welcome.animationFinished.connect(self.showGraphSelectionScreen)
        # Display Welcome Screen
        self.welcome.show()

    def showGraphSelectionScreen(self):
        # Hide welcome 
        self.welcome.close()

        # Create GraphSelectionScreen object
        self.selection = GraphSelectionScreen()
        # Connect the signal to move to the next screen
        self.selection.graphSelected.connect(self.onGraphSelected)
        # Display Selection Screen
        self.selection.show()

    def onGraphSelected(self, graphName):
        self.showGraphVisualizationScreen(graphName)

    def showGraphVisualizationScreen(self, graphName):
        self.selection.close()

        try:
            self.visual = GraphVisualizationScreen(graphName)

            self.visual.backRequested.connect(self.showGraphSelectionScreen)
            self.visual.show()
        except Exception as _:
            self.showGraphSelectionScreen()
    
    def run(self):
        self.app.exec_()

if __name__ == "__main__":
    app = Beautify()
    app.run()