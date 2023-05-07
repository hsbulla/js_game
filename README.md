# WebGame: "Run: The Coin Run" version 1.0
Welcome to the game "Run: The Coin Run"! In this game, the "runner runs" through a magical world, collecting coins and avoiding obstacles.

## How to play:
1. Start the game by entering your nickname and clicking the "Get to the game" button.
2. Нhe game will run automatically. Use the left and right keys to move around the screen and avoid obstacles.
3. Collect coins to get points.
4. If runner collides with an obstacle, the game will end.
5. The aim of the game is to get the maximum number of points.

## Controls:
* Use the "Left Arrow" key to move left.
* Use "Right Arrow" key to move to the right.
* Use "Enter/Return" key to restart the game.

## How to install and run the game:

For the first startup, execute the following commands in sequence:
1. cd backend-container
2. python3 -m venv venv
3. source venv/bin/activate (venv\Scripts\activate.bat)
4. pip install -r requirements.txt
5. cd game_project
6. python3 manage.py runserver

*To stop the server, use the key combination: ^C

For subsequent starts, execute the following commands:
1. cd backend-container
2. source venv/bin/activate (venv\Scripts\activate.bat)
3. cd game_project
4. python3 manage.py runserver

*To stop the server, use the key combination: ^C

## Technical Requirements:
The game was developed using JavaScript, Python, HTML and CSS. Your device and browser must support the following languages and frameworks: Babylon.js and Django.

## License:
This game is distributed under the terms of the MIT license. You may use and modify this code for any purpose, including commercial purposes, as long as you credit the source code. See the LICENSE file for more information.

## Game authors:
[@hsbulla](https://github.com/hsbulla) – Backend developer

[@bakugan](https://github.com/Bakugan74) – Frontend developer

[@anastasia](https://github.com/Anastasia-Led) – Frontend developer
