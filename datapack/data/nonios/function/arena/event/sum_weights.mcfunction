# total event weight -> #wsum (on config apply)
scoreboard players set #wsum nx.arena 0
data modify storage nonios:arena tmp.evs set from storage nonios:arena config.events
function nonios:arena/event/sum_next
