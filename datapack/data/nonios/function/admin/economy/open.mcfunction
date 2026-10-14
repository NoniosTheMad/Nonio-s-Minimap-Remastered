# as the admin: economy config (storage nonios:config) into storage nonios:ui eco, then show the page
data modify storage nonios:ui eco set value {}
data modify storage nonios:ui eco.kr set from storage nonios:config kill_reward
data modify storage nonios:ui eco.bp set from storage nonios:config bounty_per_kill
data modify storage nonios:ui eco.bm set from storage nonios:config bounty_min_streak
data modify storage nonios:ui eco.bc set from storage nonios:config bounty_cap
data modify storage nonios:ui eco.ic set from storage nonios:config interest_cap_s
data modify storage nonios:ui eco.br set from storage nonios:config bank_range
# interest start / end as "<w>.<t>%" (config in basis points), ramp in minutes
execute store result score #r nx.eco run data get storage nonios:config interest_start
function nonios:admin/economy/pct {k:"s"}
execute store result score #r nx.eco run data get storage nonios:config interest_end
function nonios:admin/economy/pct {k:"e"}
execute store result score #r nx.eco run data get storage nonios:config interest_ramp
scoreboard players operation #r nx.eco /= #60 nx.eco
execute store result storage nonios:ui eco.rm int 1 run scoreboard players get #r nx.eco
execute store result storage nonios:ui eco.t1 int 1 run data get storage nonios:config tier_bonus[1]
execute store result storage nonios:ui eco.t2 int 1 run data get storage nonios:config tier_bonus[2]
execute store result storage nonios:ui eco.t3 int 1 run data get storage nonios:config tier_bonus[3]
execute store result storage nonios:ui eco.wb int 1 run scoreboard players get #white nx.bank
execute store result storage nonios:ui eco.bb int 1 run scoreboard players get #black nx.bank
function nonios:admin/economy/show with storage nonios:ui eco
