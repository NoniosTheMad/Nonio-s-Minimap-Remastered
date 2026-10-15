# DEV: build a site of a tier where you stand (in the Dream). Ground sites need an island under you, sky sites open air.
execute unless dimension nonios:emerald_dream run return run tellraw @s {"text":"[demo] enter the Dream first","color":"gray"}
$function nonios:dream/site/demo {tier:$(tier)}
execute if score #res nx.dream matches 1 run tellraw @s {"text":"[demo] site built","color":"yellow"}
execute if score #res nx.dream matches 3 run tellraw @s {"text":"[demo] chunks not loaded yet, try again","color":"gray"}
