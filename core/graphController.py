#########################################################
#   Written by  :   Hassan Ayoub                        #
#   Date        :   December 4, 2025                    #
#   Purpose     :   Handle the communication between    #
#                   graphModel.py and visualization     #
#                   Screen.py                           #
#########################################################

from core.graphModel import getDesarguesGraph, getDodecahedralGraph, getIcosahedralGraph, getKarateClubGraph, getFlorentineFamiliesGraph
import ui.styles

# A simple function to which return the graph based on the Graph Name
def getGraph(canvasWidth, canvasHeight, graphName):
    if graphName == ui.styles.DESARGUES_GRAPH:
        return getDesarguesGraph(canvasWidth, canvasHeight)
    if graphName == ui.styles.KARATE_CLUB_GRAPH:
        return getKarateClubGraph(canvasWidth, canvasHeight)
    if graphName == ui.styles.ICOSAHEDRAL_GRAPH:
        return getIcosahedralGraph(canvasWidth, canvasHeight)
    if graphName == ui.styles.DODECAHEDRAL_GRAPH:
        return getDodecahedralGraph(canvasWidth, canvasHeight)
    if graphName == ui.styles.FLORENTINE_FAMILIES:
        return getFlorentineFamiliesGraph(canvasWidth, canvasHeight)