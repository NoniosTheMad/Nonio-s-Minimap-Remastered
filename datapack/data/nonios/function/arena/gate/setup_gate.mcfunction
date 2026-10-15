# recursive over tmp.gl: one entry pad each
execute unless data storage nonios:arena tmp.gl[0] run return 0
function nonios:arena/gate/spawn_gate with storage nonios:arena tmp.gl[0]
data remove storage nonios:arena tmp.gl[0]
function nonios:arena/gate/setup_gate
