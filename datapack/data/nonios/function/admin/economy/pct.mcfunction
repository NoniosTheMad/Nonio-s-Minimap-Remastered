# {k}: #r nx.eco (basis points) -> storage nonios:ui eco.<k>w / eco.<k>t = "<w>.<t>%"
scoreboard players operation #rw nx.eco = #r nx.eco
scoreboard players operation #rw nx.eco /= #100 nx.eco
scoreboard players operation #r nx.eco %= #100 nx.eco
scoreboard players operation #r nx.eco /= #10 nx.eco
$execute store result storage nonios:ui eco.$(k)w int 1 run scoreboard players get #rw nx.eco
$execute store result storage nonios:ui eco.$(k)t int 1 run scoreboard players get #r nx.eco
