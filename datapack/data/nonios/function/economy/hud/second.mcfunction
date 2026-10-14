# once a second (economy/tick) and after each payout: redraw the team bank sidebars during a match, hide them otherwise
execute unless score #state nx.state matches 1..2 if score #hud_on nx.eco matches 1 run function nonios:economy/hud/hide
execute unless score #state nx.state matches 1..2 run return 0
execute unless score #hud_on nx.eco matches 1 run function nonios:economy/hud/show
function nonios:economy/rate
execute store result score #nx nx.eco run time query gametime
scoreboard players operation #nx nx.eco *= #-1 nx.eco
scoreboard players operation #nx nx.eco += #int_at nx.eco
scoreboard players add #nx nx.eco 19
scoreboard players operation #nx nx.eco /= #20 nx.eco
execute if score #nx nx.eco matches ..0 run scoreboard players set #nx nx.eco 0
function nonios:economy/hud/team {team:"white"}
function nonios:economy/hud/team {team:"black"}
