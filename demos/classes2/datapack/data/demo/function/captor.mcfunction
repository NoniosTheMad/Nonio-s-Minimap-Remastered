# as + at a player: a still enemy husk (nx.dummy + nx.captor) standing on the nearest arena node
execute unless entity @e[type=marker,tag=nx.node] run return run tellraw @s {"text":"[demo] No arena nodes (Rebuild map).","color":"red"}
function demo:enemy
execute as @e[type=marker,tag=nx.node,sort=nearest,limit=1] at @s run summon minecraft:husk ~ ~ ~ {NoAI:1b,PersistenceRequired:1b,Silent:1b,Tags:["nx.dummy","nx.captor","nx.soul","demo.new"],CustomNameVisible:1b,CustomName:{text:"Captor",color:"red"}}
function demo:join_new with storage demo:tmp
tellraw @s {"text":"[demo] Enemy captor on the nearest node (battle only: it captures).","color":"yellow"}
