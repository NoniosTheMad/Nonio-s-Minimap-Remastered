# as + at a generator marker; the clicking player is tagged nx.gen_clicker.
# Drops lying on the generator jump to the clicker (who picks them up), and the coin pot goes into their purse.
execute as @e[type=item,distance=..2] run tp @s @p[tag=nx.gen_clicker]
scoreboard players operation #got nx.gen = @s nx.gen_pot
execute if score #got nx.gen matches ..0 run return run title @p[tag=nx.gen_clicker] actionbar {text:"No coins yet",color:"gray"}
scoreboard players operation @p[tag=nx.gen_clicker] nx.coins += #got nx.gen
scoreboard players set @s nx.gen_pot 0
title @p[tag=nx.gen_clicker] actionbar [{text:"+",color:"gold"},{score:{name:"#got",objective:"nx.gen"},color:"gold"},{text:" coins",color:"gold"}]
playsound minecraft:entity.experience_orb.pickup player @p[tag=nx.gen_clicker] ~ ~ ~ 0.8 1.4
function nonios:generator/holo
