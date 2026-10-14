scoreboard objectives add demo.cp trigger
scoreboard objectives add demo.c dummy
execute unless data storage demo:state {built:1b} run schedule function demo:build 2t
