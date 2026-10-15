# Default #nonios:economy/kill_bonus entry (as the dead victim): bonus by the victim's tier, nx.tier (0 = none).
# nx.tier is set by the class framework (src/classes.json kill_tier; basic classes: team level - 1) and reset when the class goes.
# It is read here at the moment of death (advancement), before class/on_death strips the class on respawn.
scoreboard players add @s nx.tier 0
scoreboard players operation #vtier nx.eco = @s nx.tier
function nonios:economy/kill_bonus/tier_value
