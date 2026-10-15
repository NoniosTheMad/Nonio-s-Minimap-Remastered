# as a player, every tick: the "+N" popup (#107, #114). Purse total in hundredths (#pt = coins x 100 + nx.pfrac) vs the
# last tick (nx.ptot); a rise adds to nx.pgain. Drops (deposit, death, placing) show nothing.
# Gains below the coin step (purse/step) wait unseen (they are in the purse and the blue decimals already); once the
# sum reaches a step the popup opens: 1.5 s + 0.5 s per step in it, at most 4 s, counted from its opening, so a steady
# trickle (talisman) groups into separate popups. Waiting gains are forgotten after 5 s.
# nx.ptime: 1.. = popup open (ticks left), 0 = one last draw without it, -1 = off. nx.page = ticks since open / waiting.
scoreboard players add @s nx.pfrac 0
scoreboard players add @s nx.pgain 0
scoreboard players add @s nx.page 0
scoreboard players operation #pt nx.purse = @s nx.coins
scoreboard players operation #pt nx.purse *= #100 nx.purse
scoreboard players operation #pt nx.purse += @s nx.pfrac
execute unless score @s nx.ptot = @s nx.ptot run scoreboard players operation @s nx.ptot = #pt nx.purse
execute if score #pt nx.purse > @s nx.ptot run function nonios:purse/gain_add
scoreboard players operation @s nx.ptot = #pt nx.purse
function nonios:purse/step
scoreboard players operation #psh nx.purse = #pst nx.purse
scoreboard players operation #psh nx.purse *= #100 nx.purse
execute if score @s nx.ptime matches 1.. run return run function nonios:purse/gain_tick
execute if score @s nx.ptime matches 0 run scoreboard players set @s nx.ptime -1
execute if score @s nx.pgain matches ..0 run return 0
scoreboard players add @s nx.page 1
execute if score @s nx.pgain >= #psh nx.purse run return run function nonios:purse/gain_open
execute if score @s nx.page matches 100.. run function nonios:purse/gain_end
