# {n}: your team bank = n, then redraw
$execute if entity @s[team=white] run scoreboard players set #white nx.bank $(n)
$execute if entity @s[team=black] run scoreboard players set #black nx.bank $(n)
function nonios:economy/hud/second
function demo:im/open
