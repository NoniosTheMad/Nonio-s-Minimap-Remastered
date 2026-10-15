# as/at every Cracy Frog, each tick. Broom fuel: 160 ticks (8 s), refills 4/tick on the ground (off the broom).
# tongue spring: the frog_spring boots push when nx.cls_leap is exactly 1
execute if score @s nx.cls_leap matches 1.. run scoreboard players remove @s nx.cls_leap 1
# a mid-air yank burst that missed would fly up forever
kill @e[type=wind_charge,tag=nx.frog_wc]
execute if score @s nx.cls_tng matches 1.. run function nonios:class/cracy_frog/tongue_tick
execute if score @s nx.cls_fuel matches ..159 unless score @s nx.cls_fly matches 1.. if predicate nonios:class/on_ground run scoreboard players add @s nx.cls_fuel 4
execute if score @s nx.cls_fuel matches 161.. run scoreboard players set @s nx.cls_fuel 160
execute if score @s nx.cls_fly matches 1.. run function nonios:class/cracy_frog/fly
