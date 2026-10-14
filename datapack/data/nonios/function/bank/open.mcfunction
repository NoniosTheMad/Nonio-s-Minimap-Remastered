# {team, Team, color}: as the player at their own vault. Builds the bank dialog in storage nonios:bank ui.d and shows it.
# Sliders (number_range) + dynamic/run_command -> /trigger nx.bankd|nx.bankw set <slider value>: permission 0, no op prompt.
# A slider needs at least 2 coins (start 1 < end); "... all" buttons cover the rest.
execute store result score #p nx.eco run scoreboard players get @s nx.coins
$execute store result score #bb nx.eco run scoreboard players get #$(team) nx.bank
$data modify storage nonios:bank ui.a set value {team:"$(team)",Team:"$(Team)",color:"$(color)",cap:""}
execute store result storage nonios:bank ui.a.p int 1 run scoreboard players get #p nx.eco
execute store result storage nonios:bank ui.a.b int 1 run scoreboard players get #bb nx.eco
# withdraw slider starts at min(bank, 100)
scoreboard players operation #wi nx.eco = #bb nx.eco
scoreboard players operation #wi nx.eco < #100 nx.eco
execute store result storage nonios:bank ui.a.wi int 1 run scoreboard players get #wi nx.eco
# interest line: rate (permille -> "2.0"), period, cap, seconds to the next payout
execute store result score #r nx.eco run data get storage nonios:config interest_rate
scoreboard players operation #rw nx.eco = #r nx.eco
scoreboard players operation #rw nx.eco /= #10 nx.eco
scoreboard players operation #r nx.eco %= #10 nx.eco
execute store result storage nonios:bank ui.a.rw int 1 run scoreboard players get #rw nx.eco
execute store result storage nonios:bank ui.a.rt int 1 run scoreboard players get #r nx.eco
data modify storage nonios:bank ui.a.per set from storage nonios:config interest_period
execute store result score #c nx.eco run data get storage nonios:config interest_cap
execute if score #c nx.eco matches 1.. run function nonios:bank/ui/cap with storage nonios:config
execute store result score #nx nx.eco run time query gametime
scoreboard players operation #nx nx.eco *= #-1 nx.eco
scoreboard players operation #nx nx.eco += #int_at nx.eco
scoreboard players add #nx nx.eco 19
scoreboard players operation #nx nx.eco /= #20 nx.eco
execute if score #nx nx.eco matches ..0 run scoreboard players set #nx nx.eco 0
execute store result storage nonios:bank ui.a.next int 1 run scoreboard players get #nx nx.eco
data modify storage nonios:bank ui.d set value {type:"minecraft:multi_action",title:"",body:[],inputs:[],actions:[],columns:2,pause:false,after_action:"wait_for_response",exit_action:{label:"Close"}}
function nonios:bank/ui/head with storage nonios:bank ui.a
data modify storage nonios:bank ui.d.body append from storage nonios:bank ui.msg
execute if score #p nx.eco matches 0 if score #bb nx.eco matches 0 run data modify storage nonios:bank ui.d.body append value {type:"minecraft:plain_message",width:300,contents:{text:"Nothing to deposit or withdraw yet: mine ores for coins.",color:"gray",italic:true}}
execute if score #p nx.eco matches 2.. run function nonios:bank/ui/dep_slider with storage nonios:bank ui.a
execute if score #bb nx.eco matches 2.. run function nonios:bank/ui/wd_slider with storage nonios:bank ui.a
execute if score #p nx.eco matches 2.. run data modify storage nonios:bank ui.d.actions append value {label:{text:"Deposit",color:"green"},tooltip:{text:"Deposit the amount on the Deposit slider"},width:150,action:{type:"minecraft:dynamic/run_command",template:"trigger nx.bankd set $(dep)"}}
execute if score #p nx.eco matches 1.. run function nonios:bank/ui/dep_all with storage nonios:bank ui.a
execute if score #bb nx.eco matches 2.. run data modify storage nonios:bank ui.d.actions append value {label:{text:"Withdraw",color:"yellow"},tooltip:{text:"Withdraw the amount on the Withdraw slider into your purse"},width:150,action:{type:"minecraft:dynamic/run_command",template:"trigger nx.bankw set $(wd)"}}
execute if score #bb nx.eco matches 1.. run function nonios:bank/ui/wd_all with storage nonios:bank ui.a
function nonios:bank/ui/show with storage nonios:bank ui
