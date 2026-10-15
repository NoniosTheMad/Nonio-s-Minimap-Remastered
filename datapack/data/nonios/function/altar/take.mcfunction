# {team,m,id,n}: as the offering player: move min(still needed, carried) blocks of $(id) into #<team>_<m>
$scoreboard players operation #left nx.altar = $(n) nx.altar
$scoreboard players operation #left nx.altar -= #$(team)_$(m) nx.altar
execute if score #left nx.altar matches ..0 run return 0
$execute store result score #have nx.altar run clear @s $(id) 0
execute if score #have nx.altar matches ..0 run return 0
scoreboard players operation #left nx.altar < #have nx.altar
execute store result storage nonios:altar arg.c int 1 run scoreboard players get #left nx.altar
$data modify storage nonios:altar arg.id set value "$(id)"
function nonios:altar/clear with storage nonios:altar arg
$scoreboard players operation #$(team)_$(m) nx.altar += #left nx.altar
scoreboard players operation #gave nx.altar += #left nx.altar
