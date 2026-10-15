# Economy (M3, DESIGN §2.6-2.7): team bank dialog + interest (bank/), kill rewards + killstreak bounties (economy/kill).
# Coins = nx.coins (the purse), team banks = #white / #black in nx.bank. Config: storage nonios:config (admin > Economy).
scoreboard objectives add nx.eco dummy
scoreboard objectives add nx.bank dummy
# bank triggers (permission 0, no op prompt): nx.bankt 1 open the withdraw dialog / 3 withdraw all / 4 withdraw half,
# nx.bankw = withdraw N (preset buttons). Deposits need no trigger: entering your own bank zone (bank/zone/*).
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
scoreboard players set #10 nx.eco 10
scoreboard players set #20 nx.eco 20
scoreboard players set #1000 nx.eco 1000
scoreboard players set #100 nx.eco 100
scoreboard players set #-1 nx.eco -1
scoreboard players add #white nx.bank 0
scoreboard players add #black nx.bank 0
# --- config (storage nonios:config), defaults only when missing so admin changes survive /reload ---
# interest (#108; paid +1 at a time every tick, bank/interest/tick). All terms here, in storage nonios:config:
#   interest_period  seconds per rate period (60 = the rate is per minute; 1 = per second), 1..100
#   interest_curve   rate over the match clock: points {t: match seconds, r: parts per million per period (10000 = 1%)},
#                    joined by a smooth monotone cubic (bank/curve), flat before the first / after the last point
#   interest_base    only this many banked coins earn (2000 x 2% = 40 per period at most)
#   interest_scale   percent applied to the whole curve (admin)
# Defaults: 0% -> 0.5% at min 10 -> 1% at 20 -> 2% at 30, per minute, on at most 2000 coins.
# interest_v 2 = this scheme; older worlds drop their v4 keys (interest_start/end/ramp/cap_s) and get the defaults.
execute unless data storage nonios:config {interest_v:2} run data remove storage nonios:config interest_period
execute unless data storage nonios:config {interest_v:2} run data remove storage nonios:config interest_curve
data remove storage nonios:config interest_rate
data remove storage nonios:config interest_grow
data remove storage nonios:config interest_rate_max
data remove storage nonios:config interest_cap_grow
data remove storage nonios:config interest_start
data remove storage nonios:config interest_end
data remove storage nonios:config interest_ramp
data remove storage nonios:config interest_cap_s
data remove storage nonios:config interest_cap
data modify storage nonios:config interest_v set value 2
execute unless data storage nonios:config interest_period run data modify storage nonios:config interest_period set value 60
execute unless data storage nonios:config interest_curve run data modify storage nonios:config interest_curve set value [{t:0,r:0},{t:600,r:5000},{t:1200,r:10000},{t:1800,r:20000}]
execute unless data storage nonios:config interest_base run data modify storage nonios:config interest_base set value 2000
execute unless data storage nonios:config interest_scale run data modify storage nonios:config interest_scale set value 100
# interest mode (#110): 1 = A flat interest_a_rate per second, at most interest_a_cap coins/s (a curve over the match clock,
#   r = 1/1000 coin per second: 0, 1/s at min 10, 5 at 20, 20 at 30, 35 at 40, 50 at 50, then +1/s a minute); 2 = B interest_curve per interest_period, every banked coin earns (no base);
#   3 = C interest_curve per interest_period on at most interest_base coins (the #108 scheme)
# A chosen by the user (#110/#111): worlds from before take A and the longer cap once (interest_av 2)
execute unless data storage nonios:config {interest_av:2} run data remove storage nonios:config interest_a_cap
execute unless data storage nonios:config {interest_av:2} run data modify storage nonios:config interest_mode set value 1
data modify storage nonios:config interest_av set value 2
execute unless data storage nonios:config interest_mode run data modify storage nonios:config interest_mode set value 1
# after the last cap point the cap keeps growing by interest_a_grow (1/1000 coin per second) every minute, no ceiling
execute unless data storage nonios:config interest_a_grow run data modify storage nonios:config interest_a_grow set value 1000
execute unless data storage nonios:config interest_a_rate run data modify storage nonios:config interest_a_rate set value 1000
execute unless data storage nonios:config interest_a_cap run data modify storage nonios:config interest_a_cap set value [{t:0,r:0},{t:600,r:1000},{t:1200,r:5000},{t:1800,r:20000},{t:2400,r:35000},{t:3000,r:50000}]
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
scoreboard players set #3 nx.eco 3
scoreboard players set #2000 nx.eco 2000
# interest curve (needs the constants above): tangents once per load; rate recomputed on the next tick
function nonios:bank/curve/build
scoreboard players set #rsec nx.eco -1
scoreboard players set #2 nx.eco 2
# withdraw dialog (bank/open): Half and All greyed in the same places when the bank is empty; no action = inactive
data modify storage nonios:bank off set value [{label:{text:"Half",color:"dark_gray"},tooltip:{text:"The bank is empty"},width:150},{label:{text:"All",color:"dark_gray"},tooltip:{text:"The bank is empty"},width:150}]
