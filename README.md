Pyforest
=======

A small 2D game/demo built with Pygame demonstrating:

- A* pathfinding AI for non-player mobs
- Tiled (.tmx) maps and collision handling (pytmx, pyscroll)
- 2D sprite animation system with movement / idle animations
- Simple game loop and entity system

Project structure
-----------------

- `main.py` — game entrypoint
- `src/graphique/` — rendering and animation systems
  - `animation.py` — AnimateSprite base class and animation loaders
  - `game.py` — main Game class and loop
- `src/sprite/` — in-game entities
  - `mob.py` — Mob entity (AI-driven)
  - `player.py` — Player entity and input handling
- `src/strategie/` — AI and pathfinding
  - `ia.py` — A* implementation and pursuit logic
- `src/modele/` — assets, tilemaps and spritesheets (not mine)
- Other supporting modules: `src/` packages, helpers, etc.

Dependencies
------------

The project uses the following Python packages:

- pygame
- pytmx
- pyscroll

Install them with pip (prefer a virtualenv):

```bash
pip install pygame pytmx pyscroll
```

How it works (high level)
-------------------------

- The `IA` class in `src/strategie/ia.py` runs an A* search on a grid derived from the Tiled map. The A* implementation returns a list of grid positions (path).
- Mobs use `move_along_path` to set their velocity toward the next node. The `Mob` class reads that `velocity` and the animation system displays the correct sprite frames for movement/idle.
- `src/graphique/animation.py` implements an `AnimateSprite` base class that loads spritesheets and selects frames for left/right and idle animations. The animation system takes the mob's last significant movement direction to avoid flip-flopping.

Running the game
----------------

Start the game with:

```bash
python main.py
```

