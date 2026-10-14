execute as @a[tag=!demo.init] run function demo:init
execute as @a at @s if dimension minecraft:overworld if block ~ ~-0.3 ~ minecraft:end_portal_frame unless entity @s[tag=demo.portal_cd] run function demo:portal
execute as @a[tag=demo.portal_cd] at @s if dimension minecraft:overworld unless block ~ ~-0.3 ~ minecraft:end_portal_frame run tag @s remove demo.portal_cd
execute as @a run function demo:coins
execute if score #t demo.c matches 0 run particle minecraft:portal 6.5 64.2 0.5 0.4 0.3 0.4 0.3 6
execute if score #t demo.c matches 0 run particle minecraft:happy_villager 6.5 64.5 0.5 0.6 0.4 0.6 0 1
scoreboard players add #t demo.c 1
execute if score #t demo.c matches 4.. run scoreboard players set #t demo.c 0
# menu
execute as @a[scores={demo.ed=1}] at @s run function nonios:dream/try_enter
execute as @a[scores={demo.ed=2}] at @s run function nonios:dream/force_exit
execute as @a[scores={demo.ed=3}] run function demo:say {m:"All loaded veins regrown",cmd:"function nonios:dream/reset_veins"}
execute as @a[scores={demo.ed=4}] run function demo:say {m:"Wake-up channel: 2 s",cmd:"scoreboard players set #channel_ticks nx.dream 40"}
execute as @a[scores={demo.ed=5}] run function demo:say {m:"Wake-up channel: 5 s (default)",cmd:"scoreboard players set #channel_ticks nx.dream 100"}
execute as @a[scores={demo.ed=6}] run function demo:say {m:"Wake-up channel: 10 s",cmd:"scoreboard players set #channel_ticks nx.dream 200"}
execute as @a[scores={demo.ed=7}] run function demo:say {m:"Wake-up channel: 15 s",cmd:"scoreboard players set #channel_ticks nx.dream 300"}
execute as @a[scores={demo.ed=8}] run function demo:say {m:"Veins regrow after 10 s",cmd:"scoreboard players set #regrow_ticks nx.dream 200"}
execute as @a[scores={demo.ed=9}] run function demo:say {m:"Veins regrow after 30 s (default)",cmd:"scoreboard players set #regrow_ticks nx.dream 600"}
execute as @a[scores={demo.ed=10}] at @s run function demo:say {m:"Ouch (1 heart). Sneak-channel cancelled if it was running.",cmd:"damage @s 2 minecraft:magic"}
execute as @a[scores={demo.ed=11}] run function demo:cfg
execute as @a[scores={demo.ed=12}] run function demo:say {m:"Gear given",cmd:"function demo:gear"}
execute as @a[scores={demo.ed=13}] run function demo:say {m:"Coins reset to 0",cmd:"scoreboard players set @s nx.coins 0"}
scoreboard players reset @a demo.ed
scoreboard players enable @a demo.ed
