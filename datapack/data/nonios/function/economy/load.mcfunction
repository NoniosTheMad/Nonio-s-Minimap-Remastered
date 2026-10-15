# Economy (M3, DESIGN §2.6-2.7): team bank dialog + interest (bank/), kill rewards + killstreak bounties (economy/kill).
# Coins = nx.coins (the purse), team banks = #white / #black in nx.bank. Config: storage nonios:config (admin > Economy).
scoreboard objectives add nx.eco dummy
scoreboard objectives add nx.bank dummy
# bank triggers (permission 0, no op prompt): nx.bankt 1 open the withdraw dialog / 3 withdraw all / 4 withdraw half,
# nx.bankw = withdraw N (preset buttons). Deposits need no trigger: stepping onto your own bank pad (bank/pad/*).
scoreboard objectives add nx.bankt trigger
scoreboard objectives add nx.bankw trigger
# the deposit slider is gone (bank v4, #47)
scoreboard objectives remove nx.bankd
# kills in a row without dying (bounty on your head); nx.tier = victim tier, owned by classes (class/gen/<id>/apply, class/strip)
scoreboard objectives add nx.streak dummy {"text":"Streak","color":"red"}
scoreboard objectives add nx.tier dummy
# kill reward waiting for the actionbar (shown the tick after the kill, once the purse transfer is known too)
scoreboard objectives add nx.krw dummy
scoreboard objectives add nx.kbty dummy
scoreboard objectives add nx.kbon dummy
scoreboard objectives add nx.kpurse dummy
scoreboard objectives add nx.kgold dummy
scoreboard players set #10 nx.eco 10
scoreboard players set #20 nx.eco 20
scoreboard players set #1000 nx.eco 1000
scoreboard players set #100 nx.eco 100
scoreboard players set #-1 nx.eco -1
scoreboard players add #white nx.bank 0
scoreboard players add #black nx.bank 0
# --- config (storage nonios:config), defaults only when missing so admin changes survive /reload ---
# interest (bank v4, feedback #47, like V2): every second (prep + battle) each team bank earns rate of itself,
# at most interest_cap coins per second. rate (basis points, 100 = 1%) slides linearly with the match clock:
#   rate = interest_start + (interest_end - interest_start) * min(match seconds, interest_ramp) / interest_ramp
# Defaults 1% -> 10% over 30 min, cap 20/s. Fractions of a coin carry over per team (#acc_<team>, 1/10000 coin).
data remove storage nonios:config interest_rate
data remove storage nonios:config interest_grow
data remove storage nonios:config interest_rate_max
data remove storage nonios:config interest_period
data remove storage nonios:config interest_cap_grow
execute unless data storage nonios:config interest_start run data modify storage nonios:config interest_start set value 100
execute unless data storage nonios:config interest_end run data modify storage nonios:config interest_end set value 1000
execute unless data storage nonios:config interest_ramp run data modify storage nonios:config interest_ramp set value 1800
execute unless data storage nonios:config interest_cap_s run data modify storage nonios:config interest_cap_s set value 20
data remove storage nonios:config interest_cap
# bank: usable within bank_range blocks of your own team's vault
execute unless data storage nonios:config bank_range run data modify storage nonios:config bank_range set value 5
# kills: kill_reward + bounty (victim streak >= bounty_min_streak: streak * bounty_per_kill, max bounty_cap, 0 = no cap)
execute unless data storage nonios:config kill_reward run data modify storage nonios:config kill_reward set value 10
execute unless data storage nonios:config bounty_per_kill run data modify storage nonios:config bounty_per_kill set value 10
execute unless data storage nonios:config bounty_min_streak run data modify storage nonios:config bounty_min_streak set value 3
execute unless data storage nonios:config bounty_cap run data modify storage nonios:config bounty_cap set value 150
# victim tier bonus (index = nx.tier of the victim; V2: tier 1/2/3 = +20/+90/+190)
execute unless data storage nonios:config tier_bonus run data modify storage nonios:config tier_bonus set value [0,20,90,190]
# match clock for the money scale (purse/scale) and interest growth: gametime at the match start (economy/match_start)
execute unless score #t0 nx.eco = #t0 nx.eco store result score #t0 nx.eco run time query gametime
scoreboard players set #60 nx.eco 60
# team bank sidebar (economy/hud): one objective per team, shown to that team only (sidebar.team.<team colour>)
scoreboard objectives add nx.sb_white dummy {"text":"White bank","color":"white","bold":true}
scoreboard objectives add nx.sb_black dummy {"text":"Black bank","color":"dark_purple","bold":true}
function nonios:economy/hud/lines {team:"white"}
function nonios:economy/hud/lines {team:"black"}
# interest is paid from economy/tick now; stop the old 60 s schedule loop of worlds saved before bank v4
schedule clear nonios:bank/interest/loop
scoreboard players set #10000 nx.eco 10000
scoreboard players set #1000000 nx.eco 1000000
scoreboard players set #2 nx.eco 2
# withdraw dialog (bank/open): Half and All greyed in the same places when the bank is empty; no action = inactive
data modify storage nonios:bank off set value [{label:{text:"Half",color:"dark_gray"},tooltip:{text:"The bank is empty"},width:150},{label:{text:"All",color:"dark_gray"},tooltip:{text:"The bank is empty"},width:150}]
