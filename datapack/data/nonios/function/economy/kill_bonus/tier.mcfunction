# Default #nonios:economy/kill_bonus entry (as the dead victim): bonus by the victim's tier, nx.tier (0 = none).
# Classes (M4) set nx.tier when bought/applied (V2: Tier 1/2/3 from the shop kits, reset on death) or add their own function to the tag.
scoreboard players add @s nx.tier 0
scoreboard players operation #vtier nx.eco = @s nx.tier
function nonios:economy/kill_bonus/tier_value
