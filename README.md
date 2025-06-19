# Pygame Wrapper

A simple wrapper for Pygame to make game development easier. This project provides utility functions and classes to simplify common Pygame operations.

## Features

- UI components with animations (buttons, panels)
- Color manipulation utilities
- Event handling simplification
- Simulation framework

## Requirements

- Python 3.10 or higher
- Dependencies as listed in `requirements.txt`

## Installation

There are multiple ways to install this project:

### Option 1: Using pip with requirements.txt

```bash
# Clone the repository
git clone https://github.com/yourusername/pygame_wrapper.git
cd pygame_wrapper

# Create a virtual environment
python -m venv .venv

# Activate the virtual environment
# On Windows:
.\.venv\Scripts\activate
# On macOS/Linux:
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Option 2: Using uv (Faster Python Package Installer)

```bash
# Clone the repository
git clone https://github.com/yourusername/pygame_wrapper.git
cd pygame_wrapper

# Create a virtual environment with Python 3.13
uv venv --python=python3.13 .venv

# Activate the virtual environment
# On Windows:
.\.venv\Scripts\activate
# On macOS/Linux:
source .venv/bin/activate

# Install dependencies
uv pip install -r requirements.txt
```

### Option 3: Installation as a Package

```bash
# Clone the repository
git clone https://github.com/yourusername/pygame_wrapper.git
cd pygame_wrapper

# Install the package in development mode
pip install -e .
```

## Usage

Import the components you need from the package:

```python
from pygame_wrapper import UIButton, Simulation

# Create a simulation
sim = Simulation(width=800, height=600)
sim.run()
```

### Creating a Basic Game

You can use the template.py as a starting point:

```python
import pygame
from pygame_wrapper import Simulation, UIButton

def main():
    # Initialize your game
    game = Simulation(width=800, height=600)
    
    # Add game elements
    # ...
    
    # Run the game loop
    game.run()

if __name__ == "__main__":
    main()
```

## Development

To set up the development environment:

```bash
# Install development dependencies
pip install -e ".[dev]"
