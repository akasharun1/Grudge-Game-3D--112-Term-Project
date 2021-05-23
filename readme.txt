
Description: 

This is my term project for 15112 taken at CMU. It is a 3D ray-casted Horror game I call 112 Grudge Game 3D.
Important components of my project include raycasting, implementation of A* pathfinding for the grudge AI, 
implementation of Prim's algorithm for maze construction modified to create a dungeon system by sparsifying it
and generating rooms in it, adjustable game difficulty and a leaderboard, that displays the values of only 
the top 5 scorers, in which each username is unique without any copies (Using SQL Queries and Databases).




Setup Instructions:

To play the game open main_v3.py and run it in your preffered text-editor and place the files in this folder in the 
same location as it. Leave the games window size as it is and don't modify it.

Please download Hannya.wav before running the game. Hannya.wav is a 40MB wav file which was provided to my TA mentor seperately.

Certain modules need to be installed before running the game, these modules include pygame and mysql.connector.

Pygame can be installed using the instructions given on this website: https://www.pygame.org/wiki/GettingStarted or by running
the 'python3 -m pip install -U pygame --user' command in your terminal/ command prompt.

Without MySQL and mysql.connector the database aspect of the game won't work:

Hence to install MySql go to https://dev.mysql.com/downloads/mysql/ and download MySQL from the website. 
Follow the set up and installation process detailed by the installer.

In greater detail run the installer and if MySQL Server doesn't show up in it click the Add button.
Once in the addition menu click MySQL Servers under available products >> MySQL Server >> and click the latest available version

Then press the -> arrow key symbol to transfer it to the Products to be installed side. Once its there click next at the bottom 
and follow all the necessary prompts to setup your server.

After the download and installation of your server is complete. Go back to the installer home menu and click reconfigure/ configure:
The click next and follow the prompts of the configuration menu:

IMP set the server user to root (usually preset) and password to password.

Your MySql set up is now complete!

To install mysql.connector on the other hand run the "pip install mysql-connector-python" command in your terminal/ command prompt.





Game Commands, Shortcuts and Instructions:

You can use the WASD keys to move and change player orientation.

Press the 'p' key to pause the game.

Press the 'h' key to get help on the games mechanics and rules

Press the 'o' key to skip to the You escaped mode of the game.




Thats all, enjoy my game!











