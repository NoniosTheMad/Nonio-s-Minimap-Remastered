# as the site marker at the site point, right after place template (storage nonios:dream site.placed {name,tier,r})
tag @s remove nx.dream_site_new
tag @s add nx.dream_site
function nonios:dream/site/placed_m with storage nonios:dream site.placed
playsound minecraft:block.amethyst_block.resonate ambient @a ~ ~ ~ 3 0.6
