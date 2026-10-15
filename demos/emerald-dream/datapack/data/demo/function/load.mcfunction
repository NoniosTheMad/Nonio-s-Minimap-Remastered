scoreboard objectives add demo.ed trigger
scoreboard objectives add demo.c dummy
scoreboard objectives setdisplay sidebar nx.coins
scoreboard objectives modify nx.coins displayname {"text":"Coins","color":"gold"}
execute unless data storage demo:state {built:1b} run schedule function demo:build 2t
