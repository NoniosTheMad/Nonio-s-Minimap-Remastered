# as + at a node marker after #st / #sgn changed: bossbar name + colour, indicator block, hologram
scoreboard players operation #code nx.arena = #st nx.arena
scoreboard players operation #code nx.arena *= #10 nx.arena
scoreboard players operation #code nx.arena += #sgn nx.arena
scoreboard players operation @s nx.ar_st = #code nx.arena
data modify storage nonios:arena sty set value {btxt:""}
data modify storage nonios:arena sty merge from entity @s data
function nonios:arena/node/style with storage nonios:arena sty
execute if score #indicator nx.arena matches 1 run function nonios:arena/node/indicator
function nonios:arena/node/holo
