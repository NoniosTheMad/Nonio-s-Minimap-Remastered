# {team}: #<team> nx.bank += bank * #rate / 1000 (max #icap). The remainder below 1 coin carries over
# in #acc_<team> nx.eco (V2 did the same with whiteAccumulated/whiteRemoved), so small banks still earn over time.
# No chat line: the team sees the payout on its bank sidebar (economy/hud), with a soft chime.
$scoreboard players set #last_$(team) nx.eco 0
$scoreboard players set #capped_$(team) nx.eco 0
$scoreboard players add #$(team) nx.bank 0
$scoreboard players add #acc_$(team) nx.eco 0
$execute if score #$(team) nx.bank matches ..0 run return 0
$scoreboard players operation #i nx.eco = #$(team) nx.bank
scoreboard players operation #i nx.eco *= #rate nx.eco
$scoreboard players operation #i nx.eco += #acc_$(team) nx.eco
$scoreboard players operation #acc_$(team) nx.eco = #i nx.eco
$scoreboard players operation #acc_$(team) nx.eco %= #1000 nx.eco
scoreboard players operation #i nx.eco /= #1000 nx.eco
# capped payout: the remainder is dropped too
$execute if score #icap nx.eco matches 1.. if score #i nx.eco >= #icap nx.eco run scoreboard players set #capped_$(team) nx.eco 1
$execute if score #icap nx.eco matches 1.. if score #i nx.eco > #icap nx.eco run scoreboard players set #acc_$(team) nx.eco 0
execute if score #icap nx.eco matches 1.. run scoreboard players operation #i nx.eco < #icap nx.eco
execute if score #i nx.eco matches ..0 run return 0
$scoreboard players operation #$(team) nx.bank += #i nx.eco
$scoreboard players operation #last_$(team) nx.eco = #i nx.eco
$execute as @a[team=$(team)] at @s run playsound minecraft:block.amethyst_block.chime player @s ~ ~ ~ 0.4 1.4
