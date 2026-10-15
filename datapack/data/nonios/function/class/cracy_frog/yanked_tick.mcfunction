# as/at a player the tongue yanked (from class/tick, any class): keep the peak, hurt on landing.
scoreboard players add @s nx.cls_yk 1
execute if entity @s[gamemode=!survival,gamemode=!adventure] run return run function nonios:class/cracy_frog/yank_end
execute if score @s nx.cls_yk matches 200.. run return run function nonios:class/cracy_frog/yank_end
# dragged down: nothing keeps them up
execute if entity @s[tag=nx.frog_hooked] run effect clear @s minecraft:levitation
execute if entity @s[tag=nx.frog_hooked] run effect clear @s minecraft:slow_falling
# the counters: water, lava, cobweb, slow falling
execute if block ~ ~ ~ #nonios:class/reaper_fluid run return run function nonios:class/cracy_frog/yank_end
execute if block ~ ~ ~ minecraft:cobweb run return run function nonios:class/cracy_frog/yank_end
execute if predicate nonios:class/reaper/slow_falling run return run function nonios:class/cracy_frog/yank_end
execute store result score #y nx.cls_tmp run data get entity @s Pos[1] 10
execute if score #y nx.cls_tmp > @s nx.cls_ypk run scoreboard players operation @s nx.cls_ypk = #y nx.cls_tmp
execute if score @s nx.cls_yk matches 4.. if predicate nonios:class/on_ground run function nonios:class/cracy_frog/yank_land
