# with storage nonios:map area: kill non-player entities, then air-fill two layers per command (fill cap 32768)
$kill @e[type=!player,x=$(x1),y=-64,z=$(z1),dx=$(dx),dy=400,dz=$(dz)]
$scoreboard players set #y nx.tmp $(y1)
$scoreboard players set #y2 nx.tmp $(y2)
function nonios:map/gen/clear_step
