# Ludo-for-CodeNationGameJam
The Ludo board game as a 45h hackathon for CodeNation

Code can be improved obviously but it seems to be working and as the time for the jam ran out, I will not allow myself to improve the project anymore. Perhaps on another repo.

Known bugs (or "features") : 
- When you roll a 6 you sometimes have only 1 pawn you can move and the game will ask you to pick which one you can move (but you will only be able to move 1)
- When you roll a 6, have pawns on the board but they can't move and still have pawn(s) on the yard. If you have a pawn on your starting position, the game will ask you to swap it with one of your yard.
- When a player has finished (all 4 pawns in the centre) and the game is still running for the others, the 'finished' player is still asked to roll the die for no reason

The rules applied : https://en.wikipedia.org/wiki/Ludo_(board_game)

The only way to change the number of players is by hardcoding it, on line 68 of Game.py you have:
        self.players = [Player("green"), Player("yellow"), Player("blue"), Player("red")]
you can change that to for example : 
        self.players = [Player("yellow"), Player("red")]
And you will play as Yellow and Red
