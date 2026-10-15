# every arena loop (10 ticks) while the arena runs: a mined core regrows `core_regrow` ticks later (V2: at once)
execute as @e[type=marker,tag=nx.acore] at @s run function nonios:arena/core/check
