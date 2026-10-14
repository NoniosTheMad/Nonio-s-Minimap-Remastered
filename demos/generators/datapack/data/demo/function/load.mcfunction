scoreboard objectives add demo.gen trigger
scoreboard objectives add demo.c dummy
scoreboard objectives setdisplay sidebar nx.coins
execute unless data storage demo:state {built:1b} run schedule function demo:build 2t
