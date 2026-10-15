# start tracking a yanked player: launch height and peak (tenths of a block), ticks in the air
tag @s add nx.frog_yanked
scoreboard players set @s nx.cls_yk 0
execute store result score @s nx.cls_y0 run data get entity @s Pos[1] 10
scoreboard players operation @s nx.cls_ypk = @s nx.cls_y0
