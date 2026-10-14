# as + at a freshly summoned node marker; storage nonios:arena n = its resolved config
tag @s remove nx.node_new
data modify entity @s data set from storage nonios:arena n
scoreboard players set @s nx.ar_cap 0
scoreboard players set @s nx.ar_own 0
scoreboard players set @s nx.ar_st -1
execute store result score @s nx.ar_iv run data get storage nonios:arena n.every
scoreboard players operation @s nx.ar_t = @s nx.ar_iv
function nonios:arena/node/init_m with storage nonios:arena n
scoreboard players set #st nx.arena 0
scoreboard players set #sgn nx.arena 0
function nonios:arena/node/restyle
