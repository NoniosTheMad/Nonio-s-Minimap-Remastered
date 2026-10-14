scoreboard players set #t nx.eco 0
$execute store result score #t nx.eco run data get storage nonios:config tier_bonus[$(i)]
scoreboard players operation #bonus nx.eco += #t nx.eco
