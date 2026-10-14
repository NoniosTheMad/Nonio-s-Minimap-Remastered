# as + at a node marker, once a second: hologram, indicator block (put back if someone broke it), owner-coloured particles
function nonios:arena/node/holo
execute if score #indicator nx.arena matches 1 run function nonios:arena/node/indicator
execute if score @s nx.ar_own matches 1 run particle minecraft:dust{color:[1.0,1.0,1.0],scale:1.5} ~ ~0.6 ~ 0.15 0.5 0.15 0 6
execute if score @s nx.ar_own matches 2 run particle minecraft:dust{color:[0.6,0.2,0.9],scale:1.5} ~ ~0.6 ~ 0.15 0.5 0.15 0 6
execute if score #st nx.arena matches 3 run particle minecraft:angry_villager ~ ~1.5 ~ 0.6 0.3 0.6 0 2
