# rebuild this player's post-effect stack in a fixed order: look -> colour -> lines -> distortion
posteffect clear @s
execute if score @s demo.look matches 1 run posteffect add @s nonios:reaper
execute if score @s demo.look matches 2 run posteffect add @s nonios:cinematic
execute if score @s demo.look matches 3 run posteffect add @s nonios:thermal
execute if score @s demo.look matches 4 run posteffect add @s nonios:cosmic
execute if score @s demo.look matches 5 run posteffect add @s nonios:monster
execute if score @s demo.col matches 11 run posteffect add @s nonios:rainbow
execute if score @s demo.col matches 12 run posteffect add @s nonios:comic
execute if score @s demo.line matches 21 run posteffect add @s nonios:ink
execute if score @s demo.line matches 22 run posteffect add @s nonios:neon
execute if score @s demo.dist matches 31 run posteffect add @s nonios:acid
function demo:fx/status
