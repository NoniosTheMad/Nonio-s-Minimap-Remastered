# {team}: #<team> nx.bank += bank * interest_rate / 1000 (max interest_cap). The remainder below 1 coin carries over
# in #acc_<team> nx.eco (V2 did the same with whiteAccumulated/whiteRemoved), so small banks still earn over time.
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
$execute if score #icap nx.eco matches 1.. if score #i nx.eco > #icap nx.eco run scoreboard players set #acc_$(team) nx.eco 0
execute if score #icap nx.eco matches 1.. run scoreboard players operation #i nx.eco < #icap nx.eco
execute if score #i nx.eco matches ..0 run return 0
$scoreboard players operation #$(team) nx.bank += #i nx.eco
$tellraw @a[team=$(team)] [{"text":"🏦 Bank interest ","color":"gold"},{"text":"+","color":"yellow"},{"score":{"name":"#i","objective":"nx.eco"},"color":"yellow","bold":true},{"text":" coins (","color":"gray"},{"score":{"name":"#rw","objective":"nx.eco"},"color":"aqua"},{"text":".","color":"aqua"},{"score":{"name":"#rt","objective":"nx.eco"},"color":"aqua"},{"text":"%). Team bank: ","color":"gray"},{"score":{"name":"#$(team)","objective":"nx.bank"},"color":"gold"}]
$execute as @a[team=$(team)] at @s run playsound minecraft:block.amethyst_block.chime player @s ~ ~ ~ 0.8 1.2
