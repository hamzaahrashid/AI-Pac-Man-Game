AI Pac-Man Game

A modern Pac-Man game built with Pygame, featuring AI-driven ghost movement using A* pathfinding, random maze generation, and data persistence. Players collect pellets, track scores, and progress through levels while evading a ghost.

Features





Random Maze Generation: Dynamically created mazes for varied gameplay.



A Pathfinding*: Ghost uses A* algorithm to chase Pac-Man intelligently.



Game States: Start, countdown, playing, paused, and game-over screens.



Score & Data Tracking: Saves player name, score, survival time, and level to an Excel file.



High Score Persistence: Stores and updates high scores in a text file.



User Input: Name entry and keyboard controls for Pac-Man movement.

Requirements





Python 3.x



Pygame (pip install pygame)



Pandas (pip install pandas)



Openpyxl (pip install openpyxl)

Installation





Clone the repository:

git clone https://github.com/your-username/ai-pacman-game.git



Navigate to the project directory:

cd ai-pacman-game



Install dependencies:

pip install pygame pandas openpyxl

How to Play





Run the game:

python pacman.py



Enter your name on the input screen.



Click "Start Game" to begin.



Use arrow keys to move Pac-Man, collect pellets, and avoid the ghost.



Press ESC to pause/resume.



Clear all pellets to advance levels; collision with the ghost ends the game.



Game data (name, score, survival time, level) is saved to game_data.xlsx.

Controls





Arrow Keys: Move Pac-Man (up, down, left, right).



ESC: Pause/resume game.



Enter: Submit name during input screen.



Mouse Click: Start or restart game.

Files





pacman.py: Main game script.



high_score.txt: Stores high score (created automatically).



game_data.xlsx: Stores game data (created automatically).

Notes





The ghost recalculates its path with a 10% chance per move for dynamic pursuit.



Mazes ensure valid paths between Pac-Man and the ghost.



Survival time and score are displayed during gameplay.
