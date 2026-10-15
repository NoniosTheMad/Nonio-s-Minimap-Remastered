# as a landed dreamer, at them, every tick: their pixie (a shop that follows) hovers just off their shoulder, through walls
scoreboard players operation #me nx.dream = @s nx.pid
tag @e[tag=nx.pix_me] remove nx.pix_me
execute as @e[type=allay,tag=nx.pixie] if score @s nx.pid = #me nx.dream run tag @s add nx.pix_me
execute as @e[type=interaction,tag=nx.pixie] if score @s nx.pid = #me nx.dream run tag @s add nx.pix_me
execute unless entity @e[type=interaction,tag=nx.pix_me] run function nonios:dream/pixie/spawn
execute unless entity @e[type=allay,tag=nx.pix_me] run function nonios:dream/pixie/spawn
execute positioned ~-0.8 ~1.45 ~-0.8 run tp @e[type=allay,tag=nx.pix_me] ~ ~ ~ facing entity @s eyes
execute positioned ~-0.8 ~1.15 ~-0.8 run tp @e[type=interaction,tag=nx.pix_me] ~ ~ ~
tag @e[tag=nx.pix_me] remove nx.pix_me
