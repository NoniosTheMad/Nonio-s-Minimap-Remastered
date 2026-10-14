execute store result storage nonios:ui team.w int 1 if entity @a[team=white]
execute store result storage nonios:ui team.b int 1 if entity @a[team=black]
data modify storage nonios:ui team.me set value "no team"
execute if entity @s[team=white] run data modify storage nonios:ui team.me set value "White"
execute if entity @s[team=black] run data modify storage nonios:ui team.me set value "Black"
data modify storage nonios:ui team.phase set value "Lobby: pick freely. Teamless players are auto-assigned at Start."
execute if score #state nx.state matches 1..2 run data modify storage nonios:ui team.phase set value "Match running: teamless players can join a team that still has its Nexus. No switching."
function nonios:team/show with storage nonios:ui team
