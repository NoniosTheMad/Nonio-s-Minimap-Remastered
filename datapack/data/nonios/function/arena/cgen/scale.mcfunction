# as the centre generator: strength from the coins in both team banks, B = #white + #black nx.bank.
# Level 1/2/3 at B >= cg_bank1/2/3 (core size); emeralds per spit = 1 + B / bank_per_roll (max).
execute store result score #cb_w nx.arena run scoreboard players get #white nx.bank
execute store result score #cb_b nx.arena run scoreboard players get #black nx.bank
scoreboard players operation #cbank nx.arena = #cb_w nx.arena
scoreboard players operation #cbank nx.arena += #cb_b nx.arena
scoreboard players set #cl nx.arena 1
execute if score #cbank nx.arena >= #cg_bank2 nx.gen run scoreboard players set #cl nx.arena 2
execute if score #cbank nx.arena >= #cg_bank3 nx.gen run scoreboard players set #cl nx.arena 3
execute unless score @s nx.gen_lvl = #cl nx.arena run function nonios:arena/cgen/level
scoreboard players operation #crolls nx.arena = #cbank nx.arena
scoreboard players operation #crolls nx.arena /= #cg_bpr nx.gen
scoreboard players add #crolls nx.arena 1
scoreboard players operation #crolls nx.arena < #cg_maxr nx.gen
execute if score #crolls nx.arena matches ..0 run scoreboard players set #crolls nx.arena 1
