scoreboard players add #timer nx.state 1
scoreboard players operation #s nx.tmp = #timer nx.state
scoreboard players operation #s nx.tmp %= #20 nx.const
execute if score #s nx.tmp matches 0 run function nonios:game/battle/second
