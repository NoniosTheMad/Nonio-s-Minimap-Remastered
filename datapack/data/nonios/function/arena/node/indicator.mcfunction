# as + at a node marker: the indicator block shows owner (red while contested)
data modify storage nonios:arena ind set value {}
data modify storage nonios:arena ind.dy set from entity @s data.ind
data modify storage nonios:arena ind.b set from storage nonios:arena config.blocks.none
execute if score @s nx.ar_own matches 1 run data modify storage nonios:arena ind.b set from storage nonios:arena config.blocks.white
execute if score @s nx.ar_own matches 2 run data modify storage nonios:arena ind.b set from storage nonios:arena config.blocks.black
execute if score #st nx.arena matches 3 run data modify storage nonios:arena ind.b set from storage nonios:arena config.blocks.contested
function nonios:arena/node/indicator_m with storage nonios:arena ind
