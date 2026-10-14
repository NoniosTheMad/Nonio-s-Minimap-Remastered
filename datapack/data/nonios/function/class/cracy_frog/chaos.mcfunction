# enchantment nonios:class/frog_tongue (post_attack): as/at the victim. Something random happens. #Useful
playsound minecraft:entity.frog.tongue player @a ~ ~ ~ 1.5 1.2
particle minecraft:item_slime ~ ~1 ~ 0.4 0.5 0.4 0.1 15
execute store result score #r nx.cls_tmp run random value 1..5
# 1: a gust under its feet (yeet)
execute if score #r nx.cls_tmp matches 1 run summon minecraft:wind_charge ~ ~0.3 ~ {Motion:[0.0,-1.0,0.0]}
# 2: up it goes
execute if score #r nx.cls_tmp matches 2 run effect give @s minecraft:levitation 2 2
# 3: turned around
execute if score #r nx.cls_tmp matches 3 run rotate @s ~180 ~
execute if score #r nx.cls_tmp matches 3 run playsound minecraft:entity.frog.ambient player @a ~ ~ ~ 2 1.8
# 4: the world melts a little for it too
execute if score #r nx.cls_tmp matches 4 run effect give @s minecraft:nausea 5 0
execute if score #r nx.cls_tmp matches 4 run effect give @s minecraft:slowness 3 1
# 5: sticky (rooted for a moment) then bouncy
execute if score #r nx.cls_tmp matches 5 run effect give @s minecraft:slowness 1 6
execute if score #r nx.cls_tmp matches 5 run effect give @s minecraft:jump_boost 2 4
