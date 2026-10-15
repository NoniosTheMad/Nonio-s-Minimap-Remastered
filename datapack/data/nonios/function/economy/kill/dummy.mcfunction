# as a player who killed a test dummy (game/dummy_killed) or the demo's "Simulate kill". A dead husk can't be selected,
# so the victim profile comes from #dummy nx.streak / #dummy nx.tier (demo button "Victim profile").
scoreboard players add #dummy nx.streak 0
scoreboard players add #dummy nx.tier 0
scoreboard players operation #vs nx.eco = #dummy nx.streak
scoreboard players set #bonus nx.eco 0
scoreboard players operation #vtier nx.eco = #dummy nx.tier
function nonios:economy/kill_bonus/tier_value
# arena Bounty Hunt (#nonios:economy/kill_bonus entry): the husk is gone, so the killer's position stands in for it
function nonios:arena/event/bounty_bonus
data modify storage nonios:eco vname set value "Dummy"
function nonios:economy/kill/award
