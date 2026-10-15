# as/at a player the tongue caught in mid-air (2+ blocks of air below): dragged DOWN instead of yanked up (#136 grappling
# hook). Off any mount, a wind burst just above the head, heavier gravity and no lift (slow falling, levitation, Reaper
# flight) until they land, then a fixed 2-heart thud (yank_land). Vanilla fall damage is off meanwhile: it stays minor.
ride @s dismount
effect clear @s minecraft:levitation
effect clear @s minecraft:slow_falling
summon minecraft:wind_charge ~ ~2.3 ~ {Motion:[0.0,-1.0,0.0],Tags:["nx.frog_wc"]}
attribute @s minecraft:gravity modifier add nonios:frog_hook 0.08 add_value
attribute @s minecraft:fall_damage_multiplier modifier add nonios:frog_hook -1 add_value
tag @s add nx.frog_hooked
function nonios:class/cracy_frog/yank_track
playsound minecraft:entity.frog.eat player @a ~ ~ ~ 2 0.5
playsound minecraft:entity.fishing_bobber.retrieve player @a ~ ~ ~ 2 0.6
particle minecraft:item_slime ~ ~1 ~ 0.4 0.6 0.4 0.1 20
title @s actionbar {"text":"#Grounded","color":"green","italic":true}
