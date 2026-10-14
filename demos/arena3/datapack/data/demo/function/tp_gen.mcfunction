# next to your team's field generator (no team: White's)
execute if entity @s[team=black] run return run function demo:tp_gen_at with storage nonios:map black.gen
function demo:tp_gen_at with storage nonios:map white.gen
