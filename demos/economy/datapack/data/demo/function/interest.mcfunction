# pay one interest round now (the schedule loop keeps its own clock)
execute unless score #state nx.state matches 1..2 run return run tellraw @s {"text":"[demo] Interest is paid during a match (Start match first).","color":"red"}
execute if score #white nx.bank matches ..0 if score #black nx.bank matches ..0 run tellraw @s {"text":"[demo] Both team banks are empty: deposit some coins first.","color":"red"}
function nonios:bank/interest/pay
