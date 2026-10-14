execute as @a[tag=!demo.init] run function demo:init
# G menu (demo:generators dialog) -> trigger demo.gen
execute as @a[scores={demo.gen=1}] at @s run function demo:near {fn:"upgrade"}
execute as @a[scores={demo.gen=2}] at @s run function demo:near {fn:"downgrade"}
execute if entity @a[scores={demo.gen=3}] as @e[type=marker,tag=nx.gen] at @s run function nonios:generator/reset
execute if entity @a[scores={demo.gen=3}] run function demo:say {m:"All generators reset to Lv 1 (pot emptied)"}
execute as @a[scores={demo.gen=4}] at @s run function nonios:generator/buy_upgrade
execute if entity @a[scores={demo.gen=5}] run scoreboard players set #speed nx.gen 10
execute if entity @a[scores={demo.gen=5}] run function demo:say {m:"Time x10: a drop every 1-2 s"}
execute if entity @a[scores={demo.gen=6}] run scoreboard players set #speed nx.gen 1
execute if entity @a[scores={demo.gen=6}] run function demo:say {m:"Time x1 (Lv1 10s, Lv2 8s, Lv3 6s)"}
execute as @a[scores={demo.gen=7}] run scoreboard players add @s nx.coins 100
execute as @a[scores={demo.gen=8}] run scoreboard players set @s nx.coins 0
execute if entity @a[scores={demo.gen=9}] run function demo:sim
execute if entity @a[scores={demo.gen=10}] as @e[type=marker,tag=nx.gen] run scoreboard players set @s nx.gen_t 1
execute as @a[scores={demo.gen=11}] run function demo:status
execute if entity @a[scores={demo.gen=12}] run function demo:build
execute if entity @a[scores={demo.gen=12}] run function demo:say {m:"Demo rebuilt"}
scoreboard players reset @a[scores={demo.gen=1..}] demo.gen
scoreboard players enable @a demo.gen
