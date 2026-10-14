# as the core item_display
execute store result score #yaw nx.gen run data get entity @s Rotation[0]
scoreboard players operation #yaw nx.gen += #spin nx.gen
scoreboard players operation #yaw nx.gen %= #360 nx.gen
execute store result storage nonios:gen s.yaw int 1 run scoreboard players get #yaw nx.gen
function nonios:generator/spin_tp with storage nonios:gen s
