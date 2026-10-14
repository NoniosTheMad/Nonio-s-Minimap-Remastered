# {team, Team, color}
$execute if entity @s[team=$(team)] run return run tellraw @s {"text":"You are already on $(Team).","color":"gray"}
# lobby / end screen: free choice (applies to the next match)
$execute unless score #state nx.state matches 1..2 run return run function nonios:team/set {team:"$(team)",Team:"$(Team)",color:"$(color)"}
# match running: no switching sides; teamless players may join a team that still has its Nexus
execute unless entity @s[team=] run return run tellraw @s {"text":"You can't switch teams during a match.","color":"red"}
$execute if score #$(team) nx.last matches 1 run return run tellraw @s {"text":"$(Team)'s Nexus is destroyed: no new players.","color":"red"}
$function nonios:team/set {team:"$(team)",Team:"$(Team)",color:"$(color)"}
$function nonios:game/enter {team:"$(team)"}
