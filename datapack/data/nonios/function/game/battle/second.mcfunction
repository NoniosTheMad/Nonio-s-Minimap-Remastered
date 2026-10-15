# once per second: elapsed time on the bossbar + safety-net win check (e.g. the last player of a team logged out)
scoreboard players operation #sec nx.tmp = #timer nx.state
scoreboard players operation #sec nx.tmp /= #20 nx.const
function nonios:game/clock
execute if score #ss nx.tmp matches 10.. run bossbar set nonios:phase name [{"text":"⚔ Battle  ","color":"red"},{"score":{"name":"#mm","objective":"nx.tmp"},"color":"white"},{"text":":","color":"white"},{"score":{"name":"#ss","objective":"nx.tmp"},"color":"white"}]
execute if score #ss nx.tmp matches ..9 run bossbar set nonios:phase name [{"text":"⚔ Battle  ","color":"red"},{"score":{"name":"#mm","objective":"nx.tmp"},"color":"white"},{"text":":0","color":"white"},{"score":{"name":"#ss","objective":"nx.tmp"},"color":"white"}]
bossbar set nonios:phase players @a
function nonios:game/win_check
