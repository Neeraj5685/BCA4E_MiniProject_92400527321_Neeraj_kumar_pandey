Name -: Neeraj Kumar Pandey
Enrollment no. -: 92400527321
Stream -: BCA

FLAPPY BIRD GAME USING PYTHON (PYGAME)

DESCRIPTION:
This project is a clone of the classic Flappy Bird game developed using Python and the Pygame library. The player controls a bird and tries to fly through gaps between pipes without colliding.

GAME OBJECTIVE:
The goal of the game is to score maximum points by successfully passing the bird through the pipes. Each pipe crossed increases the score.

GAME LOGIC:
The core logic of the game is based on the following concepts:

1. GAME LOOP:
   The game runs inside a continuous loop that updates the screen, handles user input, and checks game conditions.

2. GRAVITY SYSTEM:
   The bird automatically falls down due to gravity. This is implemented by increasing the bird's downward velocity over time.

3. JUMP MECHANISM:
   When the player presses a key (spacebar/up arrow), an upward force is applied to the bird, making it jump.

4. PIPE GENERATION:
   Pipes are generated at regular intervals with random gaps. These pipes move from right to left to create the illusion of motion.

5. COLLISION DETECTION:
   The game checks if the bird touches the pipes or the ground. If a collision occurs, the game ends.

6. SCORING SYSTEM:
   Each time the bird successfully passes a pipe, the score increases.

7. GAME OVER CONDITION:
   The game stops when the bird hits a pipe or falls to the ground.

FEATURES:

* Smooth gameplay using frame updates
* Real-time score display
* Random pipe generation
* Simple graphics and sound effects

TECHNOLOGIES USED:

* Python
* Pygame

IMPORTANT NOTE:
This project may not work properly with the latest version of Pygame. Some functions used in this code are compatible with older versions only.

If you face issues while running the game, install an older version:
pip install pygame==2.1.0

HOW TO RUN:

1. Install Python (version 3.x)
2. Install Pygame (recommended older version)
3. Open the project in VS Code
4. Run the main file (main.py)
5. Press SPACE or UP ARROW to control the bird

FOLDER STRUCTURE (Example):

* game.py
* bird.py
* pipe.py
* assets/

  * images
  * sounds

CONCLUSION:
This project helps beginners understand basic game development concepts such as game loops, physics (gravity), collision detection, and object movement using Python.


