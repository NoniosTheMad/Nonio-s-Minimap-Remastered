# as + at a node marker, every 10 ticks
# 1) who is inside (#w, #b; also shows the bossbar to everyone inside)
function nonios:arena/node/scan with entity @s data
# 2) progress. #st: 0 neutral, 1/2 White/Black capturing, 3 contested, 4/5 held by White/Black, 6/7 White/Black neutralising
scoreboard players set #st nx.arena 0
execute if score #w nx.arena matches 1.. if score #b nx.arena matches 1.. run scoreboard players set #st nx.arena 3
execute if score #w nx.arena matches 1.. if score #b nx.arena matches 0 run function nonios:arena/node/push_white
execute if score #b nx.arena matches 1.. if score #w nx.arena matches 0 run function nonios:arena/node/push_black
execute if score #w nx.arena matches 0 if score #b nx.arena matches 0 run function nonios:arena/node/idle
# 3) ownership changes
execute if score @s nx.ar_own matches 1 if score @s nx.ar_cap matches ..0 run function nonios:arena/node/neutral
execute if score @s nx.ar_own matches 2 if score @s nx.ar_cap matches 0.. run function nonios:arena/node/neutral
execute unless score @s nx.ar_own matches 1 if score @s nx.ar_cap >= #capture nx.arena run function nonios:arena/node/captured {team:"white",tname:"White",col:"white",own:1,st:4}
execute unless score @s nx.ar_own matches 2 if score @s nx.ar_cap <= #ncap nx.arena run function nonios:arena/node/captured {team:"black",tname:"Black",col:"dark_purple",own:2,st:5}
# 4) display: restyle only when state or progress sign changes
scoreboard players set #sgn nx.arena 0
execute if score @s nx.ar_cap matches 1.. run scoreboard players set #sgn nx.arena 1
execute if score @s nx.ar_cap matches ..-1 run scoreboard players set #sgn nx.arena 2
scoreboard players operation #code nx.arena = #st nx.arena
scoreboard players operation #code nx.arena *= #10 nx.arena
scoreboard players operation #code nx.arena += #sgn nx.arena
execute unless score @s nx.ar_st = #code nx.arena run function nonios:arena/node/restyle
scoreboard players operation #abs nx.arena = @s nx.ar_cap
execute if score #abs nx.arena matches ..-1 run scoreboard players operation #abs nx.arena *= #-1 nx.arena
function nonios:arena/node/bar with entity @s data
# 5) held: count the bonus, payout timer
execute if score @s nx.ar_own matches 1.. if data entity @s data.bonus run function nonios:arena/node/tally with entity @s data
execute if score @s nx.ar_own matches 1.. run function nonios:arena/node/payout_timer
# 6) once a second: hologram, indicator, particles
execute if score #half nx.arena matches 0 run function nonios:arena/node/second
