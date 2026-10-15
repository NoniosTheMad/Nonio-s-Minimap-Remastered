$execute unless entity @e[type=marker,tag=nx.core,tag=nx.$(team)] run return run tellraw @s {"text":"[demo] That Nexus is not in play (start a match first).","color":"red"}
$kill @e[type=interaction,tag=nx.shield,tag=nx.$(team)]
$kill @e[type=item_display,tag=nx.shield_fx,tag=nx.$(team)]
$setblock $(x) $(y) $(z) minecraft:air
