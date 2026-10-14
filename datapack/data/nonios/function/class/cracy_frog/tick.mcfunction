# as/at every Cracy Frog, each tick. Broom fuel: 60 ticks (3 s), refills 3/tick on the ground.
scoreboard players set @s nx.cls_kick 0
execute if score @s nx.cls_fuel matches ..59 if predicate nonios:class/on_ground run scoreboard players add @s nx.cls_fuel 3
execute if score @s nx.cls_fuel matches 61.. run scoreboard players set @s nx.cls_fuel 60
execute if score @s nx.cls_fly matches 1.. run function nonios:class/cracy_frog/fly
