scoreboard objectives add demo.shop trigger
execute unless data storage demo:state {built:1b} run schedule function demo:build 2t
