# {team}: as/at a player of that team at its altar. Takes from the inventory what the next step still needs (never more).
function nonios:altar/max
$scoreboard players operation #lvl nx.altar = #$(team) nx.cls_lvl
execute if score #lvl nx.altar >= #max nx.altar run return run title @s actionbar {text:"The altar is fulfilled.",color:"light_purple"}
execute store result storage nonios:altar arg.i int 1 run scoreboard players get #lvl nx.altar
function nonios:altar/need with storage nonios:altar arg
scoreboard players set #gave nx.altar 0
$function nonios:altar/take {team:"$(team)",m:"iron",id:"minecraft:iron_block",n:"#ni"}
$function nonios:altar/take {team:"$(team)",m:"gold",id:"minecraft:gold_block",n:"#ng"}
$function nonios:altar/take {team:"$(team)",m:"diamond",id:"minecraft:diamond_block",n:"#nd"}
$execute if score #$(team)_iron nx.altar >= #ni nx.altar if score #$(team)_gold nx.altar >= #ng nx.altar if score #$(team)_diamond nx.altar >= #nd nx.altar run return run function nonios:altar/level_up {team:"$(team)"}
$function nonios:altar/refresh {team:"$(team)"}
execute if score #gave nx.altar matches 1.. run playsound minecraft:block.respawn_anchor.charge block @a ~ ~ ~ 0.7 1.3
execute if score #gave nx.altar matches 0 run playsound minecraft:block.respawn_anchor.deplete block @s ~ ~ ~ 0.4 1.6
function nonios:altar/bar with storage nonios:altar v
