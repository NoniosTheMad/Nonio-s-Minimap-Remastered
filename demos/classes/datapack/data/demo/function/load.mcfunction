scoreboard objectives add demo.cls trigger
scoreboard objectives add demo.died deathCount
gamerule keep_inventory true
gamerule immediate_respawn true
execute unless data storage demo:state {built:1b} run schedule function demo:build 2t
