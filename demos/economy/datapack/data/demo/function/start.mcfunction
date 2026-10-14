# solo start with a long preparation (bank + interest work in prep and battle): team first, the game refuses to start without one
data modify storage nonios:config prep_time set value 600
execute if entity @s[team=] run function nonios:team/auto_pick
function nonios:game/start
