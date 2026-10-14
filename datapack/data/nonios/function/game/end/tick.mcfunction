scoreboard players remove #timer nx.state 1
execute if score #timer nx.state matches ..0 run return run function nonios:game/to_lobby
scoreboard players operation #s nx.tmp = #timer nx.state
scoreboard players operation #s nx.tmp %= #20 nx.const
execute unless score #s nx.tmp matches 0 run return 0
scoreboard players operation #sec nx.tmp = #timer nx.state
scoreboard players operation #sec nx.tmp /= #20 nx.const
execute store result bossbar nonios:phase value run scoreboard players get #sec nx.tmp
bossbar set nonios:phase name [{"text":"Back to the lobby in ","color":"yellow"},{"score":{"name":"#sec","objective":"nx.tmp"},"color":"white"},{"text":" s","color":"yellow"}]
bossbar set nonios:phase players @a
