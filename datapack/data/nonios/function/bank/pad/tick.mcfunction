# every tick (economy/tick): the bank pads (gold pressure plates around each vault, map/gen/bank). Deposit on contact:
# stepping onto a plate fires once (tag nx.bk.on until you step off), so standing there to withdraw never re-deposits.
execute as @a[tag=nx.bk.on] at @s unless block ~ ~ ~ minecraft:light_weighted_pressure_plate run tag @s remove nx.bk.on
execute as @a[tag=!nx.bk.on,gamemode=!spectator] at @s if block ~ ~ ~ minecraft:light_weighted_pressure_plate if entity @e[type=marker,tag=nx.bank_zone,distance=..2.6] run function nonios:bank/pad/enter
