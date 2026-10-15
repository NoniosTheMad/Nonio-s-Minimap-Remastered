# macro {lvl}: the core grows to ccore.l<lvl> (src/generators.json levels.core_scale)
$data modify storage nonios:arena cg.s set from storage nonios:gen ccore.l$(lvl)
execute as @e[type=item_display,tag=nx.cgen_core,distance=..3,limit=1] run function nonios:arena/cgen/level_s
