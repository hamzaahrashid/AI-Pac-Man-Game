##**🎮 AI Pac-Man Game 🟡👻**

Welcome to AI Pac-Man Game, a thrilling modern twist on the classic Pac-Man! Built with Pygame, this game features a clever ghost powered by A* pathfinding, dynamic mazes, and score tracking saved to Excel. Gobble up pellets, dodge the ghost, and climb the levels! 🚀

**✨ Features**

**🗺️ Random Maze Generation:** Every game brings a fresh, unpredictable maze!

**🧠 A star (algorithm) Pathfinding:** The ghost uses the A* algorithm to hunt Pac-Man with smarts.

**🎲 Game States:** Enjoy start, countdown, playing, paused, and game-over screens.

**📊 Score & Data Tracking:** Save your name, score, survival time, and level to game_data.xlsx.

**🏆 High Score Persistence:** High scores are stored in high_score.txt for glory!

**⌨️ User Input:** Enter your name and control Pac-Man with smooth keyboard inputs.

**🛠️ Requirements**

🐍 Python 3.x
🎮 Pygame (pip install pygame)
📈 Pandas (pip install pandas)
📑 Openpyxl (pip install openpyxl)

**🚀 Installation**

**Clone the repository:**

git clone https://github.com/hamzaahrashid/AI-Pac-Man-Game.git

**Navigate to the project directory:**

https://github.com/hamzaahrashid/AI-Pac-Man-Game in your browser

**Install dependencies:**

pip install pygame pandas openpyxl

**🎉 How to Play**

**Run the game:**
python pacman.py
Type your name on the input screen. ✍️
Click Start Game to dive in! 🟢
Use arrow keys to guide Pac-Man, munch pellets, and evade the ghost. 🟡👻
Press ESC to pause or resume. ⏸️
Clear all pellets to level up; hit the ghost, and it’s game over! 😱
Your stats (name, score, survival time, level) are saved to game_data.xlsx. 📂

**🕹️ Controls**
Arrow Keys: Move Pac-Man (up ⬆️, down ⬇️, left ⬅️, right ➡️).
ESC: Pause/resume the game. ⏯️
Enter: Submit your name on the input screen. ✅
Mouse Click: Start or restart the game. 🖱️

**📂 Files**
pacman.py: The main game script. 🐍
high_score.txt: Stores your high score (auto-generated). 🏅
game_data.xlsx: Logs game data (auto-generated). 📊

**💡 Notes**

The ghost recalculates its path with a 10% chance per move for sneaky surprises! 😈
Mazes are designed to always have a path between Pac-Man and the ghost. 🛤️
Keep an eye on your survival time and score during gameplay! ⏱️
