# as the admin: economy config (storage nonios:config) into storage nonios:ui eco, then show the page
data modify storage nonios:ui eco set value {}
data modify storage nonios:ui eco.kr set from storage nonios:config kill_reward
data modify storage nonios:ui eco.bp set from storage nonios:config bounty_per_kill
data modify storage nonios:ui eco.bm set from storage nonios:config bounty_min_streak
data modify storage nonios:ui eco.bc set from storage nonios:config bounty_cap
data modify storage nonios:ui eco.ib set from storage nonios:config interest_base
data modify storage nonios:ui eco.isc set from storage nonios:config interest_scale
data modify storage nonios:ui eco.br set from storage nonios:config bank_range
# interest now (economy/rate text) and the unit
function nonios:economy/rate
data modify storage nonios:ui eco.ir set from storage nonios:eco rtxt
execute store result storage nonios:ui eco.t1 int 1 run data get storage nonios:config tier_bonus[1]
execute store result storage nonios:ui eco.t2 int 1 run data get storage nonios:config tier_bonus[2]
execute store result storage nonios:ui eco.t3 int 1 run data get storage nonios:config tier_bonus[3]
execute store result storage nonios:ui eco.wb int 1 run scoreboard players get #white nx.bank
execute store result storage nonios:ui eco.bb int 1 run scoreboard players get #black nx.bank
function nonios:admin/economy/show with storage nonios:ui eco
