# once a second (economy/tick, right after the interest payout): redraw the team bank sidebars during a match, hide them otherwise
execute unless score #state nx.state matches 1..2 if score #hud_on nx.eco matches 1 run function nonios:economy/hud/hide
execute unless score #state nx.state matches 1..2 run return 0
execute unless score #hud_on nx.eco matches 1 run function nonios:economy/hud/show
function nonios:economy/rate
function nonios:economy/hud/team {team:"white"}
function nonios:economy/hud/team {team:"black"}
