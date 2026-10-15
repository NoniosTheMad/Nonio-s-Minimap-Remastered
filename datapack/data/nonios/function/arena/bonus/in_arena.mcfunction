# macro {team, effect}: that effect (level I, 3 s, refreshed every second) to the team inside the Arena bounds
$data modify storage nonios:arena bfx set value {team:"$(team)",effect:"$(effect)"}
data modify storage nonios:arena bfx merge from storage nonios:arena config.bounds
function nonios:arena/bonus/in_arena_m with storage nonios:arena bfx
