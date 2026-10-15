# every tick (economy/tick): the bank zones = a 5x5 footprint around each vault (gold floor, map/gen/bank), from the floor
# up to 4 blocks above it (marker nx.bank_zone sits on the floor at the vault). Presence, not blocks: walking, jumping or
# flying through counts. Entering fires once (tag nx.bk.on until you leave), so standing there to withdraw never re-deposits.
tag @a remove nx.bk.in
execute as @e[type=marker,tag=nx.bank_zone] at @s positioned ~-2.5 ~ ~-2.5 run tag @a[dx=4,dy=3,dz=4,gamemode=!spectator] add nx.bk.in
tag @a[tag=nx.bk.on,tag=!nx.bk.in] remove nx.bk.on
execute as @a[tag=nx.bk.in,tag=!nx.bk.on] at @s run function nonios:bank/zone/enter
# ambient glint over the gold floor, once a second
execute if score #es nx.eco matches 0 as @e[type=marker,tag=nx.bank_zone] at @s run particle minecraft:wax_on ~ ~0.15 ~ 1.4 0 1.4 0 3 normal @a
