# roll the core 810 times without placing anything and print the counts (V2 odds x10 = 360/180/90/160/20)
scoreboard players set #c0 demo.tal 0
scoreboard players set #c1 demo.tal 0
scoreboard players set #c2 demo.tal 0
scoreboard players set #c3 demo.tal 0
scoreboard players set #c4 demo.tal 0
scoreboard players set #n demo.tal 810
function demo:sample_step
tellraw @s {"text":"[demo] 810 core rolls:","color":"yellow"}
function demo:sample_line {i:0}
function demo:sample_line {i:1}
function demo:sample_line {i:2}
function demo:sample_line {i:3}
function demo:sample_line {i:4}
