# as a template's vein seed marker (cell above the host block): becomes a regrowing vein (no forgetting: it belongs to the site)
tag @s remove nx.dream_vseed
tag @s add nx.dream_vein
tag @s add nx.dv3
execute align xyz run tp @s ~0.5 ~ ~0.5
scoreboard players set @s nx.dvt 0
execute at @s run function nonios:dream/vein/grow
