# DEV: build a site of tier $(tier) (1 minor 2 major 3 grand 4 nightmare) at the cell point nearest to @s right now
$scoreboard players set #force_tier nx.dream $(tier)
execute align xyz positioned ~ 0 ~ run function nonios:dream/site/new_here
