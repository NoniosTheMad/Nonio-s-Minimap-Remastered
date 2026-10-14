# macro $(team), $(lvl), $(glow). Structure origin = 3x3 base corner, two blocks below the marker.
$place template nonios:generator/$(team)_lvl$(lvl) ~-1 ~-2 ~-1
$execute as @e[type=item_display,tag=nx.gen_core,distance=..2.5,limit=1] run data modify entity @s item.id set from storage nonios:gen core.l$(lvl)
$execute if score @s nx.gen_lvl matches 3 as @e[type=item_display,tag=nx.gen_core,distance=..2.5,limit=1] run data merge entity @s {Glowing:1b,glow_color_override:$(glow)}
