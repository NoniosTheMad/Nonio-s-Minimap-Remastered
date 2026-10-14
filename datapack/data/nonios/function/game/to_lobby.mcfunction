# end of match (or Stop): everyone back to the lobby, map regenerated (= map reset)
scoreboard players set #state nx.state 0
# dreamers wake up first (lobby_player teleports them), arena paused + neutral
execute as @a[tag=nx.in_dream] run function nonios:dream/force_exit
function nonios:arena/stop
function nonios:arena/reset
bossbar set nonios:phase visible false
bossbar set nonios:barrier_white visible false
bossbar set nonios:barrier_black visible false
kill @e[type=marker,tag=nx.core]
kill @e[type=interaction,tag=nx.shield]
kill @e[type=item_display,tag=nx.shield_fx]
kill @e[type=item_display,tag=nx.wall]
kill @e[type=husk,tag=nx.dummy]
kill @e[type=item,tag=nx.coinbag]
tag @a remove nx.spectator
execute as @a run function nonios:game/lobby_player
function nonios:map/build
tellraw @a [{"text":"Back in the lobby. Teams are kept; ","color":"gray"},{"text":"[Choose team]","color":"green","click_event":{"action":"run_command","command":"/trigger nx.team set 1"}}]
