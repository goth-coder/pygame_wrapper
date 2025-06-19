# Pygame Wrapper

A simple wrapper around Pygame to make game development easier and more structured. This project provides utility classes and functions for building simulations, games, or interactive visualizations.

## Features

- UI components with hover animations (buttons, panels)
- Color manipulation utilities (e.g., linear color interpolation)
- Simplified event handling
- A reusable simulation/game framework

## Requirements

- Python 3.10 or higher
- Dependencies listed in `requirements.txt`

## Installation

You can install this project in multiple ways:

### Option 1: Using pip and requirements.txt

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

### Option 2: Using uv (Fast Python Package Installer)

```bash
# Clone the repository
git clone https://github.com/yourusername/pygame_wrapper.git
cd pygame_wrapper

# Create a virtual environment with a specific Python version (e.g., Python 3.13)
uv venv --python=python3.13 .venv

# Activate the virtual environment
# On Windows:
.\.venv\Scripts\ctivate
# On macOS/Linux:
source .venv/bin/activate

# Install dependencies
uv pip install -r requirements.txt
```

### Option 3: Install as Editable Package (Development Mode)

```bash
# Clone the repository
git clone https://github.com/yourusername/pygame_wrapper.git
cd pygame_wrapper

# Install in development mode
pip install -e .
```

## Running the Example Template

This repository includes a `template.py` file that demonstrates how to use the wrapper to create a simple simulation with buttons and event handling.

### To run the template:

```bash
python template.py
```

### Template Features

- **Pause/Resume button** to freeze or continue the simulation.
- **Restart button** to reset the simulation.
- Top UI panel with instructions (e.g., "Hold SPACE to launch!").
- Basic keyboard and mouse event handling.
- Placeholder for adding your own game logic.

### How to Customize

You can use `template.py` as a starting point for your own game or simulation.  
Key methods you may want to customize:

- `setup_simulation()`: Initialize game objects and static elements.
- `game_logic()`: Add your simulation/game logic here.
- `handle_events()`: Handle additional keyboard or mouse events.
- `_draw_static_objects()`: Draw background or static game elements.

---

## Development

To set up a development environment with linting (Ruff) and other dev tools:

```bash
# Install dev dependencies
pip install -e ".[dev]"
```

Or if using `uv`:

```bash
uv pip install --all-features
```

Then you can run Ruff manually:

```bash
ruff check .
```

## VS Code: Automatic Formatting with Ruff

This project includes a `.vscode/settings.json` file that configures VS Code to automatically format Python files and organize imports using [Ruff](https://docs.astral.sh/ruff/) every time you save a file. This ensures consistent code style and helps keep your imports tidy.

**No extra setup is needed if you use VS Code and have the [Ruff extension](https://marketplace.visualstudio.com/items?itemName=charliermarsh.ruff) installed.**

If you want to use a different editor, you can run Ruff manually:

```bash
ruff check .
```

---

## License

MIT License.
