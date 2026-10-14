# storage nonios:map arena_cfg -> storage nonios:arena config: capture nodes, Lightning Rabbit box and spawn.
# map/build runs this before arena/setup; on every load #nonios:arena/config runs map/arena_hook (keeps it after /reload).
data modify storage nonios:arena config.nodes set from storage nonios:map arena_cfg.nodes
data modify storage nonios:arena config.bounds set from storage nonios:map arena_cfg.bounds
data modify storage nonios:arena config.center set from storage nonios:map arena_cfg.center
