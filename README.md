# bot-battle-board
## What is it?
Bot-Battle-Board (name tentative) is a programming game, where two or more players compete to see whose bots can beat the others'. The players do not manuall control these bots. Instead, they write a set of instructions for them using a simple programming language, and these bots simply perform the instructions given to them.
## How do you play?
The rules are very simple. Each player starts with 1 bot, randomly placed somewhere on the board (default board size is 20 by 20 tiles, but may be changed as desired). Each bot begins with 3 points of health (hp). The bots take turns performing the instructions given to them by the players. The game ends either when only one player has any remaining bots, or when the turn limit has passed (default is 10,000 turns, but this is also configurable). If the turn limit is reached, the player with the most active bots wins.

There are two important things to know. The first is that the edges of the board wrap around. A bot on the leftmost side of the board taking a step to the left will emerge on the right side of the board. A unit on the top-left corner of the board may attack a unit on the bottom-right, since it is considered adjacent to it (since it is only one diagonal move away).

The second important thing is that you do not have full control of your bots. Most commands contain some element of randomness. The move() command will move the bot to a **random** adjacent tile (if there is at least one free such tile). The attack() command will attack one random adjacent enemy (if there is more than one), etc. It is advised to think of your bots as an erratic swarm of living cells, and write a strategy that leverages this.

You can start a game by running the game.py file. You will then be prompted to select text files to read, once per player. These must contain the instructions for the player's bots. The game will then begin, and a turn-by-turn record of the battle (and its conclusion) will be displayed.
## How do I tell the bots what to do?
You must write the instructions yourself in a text file. The syntax of the language is very simple. To execute a command, simply type it, followed by parentheses with the arguments for the function. Multiple whitespaces and linebreaks are ignored. The only valid input is either commands, numbers, or symbols which you define yourself (see the "define" command in the next section). For example, the following is a valid command:
> attack()

This will make the bot perform an attack against one random adjacent enemy, if one exists. No arguments are needed.
> add(3, 2) 

Is also a valid command, which returns the value of 3 + 2. This can be used as an argument for other functions.
> attack

Is not a valid command, because the command must end with parentheses.
> add(5, 1, 8) 

Is **also not a valid command**, because the add function expects exactly two arguments.

Commands are split into two categories: critical and non-critical commands. Critical commands, such as attack(), may only be performed once per turn. Once they are performed, the bot may not take any further critical action until the next turn. Non-critical actions may be used as many times as desired. Examples of such commands are the aforementioned add(a, b) which simply returns the value of a + b, and also distance_from_closest_enemy(), which returns the distance between the unit and its closest enemy.
An example strategy would be:
```
define(x, distance_from_closest_enemy())
if(eq(x, 1), attack())
if(gt(x, 3), spawn())
move()
```
This simple strategy first defines a new variable called x, and determines its value to be the distance from the closest enemy. It then checks if x = 1 (i.e. we are adjacent to an enemy). If true, then it attacks. If x > 3, meaning the closest enemy is more than three tiles away, then spawn a new unit (the spawn command disables the bot for three turns, after which a new bot is spawned next to it). Finally, if x is not 1, but also not larger than 3 (i.e. if x is 2 or 3), then move to a random adjacent tile.
Note that even though the move() command is not inside an 'if' statement, it will only be performed if the previous two conditions are not met. This is because attack(), spawn() and move() are all critical commands, and so if for example x = 1 and the unit attacks, it will not be able to move in the same turn.
## What commands are available for my bots?
Following is a list of commands available to the player:
### Critical commands
> attack()

This command attacks a random adjacent enemy (if one exists) for 1 point of damage.

> move()

The bot moves to one random free adjacent tile (if one exists; note that bots may move diagonally).

> spawn()

Forfeit the current turn and the next two turns. In the beginning of the first turn after that, a new unit (with 3 hp) is spawned in an adjacent free tile (if one exists). The new unit is placed at the end of the turn queue, meaning it will only have its first turn after one more round has passed.

>