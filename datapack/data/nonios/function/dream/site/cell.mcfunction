# cell (#cx0+#dx, #cz0+#dz): its site point and tier come from an LCG hash of the cell and the world's #seed
scoreboard players operation #cx nx.dream = #cx0 nx.dream
scoreboard players operation #cx nx.dream += #dx nx.dream
scoreboard players operation #cz nx.dream = #cz0 nx.dream
scoreboard players operation #cz nx.dream += #dz nx.dream
scoreboard players operation #h nx.dream = #cx nx.dream
scoreboard players operation #h nx.dream *= #k1 nx.dream
scoreboard players operation #hz nx.dream = #cz nx.dream
scoreboard players operation #hz nx.dream *= #k2 nx.dream
scoreboard players operation #h nx.dream += #hz nx.dream
scoreboard players operation #h nx.dream += #seed nx.dream
function nonios:dream/site/lcg
scoreboard players operation #ox nx.dream = #hv nx.dream
scoreboard players operation #ox nx.dream %= #sspan nx.dream
function nonios:dream/site/lcg
scoreboard players operation #oz nx.dream = #hv nx.dream
scoreboard players operation #oz nx.dream %= #sspan nx.dream
# site point = cell corner + margin + offset
scoreboard players operation #sx nx.dream = #cx nx.dream
scoreboard players operation #sx nx.dream *= #cell nx.dream
scoreboard players operation #sx nx.dream += #margin nx.dream
scoreboard players operation #sx nx.dream += #ox nx.dream
scoreboard players operation #sz nx.dream = #cz nx.dream
scoreboard players operation #sz nx.dream *= #cell nx.dream
scoreboard players operation #sz nx.dream += #margin nx.dream
scoreboard players operation #sz nx.dream += #oz nx.dream
# close enough?
scoreboard players operation #ddx nx.dream = #sx nx.dream
scoreboard players operation #ddx nx.dream -= #px nx.dream
scoreboard players operation #ddx nx.dream *= #ddx nx.dream
scoreboard players operation #ddz nx.dream = #sz nx.dream
scoreboard players operation #ddz nx.dream -= #pz nx.dream
scoreboard players operation #ddz nx.dream *= #ddz nx.dream
scoreboard players operation #ddx nx.dream += #ddz nx.dream
execute if score #ddx nx.dream > #reach2 nx.dream run return 0
function nonios:dream/site/lcg
scoreboard players operation #tr nx.dream = #hv nx.dream
scoreboard players operation #tr nx.dream %= #100 nx.dream
function nonios:dream/site/lcg
scoreboard players operation #pick nx.dream = #hv nx.dream
execute store result storage nonios:dream site.x int 1 run scoreboard players get #sx nx.dream
execute store result storage nonios:dream site.z int 1 run scoreboard players get #sz nx.dream
function nonios:dream/site/at with storage nonios:dream site
