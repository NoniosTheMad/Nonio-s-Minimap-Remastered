# {m}: interest mode 1 A / 2 B / 3 C (storage nonios:config interest_mode, the live game setting), then redraw
$data modify storage nonios:config interest_mode set value $(m)
scoreboard players set #rsec nx.eco -1
function nonios:economy/hud/second
function demo:im/open
