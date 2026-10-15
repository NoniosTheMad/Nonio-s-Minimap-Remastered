$summon minecraft:marker ~ ~ ~ {Tags:["nx.gen","nx.gen.$(team)","nx.gen_new"],data:{team:"$(team)",lvl:$(lvl)}}
# one interaction over the 3x3 base (sea lantern + glass + bedrock): right-click = upgrade dialog, and it takes
# the hits so the base can't be mined. The outcome block on top stays minable.
summon minecraft:interaction ~ ~-2 ~ {Tags:["nx.gen_part","nx.gen_click"],width:3.02f,height:2f,response:1b}
execute as @e[type=marker,tag=nx.gen_new,distance=..0.1,limit=1] at @s run function nonios:generator/init
