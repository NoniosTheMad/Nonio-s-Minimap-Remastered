# fast-forward the match clock by 5 minutes: money scale (purse weight) and interest rate jump as if 5 min passed
execute unless score #state nx.state matches 1..2 run return run tellraw @s {"text":"[demo] The match clock runs during a match (Start match first).","color":"red"}
scoreboard players remove #t0 nx.eco 6000
function nonios:purse/scale
function nonios:economy/hud/second
function demo:status
