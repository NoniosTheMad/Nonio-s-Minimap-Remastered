scoreboard objectives add demo.nx trigger
execute unless data storage demo:state {built:1b} run schedule function demo:build 2t
