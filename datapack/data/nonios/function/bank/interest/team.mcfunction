# {team}, every tick: #i = min(bank, 1,000,000) x #rate = interest per second in 1/10000 coin (<= 2e9, inside an int),
# capped at #icap x 10000. #acc_<team> += #i; every 200000 in it pays 1 coin (20 ticks x 10000), so a team earning N/s
# gets +1 every 20/N ticks. #last_<team> = the current coins per second (sidebar Income), #capped_<team> = at the cap.
$scoreboard players add #$(team) nx.bank 0
$scoreboard players add #acc_$(team) nx.eco 0
$scoreboard players set #capped_$(team) nx.eco 0
$execute if score #$(team) nx.bank matches ..0 run scoreboard players set #last_$(team) nx.eco 0
$execute if score #$(team) nx.bank matches ..0 run return run scoreboard players set #acc_$(team) nx.eco 0
$scoreboard players operation #i nx.eco = #$(team) nx.bank
scoreboard players operation #i nx.eco < #1000000 nx.eco
scoreboard players operation #i nx.eco *= #rate nx.eco
# cap in the same units (#icap >= 200000 would overflow x10000 and is above any possible #i anyway)
execute if score #icap nx.eco matches 1..199999 run scoreboard players operation #cu nx.eco = #icap nx.eco
execute if score #icap nx.eco matches 1..199999 run scoreboard players operation #cu nx.eco *= #10000 nx.eco
$execute if score #icap nx.eco matches 1..199999 if score #i nx.eco >= #cu nx.eco run scoreboard players set #capped_$(team) nx.eco 1
execute if score #icap nx.eco matches 1..199999 run scoreboard players operation #i nx.eco < #cu nx.eco
$scoreboard players operation #last_$(team) nx.eco = #i nx.eco
$scoreboard players operation #last_$(team) nx.eco /= #10000 nx.eco
$scoreboard players operation #acc_$(team) nx.eco += #i nx.eco
$scoreboard players operation #i nx.eco = #acc_$(team) nx.eco
scoreboard players operation #i nx.eco /= #200000 nx.eco
$scoreboard players operation #acc_$(team) nx.eco %= #200000 nx.eco
execute if score #i nx.eco matches ..0 run return 0
$scoreboard players operation #$(team) nx.bank += #i nx.eco
