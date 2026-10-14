# once per second during prep: bossbar countdown, last-5s titles, keep everyone on their own side
scoreboard players operation #sec nx.tmp = #timer nx.state
scoreboard players operation #sec nx.tmp /= #20 nx.const
execute store result bossbar nonios:phase value run scoreboard players get #sec nx.tmp
function nonios:game/clock
execute if score #ss nx.tmp matches 10.. run bossbar set nonios:phase name [{"text":"Preparation  ","color":"yellow"},{"score":{"name":"#mm","objective":"nx.tmp"},"color":"white"},{"text":":","color":"white"},{"score":{"name":"#ss","objective":"nx.tmp"},"color":"white"}]
execute if score #ss nx.tmp matches ..9 run bossbar set nonios:phase name [{"text":"Preparation  ","color":"yellow"},{"score":{"name":"#mm","objective":"nx.tmp"},"color":"white"},{"text":":0","color":"white"},{"score":{"name":"#ss","objective":"nx.tmp"},"color":"white"}]
bossbar set nonios:phase players @a
execute if score #sec nx.tmp matches 1..5 run title @a times 0 25 5
execute if score #sec nx.tmp matches 1..5 run title @a subtitle {"text":"Walls drop in","color":"gray"}
execute if score #sec nx.tmp matches 1..5 run title @a title {"score":{"name":"#sec","objective":"nx.tmp"},"color":"yellow","bold":true}
execute if score #sec nx.tmp matches 1..5 as @a at @s run playsound minecraft:block.note_block.hat master @s ~ ~ ~ 1 1
function nonios:game/prep/contain with storage nonios:map white
function nonios:game/prep/contain with storage nonios:map black
