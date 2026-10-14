forceload add -16 -16 16 16
fill -14 63 -14 14 63 14 minecraft:smooth_stone
fill -3 63 -11 3 63 -5 minecraft:white_concrete
fill -3 64 -11 3 66 -11 minecraft:white_stained_glass
function nonios:nexus/spawn {team:"white",x:0,y:64,z:-8}
data modify storage demo:state built set value 1b
