# as/at a climbing Balrog (from tick): keep rising while it pushes into the wall face; else let go
execute unless predicate nonios:class/input_forward run return run function nonios:class/balrog/unclimb
execute rotated ~ 0 positioned ^ ^0.05 ^0.9 unless block ~ ~ ~ #minecraft:replaceable run return run function nonios:class/balrog/climb
execute rotated ~ 0 positioned ^ ^0.6 ^0.9 unless block ~ ~ ~ #minecraft:replaceable run return run function nonios:class/balrog/climb
execute rotated ~ 0 positioned ^ ^1.2 ^0.9 unless block ~ ~ ~ #minecraft:replaceable run return run function nonios:class/balrog/climb
function nonios:class/balrog/unclimb
