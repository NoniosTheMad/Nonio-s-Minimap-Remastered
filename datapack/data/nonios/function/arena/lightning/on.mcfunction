# Lightning ON (remembered across reloads): the Lightning Rabbit spawns at the arena centre on the next loop
scoreboard players set #lt_set nx.arena 1
scoreboard players set #lt_on nx.arena 1
scoreboard players set #lt_rt nx.arena 0
scoreboard players operation #lt_t nx.arena = #lt_every nx.arena
tellraw @a [{text:"⚡ ",color:"yellow"},{text:"Lightning ON",color:"yellow",bold:true},{text:": the Lightning Rabbit is loose in the Arena. Kill it for its loot (it comes back).",color:"gray"}]
execute as @a at @s run playsound minecraft:entity.lightning_bolt.thunder weather @s ~ ~ ~ 0.6 1
