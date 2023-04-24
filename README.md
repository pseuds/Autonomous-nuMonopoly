# Autonomous-nuMonopoly
Autonomous Monopoly Game written in Python. For when you're too lazy to play and just want to watch it print.

Some rules are different from the known monopoly game:
1. Houses can only be bought if the owner lands on its tile.
2. Properties can only be bought if it does not cost more than 50% of the player's wallet.
3. Jailed player gets out of jail by paying bail. If the player cannot afford bail for 3 turns, they lose the game and return their properties.
4. Player sells properties if they cannot afford rent/bail. Priorities: Houses < Cheapest Base Properties < Most Expensive Base Properties
5. Allows 2-40 players.
