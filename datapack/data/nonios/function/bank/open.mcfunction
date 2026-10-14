# {team, Team, color}: as the player at their own vault. Builds the bank dialog in storage nonios:bank ui.d and shows it.
# Fixed layout (feedback #41: UI never moves): body = balances + interest + one result line; inputs = Deposit and
# Withdraw sliders; actions = Deposit | Deposit all / Withdraw | Withdraw all, always there, greyed out (no action:
# inactive) when there is nothing to move. Sliders run 1..max(amount, 2); requests are clamped anyway.
# Sliders (number_range) + dynamic/run_command -> /trigger nx.bankd|nx.bankw set <slider value>: permission 0, no op prompt.
execute store result score #p nx.eco run scoreboard players get @s nx.coins
$execute store result score #bb nx.eco run scoreboard players get #$(team) nx.bank
$data modify storage nonios:bank ui.a set value {team:"$(team)",Team:"$(Team)",color:"$(color)",cap:"",dc:"green",wc:"yellow"}
execute if score #p nx.eco matches ..0 run data modify storage nonios:bank ui.a.dc set value "dark_gray"
execute if score #bb nx.eco matches ..0 run data modify storage nonios:bank ui.a.wc set value "dark_gray"
execute store result storage nonios:bank ui.a.p int 1 run scoreboard players get #p nx.eco
execute store result storage nonios:bank ui.a.b int 1 run scoreboard players get #bb nx.eco
scoreboard players operation #m nx.eco = #p nx.eco
execute if score #m nx.eco matches ..1 run scoreboard players set #m nx.eco 2
execute store result storage nonios:bank ui.a.pm int 1 run scoreboard players get #m nx.eco
scoreboard players operation #m nx.eco = #bb nx.eco
execute if score #m nx.eco matches ..1 run scoreboard players set #m nx.eco 2
execute store result storage nonios:bank ui.a.bm int 1 run scoreboard players get #m nx.eco
# slider starts: deposit = whole purse, withdraw = min(bank, 100); at least 1
scoreboard players operation #wi nx.eco = #p nx.eco
execute if score #wi nx.eco matches ..0 run scoreboard players set #wi nx.eco 1
execute store result storage nonios:bank ui.a.pi int 1 run scoreboard players get #wi nx.eco
scoreboard players operation #wi nx.eco = #bb nx.eco
scoreboard players operation #wi nx.eco < #100 nx.eco
execute if score #wi nx.eco matches ..0 run scoreboard players set #wi nx.eco 1
execute store result storage nonios:bank ui.a.wi int 1 run scoreboard players get #wi nx.eco
# interest line: the rate and cap right now (they grow over the match, economy/rate), seconds to the next payout
function nonios:economy/rate
execute store result storage nonios:bank ui.a.rw int 1 run scoreboard players get #rw nx.eco
execute store result storage nonios:bank ui.a.rt int 1 run scoreboard players get #rt nx.eco
data modify storage nonios:bank ui.a.per set from storage nonios:config interest_period
execute if score #icap nx.eco matches 1.. store result storage nonios:bank ui.a.c int 1 run scoreboard players get #icap nx.eco
execute if score #icap nx.eco matches 1.. run function nonios:bank/ui/cap with storage nonios:bank ui.a
execute store result score #nx nx.eco run time query gametime
scoreboard players operation #nx nx.eco *= #-1 nx.eco
scoreboard players operation #nx nx.eco += #int_at nx.eco
scoreboard players add #nx nx.eco 19
scoreboard players operation #nx nx.eco /= #20 nx.eco
execute if score #nx nx.eco matches ..0 run scoreboard players set #nx nx.eco 0
execute store result storage nonios:bank ui.a.next int 1 run scoreboard players get #nx nx.eco
data modify storage nonios:bank ui.d set value {type:"minecraft:multi_action",title:"",body:[],inputs:[],actions:[],columns:2,pause:false,after_action:"wait_for_response",exit_action:{label:"Close"}}
function nonios:bank/ui/head with storage nonios:bank ui.a
execute unless data storage nonios:bank ui.msg run data modify storage nonios:bank ui.msg set value {type:"minecraft:plain_message",width:300,contents:{text:" "}}
data modify storage nonios:bank ui.d.body append from storage nonios:bank ui.msg
function nonios:bank/ui/sliders with storage nonios:bank ui.a
execute if score #p nx.eco matches 1.. run function nonios:bank/ui/dep_on with storage nonios:bank ui.a
execute if score #p nx.eco matches ..0 run data modify storage nonios:bank ui.d.actions append from storage nonios:bank off[0]
execute if score #p nx.eco matches ..0 run data modify storage nonios:bank ui.d.actions append from storage nonios:bank off[1]
execute if score #bb nx.eco matches 1.. run function nonios:bank/ui/wd_on with storage nonios:bank ui.a
execute if score #bb nx.eco matches ..0 run data modify storage nonios:bank ui.d.actions append from storage nonios:bank off[2]
execute if score #bb nx.eco matches ..0 run data modify storage nonios:bank ui.d.actions append from storage nonios:bank off[3]
function nonios:bank/ui/show with storage nonios:bank ui
