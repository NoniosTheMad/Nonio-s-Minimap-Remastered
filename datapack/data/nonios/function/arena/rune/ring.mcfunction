# as + at a node: 4 outline points per tick (one per side) marching round the zone square; one lap = nx.ar_rs ticks.
# Point t along each side = (rc - (2r + 1)) / 2, from -e to e - 0.5 (e = r + 0.5 = data.e).
scoreboard players add @s nx.ar_rc 1
execute if score @s nx.ar_rc >= @s nx.ar_rs run scoreboard players set @s nx.ar_rc 0
scoreboard players operation #t nx.arena = @s nx.ar_rs
scoreboard players operation #t nx.arena /= #2 nx.arena
scoreboard players operation #t nx.arena *= #-1 nx.arena
scoreboard players operation #t nx.arena += @s nx.ar_rc
execute store result storage nonios:arena rg.t double 0.5 run scoreboard players get #t nx.arena
data modify storage nonios:arena rg.e set from entity @s data.e
data modify storage nonios:arena rg.p set from storage nonios:arena config.rune.ring.neutral
execute if score @s nx.ar_own matches 1 run data modify storage nonios:arena rg.p set from storage nonios:arena config.rune.ring.white
execute if score @s nx.ar_own matches 2 run data modify storage nonios:arena rg.p set from storage nonios:arena config.rune.ring.black
execute if score @s nx.ar_st matches 30..39 run data modify storage nonios:arena rg.p set from storage nonios:arena config.rune.ring.contested
function nonios:arena/rune/ring_m with storage nonios:arena rg
