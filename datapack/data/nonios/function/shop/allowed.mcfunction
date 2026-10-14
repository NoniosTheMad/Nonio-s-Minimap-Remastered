# succeeds when @s may shop here: within 6 blocks of a shopkeeper of their team (or team "any"), or tagged nx.shop_anywhere (demo)
execute if entity @s[tag=nx.shop_anywhere] run return 1
execute if entity @e[type=interaction,tag=nx.shop_npc,tag=nx.any,distance=..6] run return 1
execute if entity @s[team=white] if entity @e[type=interaction,tag=nx.shop_npc,tag=nx.white,distance=..6] run return 1
execute if entity @s[team=black] if entity @e[type=interaction,tag=nx.shop_npc,tag=nx.black,distance=..6] run return 1
return fail
