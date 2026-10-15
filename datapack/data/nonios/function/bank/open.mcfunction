# {team, Team, color}: as the player at their own vault. Builds the withdraw dialog in storage nonios:bank ui.d and shows it.
# Bank v4 (#47): deposits happen in the bank zone, so the vault only pays out. Fixed layout (Dialog UI rules): body = purse,
# bank, interest now; eight buttons, always in the same places: 10 | 50 / 100 | 200 / 500 | 1000 / Half | All.
# A button the bank can't cover is greyed (dark_gray, no action, tooltip). Clicks -> /trigger nx.bankw set N or
# nx.bankt set 3 (all) / 4 (half); the dialog redraws with the new balances, so repeated clicks are quick.
execute store result score #p nx.eco run scoreboard players get @s nx.coins
$execute store result score #bb nx.eco run scoreboard players get #$(team) nx.bank
$data modify storage nonios:bank ui.a set value {team:"$(team)",Team:"$(Team)",color:"$(color)",cap:""}
execute store result storage nonios:bank ui.a.p int 1 run scoreboard players get #p nx.eco
execute store result storage nonios:bank ui.a.b int 1 run scoreboard players get #bb nx.eco
scoreboard players operation #h nx.eco = #bb nx.eco
scoreboard players add #h nx.eco 1
scoreboard players operation #h nx.eco /= #2 nx.eco
execute store result storage nonios:bank ui.a.h int 1 run scoreboard players get #h nx.eco
$execute store result storage nonios:bank ui.a.l int 1 run scoreboard players get #last_$(team) nx.eco
function nonios:economy/rate
execute store result storage nonios:bank ui.a.rw int 1 run scoreboard players get #rw nx.eco
execute store result storage nonios:bank ui.a.rt int 1 run scoreboard players get #rt nx.eco
data modify storage nonios:bank ui.d set value {type:"minecraft:multi_action",title:"",body:[],actions:[],columns:2,pause:false,after_action:"wait_for_response",exit_action:{label:"Close"}}
function nonios:bank/ui/head with storage nonios:bank ui.a
function nonios:bank/ui/preset {n:10}
function nonios:bank/ui/preset {n:50}
function nonios:bank/ui/preset {n:100}
function nonios:bank/ui/preset {n:200}
function nonios:bank/ui/preset {n:500}
function nonios:bank/ui/preset {n:1000}
execute if score #bb nx.eco matches 1.. run function nonios:bank/ui/wd_on with storage nonios:bank ui.a
execute if score #bb nx.eco matches ..0 run data modify storage nonios:bank ui.d.actions append from storage nonios:bank off[]
function nonios:bank/ui/show with storage nonios:bank ui
