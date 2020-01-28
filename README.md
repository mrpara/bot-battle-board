# bot-battle-board
## What is it?
Bot-Battle-Board (name tentative) is a programming game, where two or more players compete to see whose bots can beat the others'. The players do not manuall control these bots. Instead, they write a set of instructions for them using a simple programming language, and these bots simply perform the instructions given to them.
## How do you play?
The rules are very simple. Each player starts with 1 bot, randomly placed somewhere on the board (default board size is 20 by 20 tiles, but may be changed as desired). The bots take turns performing the instructions given to them by the players. The game ends either when only one player has any remaining bots, or when the turn limit has passed (default is 10,000 turns, but this is also configurable).
Start by running the game.py file. The game will then prompt you to select text files to read, one per player. These must contain the instructions for the player's bots. The game will then begin, and a turn-by-turn record of the battle (and its conclusion) will be displayed.
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
list commands