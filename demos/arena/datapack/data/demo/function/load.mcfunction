scoreboard objectives add demo.arena trigger
scoreboard objectives add demo.c dummy
team add white {text:"White",color:"white"}
team modify white color white
team add black {text:"Black",color:"dark_purple"}
team modify black color dark_purple
gamerule spawn_mobs false
gamerule advance_time false
gamerule keep_inventory true
time set 6000
weather clear
execute unless data storage demo:arena {built:1b} run schedule function demo:build 2t
schedule function demo:second 20t replace
