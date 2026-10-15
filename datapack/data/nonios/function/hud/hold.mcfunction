# as a player who just got an important actionbar message (Barrier): the coin display pauses ~2 s so it isn't overwritten
execute store result score @s nx.ab_hold run time query gametime
scoreboard players add @s nx.ab_hold 40
