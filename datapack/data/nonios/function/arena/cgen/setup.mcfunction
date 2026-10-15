# (Re)build the centre generator from config.cgen {x,y,z} (no config.cgen = none). arena/setup runs this.
kill @e[tag=nx.cgen_part]
scoreboard players set #cgen nx.arena 0
execute unless data storage nonios:arena config.cgen.x run return 0
function nonios:arena/cgen/spawn with storage nonios:arena config.cgen
