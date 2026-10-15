# solo start: put the tester on a team first (the game refuses to start with nobody on a team)
execute if entity @s[team=] run function nonios:team/auto_pick
function nonios:game/start
