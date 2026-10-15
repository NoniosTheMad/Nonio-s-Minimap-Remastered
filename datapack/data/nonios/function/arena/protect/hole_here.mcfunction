# at a block of the arena: the same block in the backup -> air (stays changeable, never restored)
execute store result storage nonios:arena hole.y int 1 run scoreboard players get #poff nx.arena
function nonios:arena/protect/hole_m with storage nonios:arena hole
