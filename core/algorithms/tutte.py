#########################################################
#   Written by  :   Hassan Ayoub                        #
#   Date        :   December 8, 2025                    #
#   Purpose     :   Implementing Tutte Drawing          #
#########################################################

# imports
import math
import networkx as nx 
from core.algorithms.algorithmInterface import Algorithm

# Tutte class
class Tutte(Algorithm):
    '''
    Implementation of the Tutte's Barycentric Embedding Algorithm.

    Each call to `step()` performs a single iteration, calculating the total 
    barycentric displacement and updating positions.

    Attributes:
        graph (object):
            The graph instance containing nodes and adjacency information.

        radius (float):
            Radius used to place the initial fixed boundary nodes. This defines 
            the final size of the drawing.

        dampingRate (float):
            Multiplicative step-size factor applied to the total displacement 
            vector. Must be in range (0, 1) to ensure **stability** and 
            **convergence**.

        maxIter (int):
            Maximum number of iterations before the algorithm terminates.

        epsilon (float):
            Threshold for maximum node displacement. If the displacement of 
            all nodes falls below this value, the algorithm terminates early.

        positions (dict[int, dict[str, float]]):
            Mutable dictionary storing node positions.
            Format: { nodeId: {"x": float, "y": float} }

        fixedNodes (set):
            Set of node IDs that form the fixed outer boundary, preventing them 
            from moving during iterations.

        currentIteration (int):
            Number of iterations performed so far.

        isFinished (bool):
            True if the algorithm has converged or reached the maximum iterations.
    '''
    # contructor
    def __init__(self, graph, radius, dampingRate=0.7, maxIter=3000, epsilon=0.01):
        super().__init__()
        self.graph = graph
        self.maxIter = maxIter
        self.epsilon = epsilon
        self.dampingRate = dampingRate
        self.radius = radius
        
        self.positions = {node: {'x': data['x'], 'y': data['y']} for node, data in graph.nodes.items()}
        self.fixedNodes = self._chooseFixedNode()
        
        self.currentIteration = 0
        self.isFinished = False

    def reset(self):
        '''
        Reset positions and iteration count
        '''
        self.positions = {node: {'x': data['x'], 'y': data['y']} for node, data in self.graph.nodes.items()}
        self.currentIteration = 0
        self.isFinished = False

    def dist(self, uId, vId):
        ''' 
        Calculates the Euclidean Distance between two nodes. 
        '''
        u = self.positions[uId]
        v = self.positions[vId]
        return math.hypot(v['x'] - u['x'], v['y'] - u['y'])

    def norm(self, uId, vId, d):
        ''' 
        Returns unit vector from uId to vId. 
        '''
        if d == 0:
            return 0.0, 0.0
        
        # Vector points FROM uId TO vId
        dx = (self.positions[vId]['x'] - self.positions[uId]['x']) / d
        dy = (self.positions[vId]['y'] - self.positions[uId]['y']) / d
        return dx, dy

    def forceAttr(self, uId, d, uDeg):
        '''
        Calculates the attractive force magnitude F = d / deg(u) for the edge (u, v).
        This force leads to the barycentric displacement.
        '''
        if uId in self.fixedNodes:
             return 0.0
        
        if uDeg == 0:
            return 0.0
        
        # Magnitude M = ||P_v - P_u|| / deg(u) = d / deg(u)
        return d / uDeg

    def _chooseFixedNode(self):
        '''
        Selects fixed nodes and sets their initial positions on a circle.
        ''' 
        G_nx = nx.Graph()
        G_nx.add_nodes_from(self.graph.nodes)

        for u, neighbors in self.graph.adjList.items():
            for v in neighbors:
                G_nx.add_edge(u, v)

        totalNodes = len(G_nx.nodes)
        fixedList = []
        
        try:
            # Check for planarity
            isPlanar, embedding = nx.check_planarity(G_nx)
            
            if isPlanar and len(G_nx.edges) > 0:
                try:
                    # Find a list of cycles (this is not guaranteed to be the faces)
                    cycles = list(nx.cycle_basis(G_nx))
                    
                    if cycles:
                        # Find the longest cycle 
                        fixedList = max(cycles, key=len)
                    else:
                        # Fallback for small graphs where cycles might be short
                        pass
                        
                except nx.NetworkXNoCycle:
                    # No cycle found, use fallback
                    pass
            
            if not fixedList:
                # Fallback logic for non-planar or small graphs
                numNodesToFix = max(5, int(math.sqrt(totalNodes)))
                degrees = dict(G_nx.degree())
                fixedList = sorted(G_nx.nodes, key=lambda n: degrees.get(n, 0), reverse=True)[:numNodesToFix]
                
        except nx.NetworkXException:
            # General fallback for exceptions during graph analysis
            numNodesToFix = max(5, int(math.sqrt(totalNodes)))
            degrees = dict(G_nx.degree())
            fixedList = sorted(G_nx.nodes, key=lambda n: degrees.get(n, 0), reverse=True)[:numNodesToFix]
        
        # Ensure minimum nodes are fixed
        n = len(fixedList)
        if n < 2 and totalNodes > 0:
            fixedList = list(self.graph.nodes)[:2] # Ensure at least 2 nodes are fixed
            n = len(fixedList)
        
        # Center the initial layout
        centerX, centerY = 300.0, 300.0
        n = len(fixedList)
        # Place the fixed nodes in a circle
        for i, node in enumerate(fixedList):
            node_id = str(node) if isinstance(node, int) else node
            angle = 2 * math.pi * i / n
            self.positions[node_id]['x'] = centerX + self.radius * math.cos(angle)
            self.positions[node_id]['y'] = centerY + self.radius * math.sin(angle)
            
        return set(fixedList)
    
    def step(self):
        '''
        Perform one iteration of the Tutte method.
        '''
        if self.isFinished:
            return self.positions, True

        disp = {node: {'dx': 0.0, 'dy': 0.0} for node in self.graph.nodes}
        maxTotalDisplacement = 0.0
        nodes = list(self.graph.nodes.keys())

        # ATTRACTIVE FORCES
        for uId, neighbors in self.graph.adjList.items():
            uDeg = len(neighbors)
            if uId in self.fixedNodes:
                continue
                
            for vId in neighbors:
                d = self.dist(uId, vId)
                
                # Magnitude M = d / deg(u)
                f = self.forceAttr(uId, d, uDeg)

                # Unit vector FROM uId TO vId 
                dxNorm, dyNorm = self.norm(uId, vId, max(d, 0.0001))

                # Accumulate the attractive force vector: F_u += M * unit_vector
                disp[uId]['dx'] += f * dxNorm
                disp[uId]['dy'] += f * dyNorm

        # APPLY DISPLACEMENTS 
        for nodeId in nodes:
            if nodeId in self.fixedNodes:
                continue

            dxTotal = disp[nodeId]['dx']
            dyTotal = disp[nodeId]['dy']
            magTotal = math.hypot(dxTotal, dyTotal)

            if magTotal > 0:
                # DAMPING: P_new = P_old + Damping * (D_total / ||D_total||) * ||D_total||
                stepSize = self.dampingRate * magTotal
                
                dxN = dxTotal / magTotal * stepSize
                dyN = dyTotal / magTotal * stepSize

                self.positions[nodeId]["x"] += dxN
                self.positions[nodeId]["y"] += dyN
                
                maxTotalDisplacement = max(maxTotalDisplacement, math.hypot(dxN, dyN))

        self.currentIteration += 1

        # Termination check
        if maxTotalDisplacement < self.epsilon or self.currentIteration >= self.maxIter:
            self.isFinished = True
            
        return self.positions, self.isFinished