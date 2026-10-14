# (Re)build the regrowing core block from storage nonios:arena config.core {x,y,z} (no core when absent). arena/setup runs this.
kill @e[type=marker,tag=nx.acore]
scoreboard players set #core nx.arena 0
execute unless data storage nonios:arena config.core.x run return 0
function nonios:arena/core/spawn with storage nonios:arena config.core
