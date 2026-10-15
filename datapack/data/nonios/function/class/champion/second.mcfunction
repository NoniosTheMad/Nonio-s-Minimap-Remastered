# once a second: from 3 kills the Champion glows for everyone and its crown sparkles
execute if score @s nx.cls_champ matches 3.. run effect give @s minecraft:glowing 2 0 true
execute if score @s nx.cls_champ matches 3.. run particle minecraft:wax_on ~ ~2.15 ~ 0.25 0.05 0.25 0 4 force
