# as the Reaper (#now = gametime): untouchable (resistance V) for 3 s, remembered so a second kill inside it doesn't extend it
effect give @s minecraft:resistance 3 4 true
scoreboard players operation @s nx.cls_ward = #now nx.cls_tmp
scoreboard players add @s nx.cls_ward 60
