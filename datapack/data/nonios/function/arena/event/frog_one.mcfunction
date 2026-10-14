summon minecraft:frog ~ ~9 ~ {Tags:["nx.ev_frog","nx.ev_frog_new"],PersistenceRequired:1b,DeathLootTable:"nonios:arena/frog",active_effects:[{id:"minecraft:slow_falling",duration:200,amplifier:0b,show_particles:0b}]}
scoreboard players remove #left nx.arena 1
execute if score #left nx.arena matches 1.. run function nonios:arena/event/frog_one
