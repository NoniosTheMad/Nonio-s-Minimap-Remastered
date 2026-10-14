# as + at a generator marker that was right-clicked (clicker tagged nx.gen_clicker).
# Sneak-click, or a click with nothing to collect, opens the upgrade dialog; a plain click collects.
execute if entity @p[tag=nx.gen_clicker,predicate=nonios:dream/sneaking] run return run function nonios:generator/ui/open
execute if score @s nx.gen_pot matches ..0 unless entity @e[type=item,distance=..2] run return run function nonios:generator/ui/open
function nonios:generator/collect
