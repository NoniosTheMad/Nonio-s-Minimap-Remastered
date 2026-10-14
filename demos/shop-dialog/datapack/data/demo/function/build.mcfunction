forceload add -16 -16 16 16
fill -8 63 -8 8 63 8 minecraft:smooth_stone
fill -2 63 -6 2 63 -3 minecraft:spruce_planks
fill -2 64 -6 2 66 -6 minecraft:spruce_planks
setblock -2 64 -3 minecraft:barrel[facing=up]
setblock 2 64 -3 minecraft:barrel[facing=up]
function nonios:shop/spawn_npc {x:0.5,y:64,z:-3.5,yaw:0}
scoreboard objectives setdisplay sidebar nx.coins
data modify storage demo:state built set value 1b
