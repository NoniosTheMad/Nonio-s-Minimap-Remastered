# as a player, every tick: purse total in hundredths (#pt = coins x 100 + nx.pfrac) vs the last tick (nx.ptot).
# A rise adds to nx.pgain and restarts the popup (nx.ptime 30 -> 1: purse/show draws "+gain" fading out;
# 0 = one last draw without it, then -1 = off). Drops (deposit, death, placing) show nothing.
scoreboard players add @s nx.pfrac 0
scoreboard players operation #pt nx.purse = @s nx.coins
scoreboard players operation #pt nx.purse *= #100 nx.purse
scoreboard players operation #pt nx.purse += @s nx.pfrac
execute unless score @s nx.ptot = @s nx.ptot run scoreboard players operation @s nx.ptot = #pt nx.purse
execute if score @s nx.ptime matches 0.. run scoreboard players remove @s nx.ptime 1
execute unless score @s nx.ptime matches 1.. run scoreboard players set @s nx.pgain 0
execute if score #pt nx.purse > @s nx.ptot run function nonios:purse/gain_add
scoreboard players operation @s nx.ptot = #pt nx.purse
