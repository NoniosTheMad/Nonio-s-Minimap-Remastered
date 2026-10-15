# every 10 ticks: nobody keeps Dream gifts outside the Dream (death drops picked up, ender chest, logout...)
execute as @a[tag=!nx.in_dream] if items entity @s container.* *[minecraft:custom_data~{nx_dw:1b}] run function nonios:dream/wings/strip
execute as @a[tag=!nx.in_dream] if items entity @s armor.* *[minecraft:custom_data~{nx_dw:1b}] run function nonios:dream/wings/strip
execute as @a[tag=!nx.in_dream] if items entity @s weapon.offhand *[minecraft:custom_data~{nx_dw:1b}] run function nonios:dream/wings/strip
execute as @a[tag=!nx.in_dream] if items entity @s player.cursor *[minecraft:custom_data~{nx_dw:1b}] run function nonios:dream/wings/strip
execute as @a[tag=!nx.in_dream] if items entity @s enderchest.* *[minecraft:custom_data~{nx_dw:1b}] run function nonios:dream/wings/strip
execute as @a[tag=!nx.in_dream] if items entity @s container.* *[minecraft:custom_data~{nx_dg:1b}] run function nonios:dream/wings/strip
execute as @a[tag=!nx.in_dream] if items entity @s armor.* *[minecraft:custom_data~{nx_dg:1b}] run function nonios:dream/wings/strip
execute as @a[tag=!nx.in_dream] if items entity @s weapon.offhand *[minecraft:custom_data~{nx_dg:1b}] run function nonios:dream/wings/strip
execute as @a[tag=!nx.in_dream] if items entity @s player.cursor *[minecraft:custom_data~{nx_dg:1b}] run function nonios:dream/wings/strip
execute as @a[tag=!nx.in_dream] if items entity @s enderchest.* *[minecraft:custom_data~{nx_dg:1b}] run function nonios:dream/wings/strip
execute as @a[tag=!nx.in_dream] if items entity @s container.* *[minecraft:custom_data~{nx_dwings:1b}] run function nonios:dream/wings/strip
execute as @a[tag=!nx.in_dream] if items entity @s armor.* *[minecraft:custom_data~{nx_dwings:1b}] run function nonios:dream/wings/strip
execute as @a[tag=!nx.in_dream] if items entity @s weapon.offhand *[minecraft:custom_data~{nx_dwings:1b}] run function nonios:dream/wings/strip
execute as @a[tag=!nx.in_dream] if items entity @s player.cursor *[minecraft:custom_data~{nx_dwings:1b}] run function nonios:dream/wings/strip
execute as @a[tag=!nx.in_dream] if items entity @s enderchest.* *[minecraft:custom_data~{nx_dwings:1b}] run function nonios:dream/wings/strip
