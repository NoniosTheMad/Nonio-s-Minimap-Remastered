execute as @a[tag=!demo.init] run function demo:init
execute as @a[scores={demo.nx=1}] run function demo:join {team:"black"}
execute as @a[scores={demo.nx=2}] run function demo:join {team:"white"}
execute if entity @a[scores={demo.nx=3}] run function nonios:nexus/spawn {team:"white",x:0,y:64,z:-8}
execute if entity @a[scores={demo.nx=4}] run function demo:say {m:"Regen x1",cmd:"scoreboard players set #regen_mult nx.const 1"}
execute if entity @a[scores={demo.nx=5}] run function demo:say {m:"Regen x20",cmd:"scoreboard players set #regen_mult nx.const 20"}
execute if entity @a[scores={demo.nx=6}] run function demo:say {m:"Max HP 1000 (applies on Reset)",cmd:"scoreboard players set #barrier_max nx.const 1000"}
execute if entity @a[scores={demo.nx=7}] run function demo:say {m:"Max HP 200 (applies on Reset)",cmd:"scoreboard players set #barrier_max nx.const 200"}
execute as @a[scores={demo.nx=8}] run function demo:gear
scoreboard players reset @a demo.nx
scoreboard players enable @a demo.nx
