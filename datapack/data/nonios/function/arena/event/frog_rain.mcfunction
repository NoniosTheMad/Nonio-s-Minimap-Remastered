# EVENT (as + at a node): frogs full of emeralds rain down; one is the Cracy Frog (glowing, big loot).
# Frogs not killed within frog_life ticks vanish (no loot).
scoreboard players operation #left nx.arena = #frogs nx.arena
execute if score #left nx.arena matches 1.. run function nonios:arena/event/frog_one
summon minecraft:frog ~ ~10 ~ {Tags:["nx.ev_frog","nx.ev_frog_new"],variant:"minecraft:warm",Glowing:1b,CustomName:{text:"Cracy Frog",color:"gold",bold:true},CustomNameVisible:1b,PersistenceRequired:1b,DeathLootTable:"nonios:arena/cracy_frog",active_effects:[{id:"minecraft:slow_falling",duration:200,amplifier:0b,show_particles:0b}]}
execute as @e[type=frog,tag=nx.ev_frog_new] run function nonios:arena/event/fling_frog
particle minecraft:item_slime ~ ~9 ~ 2 1 2 0 60
playsound minecraft:entity.frog.ambient master @a ~ ~ ~ 3 0.7
scoreboard players operation #frog_t nx.arena = #frog_life nx.arena
