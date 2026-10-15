# as + at a node whose redraw is due: pick the colours, then draw the rune for every player in view.
# Points 1..#lit (stroke order) are painted: #lit = |shown| x points / (capture x 10). Painted = the colour of the side
# holding the progress (white / black); unpainted = amber when nobody has started, dim amber while it is being painted
# or erased, red while contested. While it is being captured it redraws faster, the painted strokes throb and an
# end-rod spark marks the pen tip.
scoreboard players operation #st2 nx.arena = @s nx.ar_st
scoreboard players operation #st2 nx.arena /= #10 nx.arena
scoreboard players set #capt nx.arena 0
execute if score #st2 nx.arena matches 1..2 run scoreboard players set #capt nx.arena 1
execute if score #st2 nx.arena matches 6..7 run scoreboard players set #capt nx.arena 1
scoreboard players operation @s nx.ar_fx = #rn_every nx.arena
execute if score #capt nx.arena matches 1 run scoreboard players operation @s nx.ar_fx = #rn_every_cap nx.arena
# painted points
scoreboard players operation #lit nx.arena = @s nx.ar_shw
execute if score #lit nx.arena matches ..-1 run scoreboard players operation #lit nx.arena *= #-1 nx.arena
scoreboard players operation #lit nx.arena *= @s nx.ar_rn
scoreboard players operation #lit nx.arena /= #cap10 nx.arena
scoreboard players set #tip nx.arena 0
execute if score #capt nx.arena matches 1 if score #lit nx.arena < @s nx.ar_rn run scoreboard players operation #tip nx.arena = #lit nx.arena
execute if score #capt nx.arena matches 1 if score #tip nx.arena matches 0 run scoreboard players set #tip nx.arena 1
# colours
data modify storage nonios:arena rx set value {hp:"0 0 0 0 1",cp:"0 0 0 0 1"}
data modify storage nonios:arena rx.tip set from storage nonios:arena config.rune.col.tip
data modify storage nonios:arena rx.hot set from storage nonios:arena config.rune.col.neutral
execute if score @s nx.ar_shw matches 1.. run data modify storage nonios:arena rx.hot set from storage nonios:arena config.rune.col.white
execute if score @s nx.ar_shw matches ..-1 run data modify storage nonios:arena rx.hot set from storage nonios:arena config.rune.col.black
scoreboard players operation #pulse nx.arena = #gt nx.arena
scoreboard players operation #pulse nx.arena /= #4 nx.arena
scoreboard players operation #pulse nx.arena %= #2 nx.arena
execute if score #capt nx.arena matches 1 if score #pulse nx.arena matches 1 if score @s nx.ar_shw matches 1.. run data modify storage nonios:arena rx.hot set from storage nonios:arena config.rune.col.white_pulse
execute if score #capt nx.arena matches 1 if score #pulse nx.arena matches 1 if score @s nx.ar_shw matches ..-1 run data modify storage nonios:arena rx.hot set from storage nonios:arena config.rune.col.black_pulse
data modify storage nonios:arena rx.cold set from storage nonios:arena config.rune.col.cold
execute if score @s nx.ar_shw matches 0 run data modify storage nonios:arena rx.cold set from storage nonios:arena config.rune.col.neutral
execute if score #st2 nx.arena matches 3 run data modify storage nonios:arena rx.cold set from storage nonios:arena config.rune.col.contested
function nonios:arena/rune/view
