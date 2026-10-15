# as the Berserker, each tick: health may only go down, or up by what berserker/lifesteal granted (nx.cls_bgr).
# Any other gain (food, saturation, regeneration, potions...) is undone by clamping max health to the last allowed
# health (the game clamps health to max) and holding that clamp 3 s, so a slow regen cannot flicker the heart bar.
# No damage: no red flash, no sound. Leaves #mx nx.cls_tmp = unclamped max health (whole points) for the fury bands.
execute store result score #hp nx.cls_tmp run data get entity @s Health 100
execute store result score #mx nx.cls_tmp run attribute @s minecraft:max_health get 100
execute if score @s nx.cls_bcap matches 1.. run function nonios:class/berserker/held
execute unless score @s nx.cls_bhp matches 1.. run scoreboard players operation @s nx.cls_bhp = #hp nx.cls_tmp
execute if score @s nx.cls_bgr matches 1.. run function nonios:class/berserker/granted
execute if score #hp nx.cls_tmp > @s nx.cls_bhp run function nonios:class/berserker/cap
execute if score #hp nx.cls_tmp <= @s nx.cls_bhp run scoreboard players operation @s nx.cls_bhp = #hp nx.cls_tmp
scoreboard players operation #mx nx.cls_tmp /= #100 nx.cls_tmp
