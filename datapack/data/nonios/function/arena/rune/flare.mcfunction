# as + at a node just captured, macro {team}: the whole rune flares big in the team colour and throws sparks
data modify storage nonios:arena rx set value {hp:"0 0 0 0 2",cp:"0 0 0 0 1",tip:"minecraft:end_rod"}
$data modify storage nonios:arena rx.hot set from storage nonios:arena config.rune.col.$(team)_pulse
data modify storage nonios:arena rx.cold set from storage nonios:arena rx.hot
scoreboard players set #lit nx.arena 999
scoreboard players set #tip nx.arena 0
function nonios:arena/rune/view
data modify storage nonios:arena rx merge value {hot:"minecraft:firework",hp:"0 0 0 0.08 1"}
function nonios:arena/rune/view
scoreboard players set @s nx.ar_fx 8
