# as + at the centre generator; clicker tagged nx.cg_clicker: drops jump to the clicker, the pot goes to their purse
execute as @e[type=item,distance=..2.5] run tp @s @p[tag=nx.cg_clicker]
scoreboard players operation #got nx.arena = @s nx.gen_pot
execute if score #got nx.arena matches ..0 run return 0
scoreboard players operation @p[tag=nx.cg_clicker] nx.coins += #got nx.arena
scoreboard players set @s nx.gen_pot 0
title @p[tag=nx.cg_clicker] actionbar [{text:"+",color:"gold"},{score:{name:"#got",objective:"nx.arena"},color:"gold"},{text:" coins",color:"gold"}]
playsound minecraft:entity.experience_orb.pickup player @p[tag=nx.cg_clicker] ~ ~ ~ 0.8 1.4
function nonios:arena/cgen/holo
