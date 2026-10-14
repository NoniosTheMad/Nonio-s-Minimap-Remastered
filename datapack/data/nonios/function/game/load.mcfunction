# Match lifecycle (DESIGN §2.1-2.4). #state nx.state: 0 lobby, 1 prep, 2 battle, 3 end.
# #map nx.state = 1 once map/build ran: only then does the game manage players (spike demos keep full control).
scoreboard objectives add nx.kills playerKillCount {"text":"Kills"}
scoreboard objectives add nx.deaths dummy
scoreboard objectives add nx.nxdmg dummy
scoreboard objectives add nx.nxpct dummy
scoreboard objectives add nx.nxkill dummy
scoreboard objectives add nx.mn.obsidian minecraft.mined:minecraft.obsidian
scoreboard objectives add nx.match dummy
scoreboard objectives add nx.left minecraft.custom:minecraft.leave_game
scoreboard objectives add nx.last dummy
scoreboard objectives add nx.team trigger
scoreboard objectives add nx.admin trigger
execute unless score #state nx.state matches 0.. run scoreboard players set #state nx.state 0
execute unless score #match nx.state matches 0.. run scoreboard players set #match nx.state 0
scoreboard players set #20 nx.const 20
scoreboard players set #60 nx.const 60
# config (storage nonios:config): defaults only when missing, so admin changes survive /reload
execute unless data storage nonios:config prep_time run data modify storage nonios:config prep_time set value 300
execute unless data storage nonios:config start_coins run data modify storage nonios:config start_coins set value 0
execute unless data storage nonios:config keep_inventory run data modify storage nonios:config keep_inventory set value 1b
execute unless data storage nonios:config barrier_hp run data modify storage nonios:config barrier_hp set value 1000
execute unless data storage nonios:config auto_balance run data modify storage nonios:config auto_balance set value 1b
execute unless data storage nonios:config end_time run data modify storage nonios:config end_time set value 15
function nonios:team/load
bossbar add nonios:phase ""
bossbar set nonios:phase style notched_10
function nonios:map/config
