# {team}: rebuild storage nonios:altar v (level, next step, paid / needed) and redraw that altar (hologram + anchor charges)
function nonios:altar/max
$data modify storage nonios:altar v.team set value "$(team)"
$scoreboard players operation #lvl nx.altar = #$(team) nx.cls_lvl
execute if score #lvl nx.altar matches ..0 run scoreboard players set #lvl nx.altar 1
scoreboard players operation #nl nx.altar = #lvl nx.altar
scoreboard players add #nl nx.altar 1
function nonios:altar/roman {s:"#lvl",k:"cur"}
function nonios:altar/roman {s:"#nl",k:"nxt"}
# respawn-anchor charges: level 1 / 2 / 3+ = 1 / 2 / 4
data modify storage nonios:altar v.ch set value "1"
execute if score #lvl nx.altar matches 2 run data modify storage nonios:altar v.ch set value "2"
execute if score #lvl nx.altar matches 3.. run data modify storage nonios:altar v.ch set value "4"
execute if score #lvl nx.altar >= #max nx.altar run return run function nonios:altar/show_done with storage nonios:altar v
execute store result storage nonios:altar arg.i int 1 run scoreboard players get #lvl nx.altar
function nonios:altar/need with storage nonios:altar arg
execute store result storage nonios:altar v.ni int 1 run scoreboard players get #ni nx.altar
execute store result storage nonios:altar v.ng int 1 run scoreboard players get #ng nx.altar
execute store result storage nonios:altar v.nd int 1 run scoreboard players get #nd nx.altar
$execute store result storage nonios:altar v.i int 1 run scoreboard players get #$(team)_iron nx.altar
$execute store result storage nonios:altar v.g int 1 run scoreboard players get #$(team)_gold nx.altar
$execute store result storage nonios:altar v.d int 1 run scoreboard players get #$(team)_diamond nx.altar
function nonios:altar/show with storage nonios:altar v
