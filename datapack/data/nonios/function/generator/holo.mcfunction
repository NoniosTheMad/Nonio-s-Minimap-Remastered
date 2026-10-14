# as + at a generator marker: rewrite the hologram ("White generator / Lv 2 · next drop 4s / 12 coins / upgrade: 500 coins")
# seconds left (real time) = ceil(t / step)
scoreboard players operation #sec nx.gen = @s nx.gen_t
scoreboard players operation #sec nx.gen += #step nx.gen
scoreboard players remove #sec nx.gen 1
scoreboard players operation #sec nx.gen /= #step nx.gen
execute if score #sec nx.gen matches ..0 run scoreboard players set #sec nx.gen 0
data modify storage nonios:gen h set from entity @s data
execute store result storage nonios:gen h.sec int 1 run scoreboard players get #sec nx.gen
execute store result storage nonios:gen h.pot int 1 run scoreboard players get @s nx.gen_pot
execute if entity @s[tag=!nx.gen_full] run function nonios:generator/holo_next with storage nonios:gen h
execute if entity @s[tag=nx.gen_full] run data modify storage nonios:gen h.next set value "full: pick up the drops"
data modify storage nonios:gen h.up set value "max level"
execute if score @s nx.gen_lvl matches ..1 store result storage nonios:gen h.cost int 1 run scoreboard players get #cost2 nx.gen
execute if score @s nx.gen_lvl matches 2 store result storage nonios:gen h.cost int 1 run scoreboard players get #cost3 nx.gen
execute if score @s nx.gen_lvl matches ..2 run function nonios:generator/holo_up with storage nonios:gen h
execute if score @s nx.gen_pot matches 1.. run return run function nonios:generator/holo_pot with storage nonios:gen h
function nonios:generator/holo_nopot with storage nonios:gen h
