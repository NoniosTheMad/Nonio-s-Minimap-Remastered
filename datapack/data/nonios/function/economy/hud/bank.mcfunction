# {team}, every tick while the sidebar is on: redraw the Bank row only when the balance changed (interest ticks in +1 at a time)
$execute if score #$(team) nx.bank = #shown_$(team) nx.eco run return 0
$scoreboard players operation #shown_$(team) nx.eco = #$(team) nx.bank
$data modify storage nonios:eco hb set value {team:"$(team)"}
$execute store result storage nonios:eco hb.b int 1 run scoreboard players get #$(team) nx.bank
function nonios:economy/hud/bank_set with storage nonios:eco hb
