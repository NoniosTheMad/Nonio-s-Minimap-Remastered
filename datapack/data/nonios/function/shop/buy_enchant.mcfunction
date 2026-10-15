# enchant the main-hand item (V2: /enchant). Vanilla rules decide: wrong item, conflicting or already present = refused, nothing taken.
$execute store success score #ok nx.tmp run enchant @s $(ench) $(lvl)
execute if score #ok nx.tmp matches 0 run return run function nonios:shop/msg_noench with storage nonios:shop sel
scoreboard players operation @s nx.coins -= #p nx.tmp
playsound minecraft:block.enchantment_table.use master @s ~ ~ ~ 1 1
function nonios:shop/paid
