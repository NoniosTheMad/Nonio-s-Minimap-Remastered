# as the Angel: (re)make its halo, a flat gold ring over its head (angel/tick keeps it there). Text is drawn on
# one side only: one display faces up, one down, so it reads from above and below. (Players cannot be ridden.)
function nonios:class/angel/halo_kill
summon minecraft:text_display ~ ~2.1 ~ {Tags:["nx.ang_halo","nx.ang_new"],text:{text:"◯",color:"#FFD75A"},background:0,shadow:0b,brightness:{sky:15,block:15},billboard:"fixed",teleport_duration:1,transformation:{left_rotation:[-0.7071068f,0f,0f,0.7071068f],right_rotation:[0f,0f,0f,1f],translation:[0f,0f,0.27f],scale:[2.2f,2.2f,2.2f]}}
summon minecraft:text_display ~ ~2.1 ~ {Tags:["nx.ang_halo","nx.ang_new"],text:{text:"◯",color:"#FFD75A"},background:0,shadow:0b,brightness:{sky:15,block:15},billboard:"fixed",teleport_duration:1,transformation:{left_rotation:[0.7071068f,0f,0f,0.7071068f],right_rotation:[0f,0f,0f,1f],translation:[0f,0f,-0.27f],scale:[2.2f,2.2f,2.2f]}}
scoreboard players operation @e[type=text_display,tag=nx.ang_new] nx.pid = @s nx.pid
tag @e[type=text_display,tag=nx.ang_new] remove nx.ang_new
