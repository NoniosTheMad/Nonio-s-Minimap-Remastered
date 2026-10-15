# enchantment nonios:class/monster_hunger (tick, 30%): the V2 red dust, seen by everyone but the Monster itself
tag @s add nx.cls_pself
particle minecraft:dust{color:[0.6,0.0,0.0],scale:1.0} ~ ~1 ~ 0.15 0.5 0.15 0 2 normal @a[tag=!nx.cls_pself]
tag @s remove nx.cls_pself
