# Economy (M3, DESIGN §2.6-2.7): team bank dialog + interest (bank/), kill rewards + killstreak bounties (economy/kill).
# Coins = nx.coins (the purse), team banks = #white / #black in nx.bank. Config: storage nonios:config (admin > Economy).
scoreboard objectives add nx.eco dummy
scoreboard objectives add nx.bank dummy
# bank dialog triggers (permission 0, no op prompt): nx.bankt 1 open / 2 deposit all / 3 withdraw all,
# nx.bankd = deposit N, nx.bankw = withdraw N (slider value via dynamic/run_command)
scoreboard objectives add nx.bankt trigger
scoreboard objectives add nx.bankd trigger
scoreboard objectives add nx.bankw trigger
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
# interest (feedback #41): grows over the match, the reverse of the purse weight. Every interest_period seconds
# (prep + battle) each team bank earns rate permille of itself, at most cap coins per payout (0 = no cap), where
#   rate = min(interest_rate + interest_grow * match minutes, interest_rate_max)      (permille: 10 = 1.0%)
#   cap  = interest_cap + interest_cap_grow * match minutes
# Early the bank earns little (mining pays more); late a full bank pays the cap every period: steady income to fight on.
execute unless data storage nonios:config interest_rate run data modify storage nonios:config interest_rate set value 10
execute unless data storage nonios:config interest_grow run data modify storage nonios:config interest_grow set value 1
execute unless data storage nonios:config interest_rate_max run data modify storage nonios:config interest_rate_max set value 50
execute unless data storage nonios:config interest_period run data modify storage nonios:config interest_period set value 60
execute unless data storage nonios:config interest_cap run data modify storage nonios:config interest_cap set value 50
execute unless data storage nonios:config interest_cap_grow run data modify storage nonios:config interest_cap_grow set value 10
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
function nonios:bank/interest/arm
# bank dialog: greyed-out buttons in the same places as the live ones (bank/open); no action = the client shows them inactive
data modify storage nonios:bank off set value [{label:{text:"Deposit",color:"dark_gray"},tooltip:{text:"Your purse is empty"},width:150},{label:{text:"Deposit all",color:"dark_gray"},tooltip:{text:"Your purse is empty"},width:150},{label:{text:"Withdraw",color:"dark_gray"},tooltip:{text:"The team bank is empty"},width:150},{label:{text:"Withdraw all",color:"dark_gray"},tooltip:{text:"The team bank is empty"},width:150}]
