# per-match reset of the M4 systems (game/start; the map rebuild on to_lobby recreates them anyway):
# generators back to Lv1 with empty pots and no drops lying around, arena paused + neutral, both Dream portals locked.
execute as @e[type=marker,tag=nx.gen] at @s run kill @e[type=item,distance=..3]
execute as @e[type=marker,tag=nx.gen] at @s run function nonios:generator/reset
function nonios:arena/stop
function nonios:arena/reset
function nonios:portal/reset
