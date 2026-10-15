# as + at a node marker: the owner lost it (the other team drained it to 0)
scoreboard players set @s nx.ar_own 0
execute if score #st nx.arena matches 6 run scoreboard players set #st nx.arena 1
execute if score #st nx.arena matches 7 run scoreboard players set #st nx.arena 2
tellraw @a [{text:"⚐ ",color:"gray"},{entity:"@s",nbt:"data.label",color:"yellow"},{text:" is unclaimed again",color:"gray"}]
playsound minecraft:block.beacon.deactivate master @a ~ ~ ~ 3 1.2
function nonios:arena/rune/fizzle
data modify storage nonios:arena cap set value {team:""}
data modify storage nonios:arena cap.node set from entity @s data.id
data modify storage nonios:arena cap.name set from entity @s data.label
function #nonios:arena/on_capture
