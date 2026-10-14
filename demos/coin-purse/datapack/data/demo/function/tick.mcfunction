execute as @a[tag=!demo.init] run function demo:init
# Purse Thief bookkeeping (demo only): follow it, remember its coins, drop them as a bag once it is dead
execute as @e[type=husk,tag=demo.thief,limit=1] store result score #thief demo.c run scoreboard players get @s coins
execute as @e[type=husk,tag=demo.thief,limit=1] unless score @s demo.c = @s coins if score @s coins = @s coins run function demo:thief_name
execute as @e[type=marker,tag=demo.thief_pos] run tp @s @e[type=husk,tag=demo.thief,limit=1]
execute unless entity @e[type=husk,tag=demo.thief] if score #thief demo.c matches 1.. at @e[type=marker,tag=demo.thief_pos,limit=1] run function demo:thief_drop
execute if score #t demo.c matches 0 at @e[type=marker,tag=nx.bank_zone] run particle minecraft:happy_villager ~ ~0.2 ~ 1 0 1 0 3
scoreboard players add #t demo.c 1
execute if score #t demo.c matches 10.. run scoreboard players set #t demo.c 0
# menu
execute as @a[scores={demo.cp=1}] run function demo:say {m:"+50 coins",cmd:"scoreboard players add @s coins 50"}
execute as @a[scores={demo.cp=2}] run function demo:say {m:"+300 coins",cmd:"scoreboard players add @s coins 300"}
execute as @a[scores={demo.cp=3}] run function demo:say {m:"Purse emptied",cmd:"scoreboard players set @s coins 0"}
execute if entity @a[scores={demo.cp=4}] run function demo:thief
execute if entity @a[scores={demo.cp=5}] run function demo:say {m:"Mine refilled",cmd:"function demo:mine"}
execute as @a[scores={demo.cp=6}] run function demo:gear
execute as @a[scores={demo.cp=7,coins=1..}] at @s run function nonios:purse/death/drop
execute if entity @a[scores={demo.cp=8}] run function demo:say {m:"Weight 0.1% per coin, max 40% (default)",cmd:"scoreboard players set #w_num nx.purse 1"}
execute if entity @a[scores={demo.cp=9}] run function demo:say {m:"Weight 0.5% per coin, max 40% (exaggerated)",cmd:"scoreboard players set #w_num nx.purse 5"}
execute if entity @a[scores={demo.cp=8..9}] run scoreboard players set @a nx.plast -1
execute as @a[scores={demo.cp=10}] run tellraw @s [{"text":"[demo] Bank: ","color":"green"},{"score":{"name":"@s","objective":"nx.bank"},"color":"yellow"},{"text":" coins (stub, no withdraw yet)","color":"gray"}]
scoreboard players reset @a demo.cp
scoreboard players enable @a demo.cp
