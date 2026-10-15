# as the Reaper (#now = gametime): resistance V for 8 s, remembered so a second kill inside it doesn't extend it
effect give @s minecraft:resistance 8 4 true
scoreboard players operation @s nx.cls_ward = #now nx.cls_tmp
scoreboard players add @s nx.cls_ward 160
