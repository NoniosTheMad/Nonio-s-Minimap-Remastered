# Rage stays 0..100; any change counts as combat (berserker/cool waits 3 s after it)
execute if score @s nx.cls_brg matches 101.. run scoreboard players set @s nx.cls_brg 100
execute store result score @s nx.cls_brt run time query gametime
