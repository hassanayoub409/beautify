#########################################################
#   Written by  :   Hassan Ayoub                        #
#   Date        :   December 7, 2025                    #
#   Purpose     :   Implementing FruchtermanReingold    #
#                   Algorithm                           #
#########################################################

# imports
import math
from core.algorithms.algorithmInterface import Algorithm

# Class to implement FruchtermanReingold Algorithm
class FruchtermanReingold(Algorithm):
    '''
    Implementation of the Fruchterman-Reingold force-directed graph drawing algorithm.

    Each call to `step()` performs a single iteration, updating positions based
    on the forces.

    Attributes:
        graph (Graph):
            The graph instance containing nodes and adjacency information.

        l (float):
            Natural spring length (ideal edge length, denoted k in FR).

        T (float):
            Current temperature (maximum allowed displacement per iteration).

        T_decayRate (float):
            Multiplicative cooling factor applied after each iteration.
            Must be in range (0, 1]. 

        max_iter (int):
            Maximum number of iterations before the algorithm terminates.

        epsilon (float):
            Threshold for maximum node displacement. If all displacements fall below
            this value, the algorithm terminates early.

        positions (dict[int, dict[str, float]]):
            Mutable dictionary storing node positions.
            Format: { nodeId: {"x": float, "y": float} }

        currentIteration (int):
            Number of iterations performed so far.

        isFinished (bool):
            True if the algorithm has converged or reached the maximum iterations.
    '''
    
    # Constructor
    def __init__(self, graph, l=100.0, delta=0.99, max_iter=5000, epsilon=0.1):
        super().__init__()

        # Attributes
        self.graph = graph
        self.l = l

        # Temperature
        self.T = 10.0
        
        self.T_decayRate = delta
        self.max_iter = max_iter
        self.epsilon = epsilon

        # This dictionary is same as graph.nodes.items()
        self.positions = {node: {'x': data['x'], 'y': data['y']} 
                          for node, data in graph.nodes.items()}
        
        self.currentIteration = 0
        self.isFinished = False

    def reset(self):
        '''
        This method will reset the position of graph so next time algorithm could start working on initial configuration.
        '''
        self.positions = {node: {'x': data['x'], 'y': data['y']} 
                          for node, data in self.graph.nodes.items()}
        self.currentIteration = 0
        self.isFinished = False
        self.T = 10.0

    def dist(self, uId, vId):
        '''
        This method uses math.hypot to calculate the Euclidean Distance between two nodes.
        '''
        u = self.positions[uId]
        v = self.positions[vId]
        return math.hypot(v['x'] - u['x'], v['y'] - u['y'])

    def norm(self, uId, vId, d):
        '''
        Returns unit vector from uId to vId. Returns (0,0) if nodes coincide.
        '''
        if d == 0:
            return 0.0, 0.0
        
        dx = (self.positions[vId]['x'] - self.positions[uId]['x']) / d
        dy = (self.positions[vId]['y'] - self.positions[uId]['y']) / d
        return dx, dy

    def forceRep(self, d):
        # Repulsive force: k^2 / d
        '''
        This method calculates the repulsive force given distance
        '''

        return (self.l ** 2) / max(d, 0.01)

    def forceAttr(self, d):
        '''
        This method calculates the attractive force given distance
        '''
        if d == 0:
            return 0
        
        # Attractive force: d^2 / k
        return (d * d) / self.l

    def step(self):
        '''
        This method gives one step of FruchtermanReingold's algorithm.
        '''
        if self.isFinished:
            return self.positions, True

        # Initial displacement
        disp = {node: {'dx': 0.0, 'dy': 0.0} for node in self.graph.nodes}
        maxForce = 0.0

        nodes = list(self.graph.nodes.keys())

        # REPULSIVE FORCES (pairwise)
        for i, uId in enumerate(nodes):
            for j in range(i + 1, len(nodes)):
                vId = nodes[j]

                # calculate the distance
                d = self.dist(uId, vId)
                # calculate repulsive force
                f = self.forceRep(d)

                # calculate the unit vector
                dx, dy = self.norm(vId, uId, max(d, 0.0001))

                # Updated displacements
                disp[uId]['dx'] += f * dx
                disp[uId]['dy'] += f * dy
                disp[vId]['dx'] -= f * dx
                disp[vId]['dy'] -= f * dy

        # ATTRACTIVE FORCES (edges)
        processedEdges = set()
        for uId, neighbors in self.graph.adjList.items():
            for vId in neighbors:
                pair = tuple(sorted((uId, vId)))
                if pair in processedEdges:
                    continue
                processedEdges.add(pair)

                # calculate the distance
                d = self.dist(uId, vId)
                # calculate attractive force
                f = self.forceAttr(d)
                # calculate the unit vector
                dx, dy = self.norm(uId, vId, max(d, 0.0001))

                # Updated displacements
                disp[uId]['dx'] += f * dx
                disp[uId]['dy'] += f * dy
                disp[vId]['dx'] -= f * dx
                disp[vId]['dy'] -= f * dy

        # APPLY FORCES WITH TEMPERATURE
        for nodeId in self.graph.nodes:
            dx = disp[nodeId]['dx']
            dy = disp[nodeId]['dy']
            # Magnitude of the displacement vector
            mag = math.hypot(dx, dy)

            if mag > 0:
                # This is the final distance the node will move.
                stepSize = min(mag, self.T)

                # Normalize the distance vector and. scale with magnitude
                dxN = dx / mag * stepSize
                dyN = dy / mag * stepSize

                self.positions[nodeId]["x"] += dxN
                self.positions[nodeId]["y"] += dyN

                maxForce = max(maxForce, math.hypot(dxN, dyN))

        # COOLING
        self.T *= self.T_decayRate
        self.currentIteration += 1

        # TERMINATION
        if self.currentIteration >= self.max_iter or maxForce < self.epsilon:
            self.isFinished = True

        return self.positions, self.isFinished