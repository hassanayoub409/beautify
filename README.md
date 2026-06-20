# Beautify

A Python desktop application for visualizing and animating graph drawing algorithms in real time — built with PyQt5 and NetworkX.

![Language](https://img.shields.io/badge/Language-Python%203.11-blue)
![Framework](https://img.shields.io/badge/Framework-PyQt5-green)
![Platform](https://img.shields.io/badge/Platform-macOS%20%7C%20Windows%20%7C%20Linux-lightgrey)

---

## Overview

Beautify lets you select from a set of well-known graphs and watch three classic graph drawing algorithms animate the layout step by step. You can also input your own graph using an adjacency list or edge pair format and apply any of the algorithms to it.

The goal of the project is to make graph drawing algorithms intuitive and visual — seeing how Eades, Fruchterman-Reingold, and Tutte each approach the same graph makes their differences immediately clear.

---

## Features

- **5 built-in graphs** — Desargues, Karate Club, Icosahedral, Dodecahedral, Florentine Families
- **Custom graph input** — Enter your own graph via Adjacency List or Edge Pair format
- **3 algorithms** — Eades Spring Embedder, Fruchterman-Reingold, Tutte's Barycentric Embedding
- **Step-by-step animation** — Watch the layout evolve in real time
- **Clean UI** — Animated welcome screen, card-based graph selection, interactive canvas

---

## Screenshots

**Landing Screen**
![Landing Screen](https://github.com/hassanayoub409/beautify/blob/a70c3b3e4acc4635f834937350abc32eeafbd4e6/landing_screen.png)


**Graph Selection Screen**
![Selection Screen](https://github.com/hassanayoub409/beautify/blob/a70c3b3e4acc4635f834937350abc32eeafbd4e6/selection_screen.png)


**Dodecahedral Graph (Before Animation)**
![Dodecahedral Graph](https://github.com/hassanayoub409/beautify/blob/a70c3b3e4acc4635f834937350abc32eeafbd4e6/dodecahedral.png)


**Dodecahedral Graph (After Fruchterman-Reingold Algorithm)**
![Fruchterman-Reingold Algorithm](https://github.com/hassanayoub409/beautify/blob/a70c3b3e4acc4635f834937350abc32eeafbd4e6/fruchterman_reingold.png)

---

## Algorithms

### Eades Spring Embedder
Models the graph as a physical system where edges act as springs and nodes repel each other. Attractive forces pull connected nodes together using a logarithmic spring model, while repulsive forces push all node pairs apart. A temperature parameter controls the maximum displacement per iteration and cools over time.

### Fruchterman-Reingold
A refinement of the force-directed approach where attractive forces scale as `d² / k` and repulsive forces scale as `k² / d`, where `k` is the ideal edge length derived from the canvas area. Temperature-based cooling ensures convergence.

### Tutte's Barycentric Embedding
A combinatorial algorithm that fixes a set of boundary nodes on a circle and iteratively moves each interior node to the average (barycentre) of its neighbours. Guaranteed to produce a straight-line planar embedding for 3-connected planar graphs.

---

## Input Format

If you choose **"Input Your Graph"**, you can enter your own graph in one of two formats:

### Adjacency List
The first line is the number of nodes. Each subsequent line is a node followed by its neighbours in brackets:
```
20
0: [3, 5, 8, 11]
1: [0, 4, 6, 9]
2: [1, 3, 7, 10]
...
```

### Edge Pair
The first line is the number of nodes. Each subsequent line is an edge as a pair of node IDs separated by a comma or space:
```
12
0,3
0 7
1 2
...
```

Sample input files are included in the repo root — `testAdjList.txt` and `testEdgePair.txt` — to help you get started quickly.

---

## Project Structure

```
Beautify/
├── main.py                          # Entry point, manages screen transitions
├── requirements.txt                 # Python dependencies
├── testAdjList.txt                  # Sample adjacency list input
├── testEdgePair.txt                 # Sample edge pair input
│
├── core/
│   ├── graphModel.py                # Graph data structure + built-in graph generators
│   ├── graphController.py           # Routes graph selection to the correct generator
│   └── algorithms/
│       ├── algorithmInterface.py    # Abstract base class for all algorithms
│       ├── eades.py                 # Eades Spring Embedder
│       ├── fruchtermanReingold.py   # Fruchterman-Reingold algorithm
│       └── tutte.py                 # Tutte's Barycentric Embedding
│
├── ui/
│   ├── styles.py                    # Global constants and style definitions
│   ├── welcomeScreen.py             # Animated intro screen
│   ├── graphSelectionScreen.py      # Card-based graph picker
│   ├── graphInputScreen.py          # Custom graph input dialog
│   ├── graphCanvas.py               # Canvas that renders and animates the graph
│   ├── visualizationScreen.py       # Main visualization interface
│   └── components.py                # Reusable UI components
│
└── assets/
    ├── fonts/                       # Application fonts
    └── images/                      # Algorithm preview images
```

---

## Prerequisites

- Python 3.8 or higher
- pip

---

## Installation & Running

### 1. Clone the repository
```bash
git clone https://github.com/YOUR_USERNAME/Beautify.git
cd Beautify
```

### 2. (Recommended) Create a virtual environment
```bash
python -m venv venv

# macOS / Linux
source venv/bin/activate

# Windows
venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the application
```bash
python main.py
```

---

## Dependencies

| Package | Purpose |
|---------|---------|
| `PyQt5` | GUI framework — windows, widgets, canvas, animations |
| `networkx` | Built-in graph generators and planarity checking (used by Tutte) |

---

## Author

**Hassan Ayoub** — November 2025

---

## License

![License](https://img.shields.io/badge/License-MIT-yellow). This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

**This project was developed as a part of Analysis of Alogirithms course requirement at Punjab University College of Information Technology.**
