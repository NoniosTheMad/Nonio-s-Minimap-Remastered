# as + at the centre generator: "Centre Generator / Lv 2 · 3 rolls · 7s / 42 coins"
scoreboard players operation #div nx.arena = #speed nx.arena
scoreboard players operation #div nx.arena *= #20 nx.arena
execute if score #golden_t nx.arena matches 1.. run scoreboard players operation #div nx.arena *= #cg_gold nx.gen
scoreboard players operation #sec nx.arena = @s nx.gen_t
scoreboard players operation #sec nx.arena += #div nx.arena
scoreboard players remove #sec nx.arena 1
scoreboard players operation #sec nx.arena /= #div nx.arena
execute if score #sec nx.arena matches ..0 run scoreboard players set #sec nx.arena 0
data modify storage nonios:arena ch set value {g:""}
execute store result storage nonios:arena ch.lvl int 1 run scoreboard players get @s nx.gen_lvl
execute store result storage nonios:arena ch.rolls int 1 run scoreboard players get #crolls nx.arena
execute store result storage nonios:arena ch.sec int 1 run scoreboard players get #sec nx.arena
execute store result storage nonios:arena ch.pot int 1 run scoreboard players get @s nx.gen_pot
execute if score #golden_t nx.arena matches 1.. run data modify storage nonios:arena ch.g set value "  x3"
execute if score @s nx.gen_pot matches 1.. run return run function nonios:arena/cgen/holo_pot with storage nonios:arena ch
function nonios:arena/cgen/holo_set with storage nonios:arena ch
