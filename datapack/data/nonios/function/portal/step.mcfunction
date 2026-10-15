# as + at a player who just stepped onto a portal frame
tag @s add nx.on_pad
execute unless entity @e[type=marker,tag=nx.dream_pad,distance=..2] run return 0
execute unless score #state nx.state matches 1..2 run return run title @s actionbar {"text":"The portal is dormant","color":"dark_green"}
execute if entity @s[team=] run return 0
execute if entity @s[team=white] unless entity @e[type=marker,tag=nx.dream_pad,tag=nx.white,distance=..2] run return run title @s actionbar {"text":"Enemy portal","color":"red"}
execute if entity @s[team=black] unless entity @e[type=marker,tag=nx.dream_pad,tag=nx.black,distance=..2] run return run title @s actionbar {"text":"Enemy portal","color":"red"}
# open: straight in. Locked: offer the unlock.
execute if entity @s[team=white] if score #white nx.portal matches 1 run return run function nonios:dream/try_enter
execute if entity @s[team=black] if score #black nx.portal matches 1 run return run function nonios:dream/try_enter
function nonios:portal/offer
