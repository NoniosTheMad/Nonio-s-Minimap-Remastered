# as an ore marker of the Miner tagged nx.spel_me: the ore is gone (mined) -> drop it, else its dot
execute unless block ~ ~ ~ #nonios:class/spelunk run return run kill @s
execute if entity @s[tag=nx.spel_coal] run return run function nonios:class/miner/spel_draw {c:"0.45,0.45,0.45"}
execute if entity @s[tag=nx.spel_iron] run return run function nonios:class/miner/spel_draw {c:"0.9,0.68,0.5"}
execute if entity @s[tag=nx.spel_copper] run return run function nonios:class/miner/spel_draw {c:"0.95,0.45,0.15"}
execute if entity @s[tag=nx.spel_gold] run return run function nonios:class/miner/spel_draw {c:"1.0,0.85,0.05"}
execute if entity @s[tag=nx.spel_redstone] run return run function nonios:class/miner/spel_draw {c:"1.0,0.05,0.05"}
execute if entity @s[tag=nx.spel_lapis] run return run function nonios:class/miner/spel_draw {c:"0.15,0.3,1.0"}
execute if entity @s[tag=nx.spel_diamond] run return run function nonios:class/miner/spel_draw {c:"0.3,1.0,0.95"}
execute if entity @s[tag=nx.spel_emerald] run return run function nonios:class/miner/spel_draw {c:"0.1,1.0,0.3"}
execute if entity @s[tag=nx.spel_quartz] run return run function nonios:class/miner/spel_draw {c:"1.0,1.0,1.0"}
execute if entity @s[tag=nx.spel_debris] run return run function nonios:class/miner/spel_draw {c:"0.6,0.3,0.25"}
