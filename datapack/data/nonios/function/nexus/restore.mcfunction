# as/at the core marker: undo an illegal Nexus break
setblock ~ ~ ~ minecraft:obsidian
kill @e[type=item,distance=..3,nbt={Item:{id:"minecraft:obsidian"}}]
$tellraw @a[scores={nx.mn.obsidian=1..}] {"text":"$(why) The Nexus was restored.","color":"red"}
scoreboard players set @a[scores={nx.mn.obsidian=1..}] nx.mn.obsidian 0
