# {k}: #dv nx.eco (1/1000 coin per second) -> storage demo:im a.<k>s = "W.FF", a.<k>m = whole coins per minute
scoreboard players operation #dw nx.eco = #dv nx.eco
scoreboard players operation #dw nx.eco /= #1000 nx.eco
scoreboard players operation #df nx.eco = #dv nx.eco
scoreboard players operation #df nx.eco %= #1000 nx.eco
scoreboard players operation #df nx.eco /= #10 nx.eco
scoreboard players operation #dm nx.eco = #dv nx.eco
scoreboard players operation #dm nx.eco *= #60 nx.eco
scoreboard players operation #dm nx.eco /= #1000 nx.eco
data modify storage demo:im f set value {}
$data modify storage demo:im f.k set value "$(k)"
execute store result storage demo:im f.w int 1 run scoreboard players get #dw nx.eco
execute store result storage demo:im f.f int 1 run scoreboard players get #df nx.eco
execute store result storage demo:im f.m int 1 run scoreboard players get #dm nx.eco
function demo:im/fmt2 with storage demo:im f
