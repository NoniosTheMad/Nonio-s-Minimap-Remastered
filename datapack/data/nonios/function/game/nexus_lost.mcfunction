# from nexus/destroyed: team $(team) is on its last life
execute unless score #state nx.state matches 1..2 run return 0
$scoreboard players set #$(team) nx.last 1
$tellraw @a[team=$(team)] {"text":"Your Nexus is destroyed. Last life.","color":"red","bold":true}
function nonios:game/win_check
