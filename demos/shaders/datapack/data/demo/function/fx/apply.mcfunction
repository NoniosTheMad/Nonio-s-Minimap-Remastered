# rebuild this player's post-effect stack in a fixed order: look -> colour -> lines -> distortion
posteffect clear @s
execute if score @s demo.look matches 1 run posteffect add @s nonios:reaper
execute if score @s demo.look matches 2 run posteffect add @s nonios:cinematic
execute if score @s demo.look matches 3 run posteffect add @s nonios:thermal
execute if score @s demo.look matches 4 run posteffect add @s nonios:cosmic
execute if score @s demo.look matches 5 run posteffect add @s nonios:monster
execute if score @s demo.look matches 6 run posteffect add @s nonios:angel
execute if score @s demo.look matches 7 run posteffect add @s nonios:neon
execute if score @s demo.look matches 8 run posteffect add @s nonios:alien
# Monster madness (level 1..10, eased toward the HP target) sits right on top of the look
execute if score @s demo.look matches 5 if score @s demo.mad matches 1 run posteffect add @s nonios:madness_1
execute if score @s demo.look matches 5 if score @s demo.mad matches 2 run posteffect add @s nonios:madness_2
execute if score @s demo.look matches 5 if score @s demo.mad matches 3 run posteffect add @s nonios:madness_3
execute if score @s demo.look matches 5 if score @s demo.mad matches 4 run posteffect add @s nonios:madness_4
execute if score @s demo.look matches 5 if score @s demo.mad matches 5 run posteffect add @s nonios:madness_5
execute if score @s demo.look matches 5 if score @s demo.mad matches 6 run posteffect add @s nonios:madness_6
execute if score @s demo.look matches 5 if score @s demo.mad matches 7 run posteffect add @s nonios:madness_7
execute if score @s demo.look matches 5 if score @s demo.mad matches 8 run posteffect add @s nonios:madness_8
execute if score @s demo.look matches 5 if score @s demo.mad matches 9 run posteffect add @s nonios:madness_9
execute if score @s demo.look matches 5 if score @s demo.mad matches 10 run posteffect add @s nonios:madness_10
execute if score @s demo.col matches 11 run posteffect add @s nonios:rainbow
execute if score @s demo.col matches 12 run posteffect add @s nonios:comic
execute if score @s demo.line matches 21 run posteffect add @s nonios:ink
execute if score @s demo.line matches 22 run posteffect add @s nonios:fluorescent
execute if score @s demo.dist matches 31 run posteffect add @s nonios:wobble
execute if score @s demo.planet matches 36 run posteffect add @s nonios:planet
# Acid world warp: night_vision is the per-player switch read by the overlay core shaders
execute if score @s demo.warp matches 35 run effect give @s minecraft:night_vision infinite 0 true
execute unless score @s demo.warp matches 35 run effect clear @s minecraft:night_vision
function demo:fx/status
