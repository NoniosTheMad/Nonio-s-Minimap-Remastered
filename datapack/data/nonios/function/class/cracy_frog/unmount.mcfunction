# off the broom (sneaked, out of fuel, class gone): the broom vanishes, a short slow fall to land safely
scoreboard players set @s nx.cls_fly 0
function nonios:dream/pid
scoreboard players operation #me nx.cls_tmp = @s nx.pid
function nonios:class/cracy_frog/mount_kill
effect give @s minecraft:slow_falling 3 0 true
particle minecraft:witch ~ ~0.5 ~ 0.4 0.2 0.4 0 10
