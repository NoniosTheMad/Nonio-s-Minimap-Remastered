scoreboard objectives add demo.fx trigger
scoreboard objectives add demo.left minecraft.custom:minecraft.leave_game
scoreboard objectives add demo.st dummy
scoreboard objectives add demo.look dummy
scoreboard objectives add demo.col dummy
scoreboard objectives add demo.line dummy
scoreboard objectives add demo.dist dummy
scoreboard objectives add demo.hp dummy
scoreboard objectives add demo.abs dummy
scoreboard objectives add demo.max dummy
scoreboard objectives add demo.tot dummy
scoreboard objectives add demo.pct dummy
scoreboard players set #100 demo.st 100
team add demo.hp1
team modify demo.hp1 color red
team add demo.hp2
team modify demo.hp2 color gold
team add demo.hp3
team modify demo.hp3 color green
team add demo.hp4
team modify demo.hp4 color light_purple
team add demo.hp5
team modify demo.hp5 color aqua
function demo:rules
forceload add -21 -9 21 43
schedule function demo:ensure 40t
