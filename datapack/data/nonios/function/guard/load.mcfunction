# Spawn defense (V2 "House"/"Deep" armor stands): players of the other team standing within r blocks of a team's spawn
# (map/config <team>.guard {foe,x,y,z,r}) get Instant Damage II every 10 ticks, in prep and battle. Own team untouched
# (V2's Deep zone also withered its own team: open question, not ported). config spawn_guard 0b turns it off.
scoreboard objectives add nx.guard dummy
execute unless data storage nonios:config spawn_guard run data modify storage nonios:config spawn_guard set value 1b
