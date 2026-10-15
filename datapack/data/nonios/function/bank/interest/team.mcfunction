# {team}: #<team> nx.bank += bank * #rate / 10000 (max #icap per second). Fractions of a coin carry over in
# #acc_<team> nx.eco (1/10000 coin), so a small bank still earns every few seconds (V2 did the same with
# whiteAccumulated/whiteRemoved). A capped second drops its remainder. No sound: it pays every second;
# the team sees it on its bank sidebar (economy/hud: Income +N/s).
$scoreboard players set #last_$(team) nx.eco 0
$scoreboard players set #capped_$(team) nx.eco 0
$scoreboard players add #$(team) nx.bank 0
$scoreboard players add #acc_$(team) nx.eco 0
$execute if score #$(team) nx.bank matches ..0 run return run scoreboard players set #acc_$(team) nx.eco 0
# min(bank, 1,000,000) x rate (<= 10000 bp) stays inside an int; a bank that large is capped anyway
$scoreboard players operation #i nx.eco = #$(team) nx.bank
scoreboard players operation #i nx.eco < #1000000 nx.eco
scoreboard players operation #i nx.eco *= #rate nx.eco
$scoreboard players operation #i nx.eco += #acc_$(team) nx.eco
$scoreboard players operation #acc_$(team) nx.eco = #i nx.eco
$scoreboard players operation #acc_$(team) nx.eco %= #10000 nx.eco
scoreboard players operation #i nx.eco /= #10000 nx.eco
$execute if score #icap nx.eco matches 1.. if score #i nx.eco >= #icap nx.eco run scoreboard players set #capped_$(team) nx.eco 1
$execute if score #icap nx.eco matches 1.. if score #i nx.eco >= #icap nx.eco run scoreboard players set #acc_$(team) nx.eco 0
execute if score #icap nx.eco matches 1.. run scoreboard players operation #i nx.eco < #icap nx.eco
execute if score #i nx.eco matches ..0 run return 0
$scoreboard players operation #$(team) nx.bank += #i nx.eco
$scoreboard players operation #last_$(team) nx.eco = #i nx.eco
