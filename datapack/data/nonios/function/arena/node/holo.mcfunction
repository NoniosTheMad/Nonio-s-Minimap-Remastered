# as + at a node marker: rewrite its hologram. Line 1 name (owner colour), line 2 state (+ %), line 3 payout / hint.
data modify storage nonios:arena h set value {oc:"yellow",s:"Neutral",sc:"gray",p:"",l3:"stand inside to capture"}
data modify storage nonios:arena h.name set from entity @s data.name
execute if score @s nx.ar_own matches 1 run data modify storage nonios:arena h.oc set value "white"
execute if score @s nx.ar_own matches 2 run data modify storage nonios:arena h.oc set value "light_purple"
scoreboard players operation #st2 nx.arena = @s nx.ar_st
scoreboard players operation #st2 nx.arena /= #10 nx.arena
execute if score #st2 nx.arena matches 1 run data modify storage nonios:arena h merge value {s:"White capturing",sc:"white",l3:"stay inside"}
execute if score #st2 nx.arena matches 2 run data modify storage nonios:arena h merge value {s:"Black capturing",sc:"light_purple",l3:"stay inside"}
execute if score #st2 nx.arena matches 3 run data modify storage nonios:arena h merge value {s:"CONTESTED",sc:"red",l3:"both teams inside: progress frozen"}
execute if score #st2 nx.arena matches 4 run data modify storage nonios:arena h merge value {s:"Held by White",sc:"white"}
execute if score #st2 nx.arena matches 5 run data modify storage nonios:arena h merge value {s:"Held by Black",sc:"light_purple"}
execute if score #st2 nx.arena matches 6 run data modify storage nonios:arena h merge value {s:"White taking it",sc:"white",l3:"stay inside"}
execute if score #st2 nx.arena matches 7 run data modify storage nonios:arena h merge value {s:"Black taking it",sc:"light_purple",l3:"stay inside"}
# progress % while someone is capturing
scoreboard players operation #pct nx.arena = @s nx.ar_cap
execute if score #pct nx.arena matches ..-1 run scoreboard players operation #pct nx.arena *= #-1 nx.arena
scoreboard players operation #pct nx.arena *= #100 nx.arena
scoreboard players operation #pct nx.arena /= #capture nx.arena
execute store result storage nonios:arena h.pn int 1 run scoreboard players get #pct nx.arena
execute if score #st2 nx.arena matches 1..2 run function nonios:arena/node/holo_pct with storage nonios:arena h
execute if score #st2 nx.arena matches 6..7 run function nonios:arena/node/holo_pct with storage nonios:arena h
# held: seconds to the next payout (real time) = ceil(t / (20 x speed))
scoreboard players operation #div nx.arena = #speed nx.arena
scoreboard players operation #div nx.arena *= #20 nx.arena
scoreboard players operation #sec nx.arena = @s nx.ar_t
scoreboard players operation #sec nx.arena += #div nx.arena
scoreboard players remove #sec nx.arena 1
scoreboard players operation #sec nx.arena /= #div nx.arena
execute store result storage nonios:arena h.sec int 1 run scoreboard players get #sec nx.arena
execute store result storage nonios:arena h.mult int 1 run scoreboard players get #mult nx.arena
execute if score @s nx.ar_own matches 1.. if score #mult nx.arena matches ..1 run function nonios:arena/node/holo_pay with storage nonios:arena h
execute if score @s nx.ar_own matches 1.. if score #mult nx.arena matches 2.. run function nonios:arena/node/holo_pay_x with storage nonios:arena h
function nonios:arena/node/holo_set with storage nonios:arena h
