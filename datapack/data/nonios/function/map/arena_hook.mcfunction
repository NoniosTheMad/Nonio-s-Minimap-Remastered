# #nonios:arena/config: once the match map exists, the arena uses its coordinates (demos without the map keep their own)
execute if score #map nx.state matches 1 run function nonios:map/arena_config
