# as an entity: success (1) if it is inside the Arena box config.bounds, else fail. Use: execute if function nonios:arena/in_bounds
return run function nonios:arena/in_bounds_m with storage nonios:arena config.bounds
