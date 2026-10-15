# {t: ticks}: match clock to t (#t0 nx.eco = now - t), then redraw. Prep/battle only (the buttons are greyed otherwise).
execute unless score #state nx.state matches 1..2 run return run function demo:im/open
execute store result score #t0 nx.eco run time query gametime
$scoreboard players remove #t0 nx.eco $(t)
scoreboard players set #rsec nx.eco -1
function nonios:purse/scale
function nonios:economy/hud/second
function demo:im/open
