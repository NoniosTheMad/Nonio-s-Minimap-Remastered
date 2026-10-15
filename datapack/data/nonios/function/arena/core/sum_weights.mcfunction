# total core weight -> #cwsum (on config apply)
scoreboard players set #cwsum nx.arena 0
data modify storage nonios:arena tmp.cbl set from storage nonios:arena config.core_blocks
function nonios:arena/core/sum_next
