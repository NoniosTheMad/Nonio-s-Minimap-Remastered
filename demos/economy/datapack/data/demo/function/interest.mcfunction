# pay 60 interest seconds at once (one minute of income; the per-second payout keeps running)
execute unless score #state nx.state matches 1..2 run return run tellraw @s {"text":"[demo] Interest is paid during a match (Start match first).","color":"red"}
execute if score #white nx.bank matches ..0 if score #black nx.bank matches ..0 run tellraw @s {"text":"[demo] Both team banks are empty: walk into your bank with coins first.","color":"red"}
scoreboard players set #demo_n nx.eco 60
function demo:interest_loop
function nonios:economy/hud/second
