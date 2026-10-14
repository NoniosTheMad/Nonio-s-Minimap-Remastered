scoreboard players set @s nx.cls_askst 0
tellraw @s [{"text":"Shop Keeper: ","color":"red","bold":true},{"text":"...Your funeral. Ribbit.","color":"white","bold":false}]
execute at @s run function nonios:class/set_id {id:"cracy_frog"}
