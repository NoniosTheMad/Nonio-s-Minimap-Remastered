# {team}, every tick: #i = min(bank, #ibase) x #ppm = interest per period in 1/#idiv coin (1000000; mode B 10000). #acc_<team> += #i; each
# #ithr (= period in ticks x 1000000) in it pays 1 coin, so a team earning N per period gets +1 every period/N.
# #last_<team> = coins per period now (sidebar Income), #capped_<team> = the bank is above the earning base ("max").
$scoreboard players add #$(team) nx.bank 0
$scoreboard players add #acc_$(team) nx.eco 0
$scoreboard players set #capped_$(team) nx.eco 0
$execute if score #$(team) nx.bank matches ..0 run scoreboard players set #last_$(team) nx.eco 0
$execute if score #$(team) nx.bank matches ..0 run return run scoreboard players set #acc_$(team) nx.eco 0
$scoreboard players operation #i nx.eco = #$(team) nx.bank
$execute if score #i nx.eco >= #ibase nx.eco run scoreboard players set #capped_$(team) nx.eco 1
scoreboard players operation #i nx.eco < #ibase nx.eco
scoreboard players operation #i nx.eco *= #ppm nx.eco
$function nonios:talisman/accrue {team:"$(team)"}
$scoreboard players operation #last_$(team) nx.eco = #i nx.eco
$scoreboard players operation #last_$(team) nx.eco /= #idiv nx.eco
$scoreboard players operation #acc_$(team) nx.eco += #i nx.eco
$scoreboard players operation #i nx.eco = #acc_$(team) nx.eco
scoreboard players operation #i nx.eco /= #ithr nx.eco
$scoreboard players operation #acc_$(team) nx.eco %= #ithr nx.eco
execute if score #i nx.eco matches ..0 run return 0
$scoreboard players operation #$(team) nx.bank += #i nx.eco
