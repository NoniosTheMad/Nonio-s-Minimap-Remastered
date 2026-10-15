# as/at a Reaper in the air, each tick. Steers its gravity so the vertical speed goes to a target picked by the keys:
# jump = rise 5 b/s, sneak = sink 6 b/s, neither = hover. Never tied to the camera.
# v = vertical speed (milliblocks/tick, averaged over 2 ticks: position packets arrive unevenly)
execute store result score #y nx.cls_tmp run data get entity @s Pos[1] 1000
scoreboard players operation #v nx.cls_tmp = #y nx.cls_tmp
scoreboard players operation #v nx.cls_tmp -= @s nx.cls_ry2
scoreboard players operation #v nx.cls_tmp /= #2 nx.cls_tmp
scoreboard players operation @s nx.cls_ry2 = @s nx.cls_ry1
scoreboard players operation @s nx.cls_ry1 = #y nx.cls_tmp
scoreboard players set #tg nx.cls_tmp 0
execute if predicate nonios:class/reaper/jump run scoreboard players set #tg nx.cls_tmp 250
execute if predicate nonios:class/reaper/sneak run scoreboard players set #tg nx.cls_tmp -300
# lift only near the ground: no block within 10 below = no rising, a slow sink (no crossing the void, no sky camping)
execute if score #tg nx.cls_tmp matches -99.. unless function nonios:class/reaper/near_ground run scoreboard players set #tg nx.cls_tmp -100
# slow falling (falls only 0.01/tick and keeps the fall distance at 0: no crits from hovering) except while diving
execute if score #tg nx.cls_tmp matches ..-300 run effect clear @s minecraft:slow_falling
execute if score #tg nx.cls_tmp matches -299.. unless predicate nonios:class/reaper/slow_falling run effect give @s minecraft:slow_falling infinite 0 true
# a = (target - v) / 10 per tick, max 0.06; gravity modifier = -0.08 - a (cancels vanilla's 0.08, then steers)
scoreboard players operation #a nx.cls_tmp = #tg nx.cls_tmp
scoreboard players operation #a nx.cls_tmp -= #v nx.cls_tmp
scoreboard players operation #a nx.cls_tmp /= #10 nx.cls_tmp
execute if score #a nx.cls_tmp matches 61.. run scoreboard players set #a nx.cls_tmp 60
execute if score #a nx.cls_tmp matches ..-61 run scoreboard players set #a nx.cls_tmp -60
scoreboard players set #g nx.cls_tmp -80
scoreboard players operation #g nx.cls_tmp -= #a nx.cls_tmp
execute if score #g nx.cls_tmp = @s nx.cls_rg run return 0
scoreboard players operation @s nx.cls_rg = #g nx.cls_tmp
execute store result storage nonios:class fly.g double 0.001 run scoreboard players get #g nx.cls_tmp
function nonios:class/reaper/fly_set with storage nonios:class fly
