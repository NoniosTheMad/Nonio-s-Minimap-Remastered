# as the admin: economy config (storage nonios:config) into storage nonios:ui eco, then show the page
data modify storage nonios:ui eco set value {}
data modify storage nonios:ui eco.kr set from storage nonios:config kill_reward
data modify storage nonios:ui eco.bp set from storage nonios:config bounty_per_kill
data modify storage nonios:ui eco.bm set from storage nonios:config bounty_min_streak
data modify storage nonios:ui eco.bc set from storage nonios:config bounty_cap
data modify storage nonios:ui eco.ip set from storage nonios:config interest_period
data modify storage nonios:ui eco.ic set from storage nonios:config interest_cap
data modify storage nonios:ui eco.br set from storage nonios:config bank_range
data modify storage nonios:ui eco.ig set from storage nonios:config interest_grow
data modify storage nonios:ui eco.im set from storage nonios:config interest_rate_max
data modify storage nonios:ui eco.icg set from storage nonios:config interest_cap_grow
execute store result score #r nx.eco run data get storage nonios:config interest_rate
scoreboard players operation #rw nx.eco = #r nx.eco
scoreboard players operation #rw nx.eco /= #10 nx.eco
scoreboard players operation #r nx.eco %= #10 nx.eco
execute store result storage nonios:ui eco.rw int 1 run scoreboard players get #rw nx.eco
execute store result storage nonios:ui eco.rt int 1 run scoreboard players get #r nx.eco
execute store result storage nonios:ui eco.t1 int 1 run data get storage nonios:config tier_bonus[1]
execute store result storage nonios:ui eco.t2 int 1 run data get storage nonios:config tier_bonus[2]
execute store result storage nonios:ui eco.t3 int 1 run data get storage nonios:config tier_bonus[3]
execute store result storage nonios:ui eco.wb int 1 run scoreboard players get #white nx.bank
execute store result storage nonios:ui eco.bb int 1 run scoreboard players get #black nx.bank
function nonios:admin/economy/show with storage nonios:ui eco
