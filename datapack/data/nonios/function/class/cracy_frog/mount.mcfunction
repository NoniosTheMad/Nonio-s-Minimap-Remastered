# as/at the frog: summon the broom (#136) - an invisible quarter-size happy ghast in a harness (vanilla's only flying mount a
# player steers: look + WASD, jump climbs, sneak hops off) with a broom display under the rider. One per frog (nx.pid).
function nonios:dream/pid
scoreboard players operation #me nx.cls_tmp = @s nx.pid
function nonios:class/cracy_frog/mount_kill
summon minecraft:happy_ghast ~ ~ ~ {Tags:["nx.frog_mount","nx.new"],Invulnerable:1b,Silent:1b,PersistenceRequired:1b,active_effects:[{id:"minecraft:invisibility",duration:-1,amplifier:0,show_particles:0b}],equipment:{body:{id:"minecraft:purple_harness",count:1}},drop_chances:{body:0.0f},attributes:[{id:"minecraft:scale",base:0.25d},{id:"minecraft:flying_speed",base:0.11d}]}
summon minecraft:item_display ~ ~ ~ {Tags:["nx.frog_broomfx","nx.new"],teleport_duration:1,item:{id:"minecraft:brush",count:1},item_display:"fixed",transformation:{left_rotation:[0f,0.7071f,0f,0.7071f],right_rotation:[0f,0f,0.3827f,0.9239f],translation:[0f,0f,0f],scale:[1.6f,1.6f,1.6f]}}
scoreboard players operation @e[tag=nx.new] nx.pid = #me nx.cls_tmp
ride @s mount @e[type=happy_ghast,tag=nx.new,limit=1]
tag @e[tag=nx.new] remove nx.new
scoreboard players set @s nx.cls_fly 1
effect clear @s minecraft:slow_falling
playsound minecraft:entity.phantom.flap player @a ~ ~ ~ 1 1.4
particle minecraft:witch ~ ~0.5 ~ 0.4 0.2 0.4 0 12
