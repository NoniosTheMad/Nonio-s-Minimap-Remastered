# as + at a node marker, every tick
# 1) bar: the shown value (x10, signed like nx.ar_cap) slides from where it was at the last check to the new value
scoreboard players operation #tgt nx.arena = @s nx.ar_cap
scoreboard players operation #tgt nx.arena *= #10 nx.arena
execute unless score #on nx.arena matches 1 run scoreboard players operation @s nx.ar_shw = #tgt nx.arena
execute if score #on nx.arena matches 1 run function nonios:arena/rune/slide
# 2) zone outline on the ground
function nonios:arena/rune/ring
# 3) the rune, every few ticks
scoreboard players remove @s nx.ar_fx 1
execute if score @s nx.ar_fx matches ..0 run function nonios:arena/rune/draw
