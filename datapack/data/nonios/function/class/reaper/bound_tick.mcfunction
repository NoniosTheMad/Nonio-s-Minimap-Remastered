# as/at a bound entity (from class/tick, any class), each tick: back onto its pin, a ring of souls, free after 2 s
scoreboard players operation #b nx.cls_tmp = @s nx.cls_bid
execute as @e[type=marker,tag=nx.reaper_pin] if score @s nx.cls_bid = #b nx.cls_tmp run tag @s add nx.cls_pin
execute positioned as @e[type=marker,tag=nx.cls_pin,limit=1] run tp @s ~ ~ ~
tag @e[tag=nx.cls_pin] remove nx.cls_pin
execute if predicate nonios:class/coin run particle minecraft:soul ~ ~0.1 ~ 0.4 0.05 0.4 0.01 1
particle minecraft:dust{color:[0.35,0.15,0.6],scale:0.8} ~ ~0.3 ~ 0.35 0.3 0.35 0 2
execute store result score #now nx.cls_tmp run time query gametime
execute if score #now nx.cls_tmp >= @s nx.cls_bnd run function nonios:class/reaper/unbind
