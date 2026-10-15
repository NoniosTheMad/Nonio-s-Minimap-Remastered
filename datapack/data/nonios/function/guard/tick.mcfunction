# from nonios:tick. Cheap when idle: one score check outside prep/battle, then one counter.
execute unless score #state nx.state matches 1..2 run return 0
scoreboard players add #t nx.guard 1
execute if score #t nx.guard matches ..9 run return 0
scoreboard players set #t nx.guard 0
execute if data storage nonios:config {spawn_guard:0b} run return 0
function nonios:guard/zone with storage nonios:map white.guard
function nonios:guard/zone with storage nonios:map black.guard
