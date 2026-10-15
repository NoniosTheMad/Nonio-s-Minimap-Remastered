# as + at a held interest node at its payout; macro (storage payout) {team, name}: bank += bank x interest_permille / 1000
# (at most interest_cap) x #mult (Golden Hour)
$scoreboard players add #$(team) nx.bank 0
$scoreboard players operation #i nx.arena = #$(team) nx.bank
scoreboard players operation #i nx.arena *= #int_pm nx.arena
scoreboard players operation #i nx.arena /= #1000 nx.arena
scoreboard players operation #i nx.arena < #int_cap nx.arena
scoreboard players operation #i nx.arena *= #mult nx.arena
execute if score #i nx.arena matches ..0 run return 0
$scoreboard players operation #$(team) nx.bank += #i nx.arena
$tellraw @a[team=$(team)] [{text:"+",color:"gold"},{score:{name:"#i",objective:"nx.arena"},color:"gold"},{text:" bank  ",color:"gold"},{text:"$(name)",color:"gray"}]
$execute as @a[team=$(team)] at @s run playsound minecraft:block.amethyst_block.chime player @s ~ ~ ~ 0.4 1.6
