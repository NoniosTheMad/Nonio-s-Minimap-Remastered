# fast-forward the match clock by 10 minutes: interest rate and coin weight jump as if 10 min passed
execute unless score #state nx.state matches 1..2 run return run tellraw @s {"text":"[demo] The match clock runs during a match (Start match first).","color":"red"}
scoreboard players remove #t0 nx.eco 12000
function nonios:purse/scale
function nonios:economy/rate
tellraw @s [{"text":"[demo] Match minute ","color":"yellow"},{"score":{"name":"#emin","objective":"nx.eco"},"color":"white"},{"text":": interest ","color":"yellow"},{"score":{"name":"#rw","objective":"nx.eco"},"color":"aqua"},{"text":".","color":"aqua"},{"score":{"name":"#rt","objective":"nx.eco"},"color":"aqua"},{"text":"%/s, max ","color":"yellow"},{"score":{"name":"#icap","objective":"nx.eco"},"color":"gold"},{"text":"/s","color":"yellow"}]
