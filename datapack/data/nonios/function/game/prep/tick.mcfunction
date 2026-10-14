scoreboard players remove #timer nx.state 1
scoreboard players operation #s nx.tmp = #timer nx.state
scoreboard players operation #s nx.tmp %= #20 nx.const
execute if score #timer nx.state matches ..0 run return run function nonios:game/battle/start
execute if score #s nx.tmp matches 0 run function nonios:game/prep/second
