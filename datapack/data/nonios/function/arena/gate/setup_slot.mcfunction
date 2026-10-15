# recursive over tmp.sl: one slot each (marker at the exit; nx.ar_slot = its number, 1..)
execute unless data storage nonios:arena tmp.sl[0] run return 0
function nonios:arena/gate/spawn_slot with storage nonios:arena tmp.sl[0].exit
data remove storage nonios:arena tmp.sl[0]
function nonios:arena/gate/setup_slot
