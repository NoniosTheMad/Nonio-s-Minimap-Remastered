# as the clicker: index = demo.ev - 1 (events_tick fires it)
scoreboard players remove @s demo.ev 1
execute store result storage demo:arena ev.i int 1 run scoreboard players get @s demo.ev
