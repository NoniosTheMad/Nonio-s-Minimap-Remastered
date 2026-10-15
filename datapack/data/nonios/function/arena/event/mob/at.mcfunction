# macro {x, y, z}: a temporary marker nx.ev_at there (spawn point for the summons; event/mob/spread removes it)
kill @e[type=marker,tag=nx.ev_at]
$summon minecraft:marker $(x) $(y) $(z) {Tags:["nx.ev_at"]}
