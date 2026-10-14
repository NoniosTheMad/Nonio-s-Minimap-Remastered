# HOOK (M2 game/death): as a player who died. Self-contained, safe on anyone, any number of times.
# Shop class: lost for good (buy it again). Basic class: items/vision removed now, re-applied by class/on_respawn.
# Works with keep_inventory on or off (class items carry curse of vanishing, so they never drop).
scoreboard players set #shop nx.cls_tmp 0
execute if score @s nx.class matches 1.. store result score #shop nx.cls_tmp run function nonios:class/gen/is_shop
execute if score #shop nx.cls_tmp matches 1 run function nonios:class/gen/lost
function nonios:class/strip
