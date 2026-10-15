# recursive: which configured block is in the core now -> tmp.cs.b
execute unless data storage nonios:arena tmp.cbl[0] run return 0
function nonios:arena/core/status_is with storage nonios:arena tmp.cbl[0]
data remove storage nonios:arena tmp.cbl[0]
function nonios:arena/core/status_find
