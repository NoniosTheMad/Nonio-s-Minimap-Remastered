execute unless data storage nonios:arena tmp.pt[0] run return 0
data modify storage nonios:arena prot.t set from storage nonios:arena tmp.pt[0]
function nonios:arena/protect/cancel with storage nonios:arena prot
data remove storage nonios:arena tmp.pt[0]
function nonios:arena/protect/cancel_next
