Must already install in your computer (and maybe more | see full constraint in documentation)
- Windows OS (Windows version depend on python version of User)
- Python 3.9++ and pygame (python library)

# [HOW TO PLAY] [IN DETAIL] (Multiplayer game and Local network only):
1. - One user must run file "server.py", it will generate "server_config.ini" file (for further customization).
   - In "server_config.ini", it will contain current machine's local IPv4 address and default port 5555.
   - If user want to change IPv4 of server to use virtual local network (Hamachi, Radmin), User can change
     Server's IPv4 in "server_config.ini" file then restart the server.
   - If "server_config.ini" file damaged, User can simply delete current "server_config.ini" and run "server.py"
     it will generate "server_config.ini" anew.
   - We recommended not to change the port number if not necessary.

2. - Any user can run game by run "main.py"** as a Player.
   - Number of players should be at least 5 players and can only have a maximum of 10 players.

3. - One of player need to 'host' the game by click 'host' button in main menu
     then put IPv4 and Port of the server in.
   - Player who 'host' the game doesn't need to be the same as player who run the server.
   - Host player can customize your match setting and more (already stated in game).
   - Other players can 'join' game after one player already 'host' via 'join' button
     then put IPv4 and Port of the server in.
   - Every player create their Avata and join the game!

4. - Each player wait for everyone to join the game (Number of player depend on match setting).
   - When all player in in the room. Host can start the game!

5. - Enjoy!

P.S. KnightVille is the Avalon-like game the tutorial is already in "How to play" button within game.

Summary of steps
1. Run "server.py"
2. Run "main.py"
3. Host
4. Join
5. Play !!!

[Suggession] You can create your own game mode to increase difficulty.
For example: 
- Every user use the same name / same skin.
- Every user use name same as role name (but actually your name is not the same as your role).
So, Be creative!

Have Fun!!!

Create by Computer Engineering Student:
- Nithi Piyaphonnarinthon	62070503430
- Romtam Tanpituckpong		62070503444
- Wagee Jr. Nanta Aree 		62070503445
- Chatchapon Sukitporn-udom 	62070503455
- Kantawit Chatdamrongmongkol 	62070503457
