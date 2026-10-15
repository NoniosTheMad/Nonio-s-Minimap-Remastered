# as/at an enemy inside a spawn zone (V2: instant_damage 1 1 every tick; damage immunity makes that one hit per 10 ticks)
effect give @s minecraft:instant_damage 1 1 true
particle minecraft:enchanted_hit ~ ~1 ~ 0.3 0.5 0.3 0.1 12
playsound minecraft:block.respawn_anchor.deplete hostile @a ~ ~ ~ 0.6 1.4
