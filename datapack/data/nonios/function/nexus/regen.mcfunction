# 20% of max per minute (user, 2026-10-14): each tick add max*mult to an accumulator; every #regen_unit (6000) = +1 HP
scoreboard players operation #tmp nx.const = @s nx.hp_max
scoreboard players operation #tmp nx.const *= #regen_mult nx.const
scoreboard players operation @s nx.regen += #tmp nx.const
execute if score @s nx.regen >= #regen_unit nx.const run function nonios:nexus/regen_step
