# as an arrow in flight near a Barrier: nx.arsp = |Motion| x100 (integer sqrt, Newton). Stuck/slow arrows keep the last value.
execute if data entity @s {inGround:1b} run return 0
execute store result score #mx nx.tmp run data get entity @s Motion[0] 100
execute store result score #my nx.tmp run data get entity @s Motion[1] 100
execute store result score #mz nx.tmp run data get entity @s Motion[2] 100
scoreboard players operation #mx nx.tmp *= #mx nx.tmp
scoreboard players operation #my nx.tmp *= #my nx.tmp
scoreboard players operation #mz nx.tmp *= #mz nx.tmp
scoreboard players operation #mx nx.tmp += #my nx.tmp
scoreboard players operation #mx nx.tmp += #mz nx.tmp
execute if score #mx nx.tmp matches ..99 run return 0
scoreboard players set #r nx.tmp 200
function nonios:nexus/arrow_sqrt
function nonios:nexus/arrow_sqrt
function nonios:nexus/arrow_sqrt
function nonios:nexus/arrow_sqrt
function nonios:nexus/arrow_sqrt
function nonios:nexus/arrow_sqrt
scoreboard players operation @s nx.arsp = #r nx.tmp
