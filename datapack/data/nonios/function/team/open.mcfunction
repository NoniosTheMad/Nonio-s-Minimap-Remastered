# as a player: team counts + phase into storage nonios:ui team, then the picker. Same 4 buttons in every state;
# a choice that team/pick or team/leave would refuse is greyed (no action) with the reason as tooltip (dialog rule #41).
data modify storage nonios:ui team set value {}
execute store result storage nonios:ui team.w int 1 if entity @a[team=white]
execute store result storage nonios:ui team.b int 1 if entity @a[team=black]
data modify storage nonios:ui team.me set value "no team"
execute if entity @s[team=white] run data modify storage nonios:ui team.me set value "White"
execute if entity @s[team=black] run data modify storage nonios:ui team.me set value "Black"
data modify storage nonios:ui team.phase set value "Lobby"
execute if score #state nx.state matches 1..2 run data modify storage nonios:ui team.phase set value "Match running"
execute if score #state nx.state matches 3 run data modify storage nonios:ui team.phase set value "End screen"
# per button: label colour (c), tooltip (t), action fragment (a: ",action:{...}" or "" = greyed)
data modify storage nonios:ui team.wc set value "white"
data modify storage nonios:ui team.bc set value "light_purple"
data modify storage nonios:ui team.ac set value "green"
data modify storage nonios:ui team.nc set value "gray"
function nonios:team/tips with storage nonios:ui team
data modify storage nonios:ui team.at set value "The smaller team"
data modify storage nonios:ui team.nt set value "Watch the next match"
data modify storage nonios:ui team.wa set value ',action:{type:"minecraft:run_command",command:"trigger nx.team set 2"}'
data modify storage nonios:ui team.ba set value ',action:{type:"minecraft:run_command",command:"trigger nx.team set 3"}'
data modify storage nonios:ui team.aa set value ',action:{type:"minecraft:run_command",command:"trigger nx.team set 4"}'
data modify storage nonios:ui team.na set value ',action:{type:"minecraft:run_command",command:"trigger nx.team set 5"}'
execute if entity @s[team=white] run function nonios:team/grey {k:"w",why:"You are on White"}
execute if entity @s[team=black] run function nonios:team/grey {k:"b",why:"You are on Black"}
execute if score #state nx.state matches 1..2 if score #white nx.last matches 1 run function nonios:team/grey {k:"w",why:"White's Nexus is destroyed"}
execute if score #state nx.state matches 1..2 if score #black nx.last matches 1 run function nonios:team/grey {k:"b",why:"Black's Nexus is destroyed"}
execute if score #state nx.state matches 1..2 unless entity @s[team=] run function nonios:team/grey {k:"w",why:"No switching during a match"}
execute if score #state nx.state matches 1..2 unless entity @s[team=] run function nonios:team/grey {k:"b",why:"No switching during a match"}
execute if score #state nx.state matches 1..2 unless entity @s[team=] run function nonios:team/grey {k:"a",why:"No switching during a match"}
execute if score #state nx.state matches 1..2 unless entity @s[team=] run function nonios:team/grey {k:"n",why:"No leaving during a match"}
function nonios:team/show with storage nonios:ui team
