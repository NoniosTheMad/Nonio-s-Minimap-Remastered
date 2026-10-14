# storage nonios:map arena_cfg (+ <team>.agate) -> storage nonios:arena config: capture nodes, Lightning Rabbit box and spawn,
# random-entry gate slots + pads, regrowing core.
# map/build runs this before arena/setup; on every load #nonios:arena/config runs map/arena_hook (keeps it after /reload).
data modify storage nonios:arena config.nodes set from storage nonios:map arena_cfg.nodes
data modify storage nonios:arena config.bounds set from storage nonios:map arena_cfg.bounds
data modify storage nonios:arena config.center set from storage nonios:map arena_cfg.center
# random-entry gates: one pad per field (<team>.agate) + the arena's slots; regrowing core
data modify storage nonios:arena config.gates set value []
data modify storage nonios:arena config.gates append from storage nonios:map white.agate
data modify storage nonios:arena config.gates append from storage nonios:map black.agate
data modify storage nonios:arena config.slots set from storage nonios:map arena_cfg.slots
data modify storage nonios:arena config.core set from storage nonios:map arena_cfg.core
