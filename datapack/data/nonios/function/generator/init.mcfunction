# as + at a freshly summoned generator marker
tag @s remove nx.gen_new
function nonios:generator/init_team with entity @s data
execute store result score @s nx.gen_lvl run data get entity @s data.lvl
scoreboard players set @s nx.gen_t 2147483647
function nonios:generator/apply
function nonios:generator/grow
