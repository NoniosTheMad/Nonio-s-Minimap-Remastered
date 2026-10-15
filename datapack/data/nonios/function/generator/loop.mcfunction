# Every second: advance the regrow timers of empty generators.
schedule function nonios:generator/loop 20t replace
# in the match, generators only run during prep and battle (demo worlds without the match map: always)
execute if score #map nx.state matches 1 unless score #state nx.state matches 1..2 run return 0
scoreboard players operation #step nx.gen = #speed nx.gen
scoreboard players operation #step nx.gen *= #20 nx.gen
# regrowth speeds up with team size: x (1 + (players - 1) / #per_roll)  (20 players, 4 per step -> x5)
execute store result score #n_white nx.gen if entity @a[team=white]
execute store result score #n_black nx.gen if entity @a[team=black]
execute if score #sim nx.gen matches 1.. run scoreboard players operation #n_white nx.gen = #sim nx.gen
execute if score #sim nx.gen matches 1.. run scoreboard players operation #n_black nx.gen = #sim nx.gen
scoreboard players operation #r_white nx.gen = #n_white nx.gen
scoreboard players operation #r_black nx.gen = #n_black nx.gen
scoreboard players remove #r_white nx.gen 1
scoreboard players remove #r_black nx.gen 1
scoreboard players operation #r_white nx.gen /= #per_roll nx.gen
scoreboard players operation #r_black nx.gen /= #per_roll nx.gen
scoreboard players add #r_white nx.gen 1
scoreboard players add #r_black nx.gen 1
execute if score #r_white nx.gen matches ..0 run scoreboard players set #r_white nx.gen 1
execute if score #r_black nx.gen matches ..0 run scoreboard players set #r_black nx.gen 1
scoreboard players operation #st_white nx.gen = #step nx.gen
scoreboard players operation #st_white nx.gen *= #r_white nx.gen
scoreboard players operation #st_black nx.gen = #step nx.gen
scoreboard players operation #st_black nx.gen *= #r_black nx.gen
# capture node bonus "regrow" (arena/node/bonus): x1.5 while the team holds one
execute if score #regrow_white nx.arena matches 1.. run scoreboard players operation #st_white nx.gen *= #3 nx.gen
execute if score #regrow_white nx.arena matches 1.. run scoreboard players operation #st_white nx.gen /= #2 nx.gen
execute if score #regrow_black nx.arena matches 1.. run scoreboard players operation #st_black nx.gen *= #3 nx.gen
execute if score #regrow_black nx.arena matches 1.. run scoreboard players operation #st_black nx.gen /= #2 nx.gen
execute as @e[type=marker,tag=nx.gen] at @s run function nonios:generator/second
