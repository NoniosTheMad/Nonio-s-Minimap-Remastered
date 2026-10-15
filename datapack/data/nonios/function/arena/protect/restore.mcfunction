# macro (prot): put every protected block back, remove the drops of the ones just broken (they are 0 ticks old), and
# cancel the mining stat of the coin blocks among them (protect_types) so the purse pays nothing for them.
$clone $(x1) $(by) $(z1) $(x2) $(by2) $(z2) $(x1) $(y1) $(z1) masked
$kill @e[type=item,x=$(x1),y=$(y1),z=$(z1),dx=$(dx),dy=$(dy),dz=$(dz),nbt={Age:0s}]
data modify storage nonios:arena tmp.pt set from storage nonios:arena config.protect_types
function nonios:arena/protect/cancel_next
scoreboard players add #restores nx.arena 1
