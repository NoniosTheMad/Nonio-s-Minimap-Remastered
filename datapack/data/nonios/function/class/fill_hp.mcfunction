# as a player whose class just raised its max health: full health in 2 ticks (equipment attributes apply on the next tick)
tag @s add nx.cls_fill
schedule function nonios:class/fill_hp_now 2t replace
