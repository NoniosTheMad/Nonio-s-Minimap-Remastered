# as + at a player: run $(fn) as + at the nearest generator; report its new level
scoreboard players set #ok demo.c 0
$execute as @e[type=marker,tag=nx.gen,sort=nearest,limit=1] at @s store success score #ok demo.c run function nonios:generator/$(fn)
execute if score #ok demo.c matches 0 run tellraw @s {text:"[demo] nothing to do (already at the limit)",color:"gray"}
execute if score #ok demo.c matches 1.. as @e[type=marker,tag=nx.gen,sort=nearest,limit=1] run tellraw @a [{text:"[demo] nearest generator is now Lv ",color:"aqua"},{score:{name:"@s",objective:"nx.gen_lvl"},color:"yellow"}]
