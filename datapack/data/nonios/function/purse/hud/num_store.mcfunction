# {src:"<holder> <objective>"} in hundredths -> #hp (0..99), #ht tenths digit, #hz hundredths digit, #hw whole
# (nx.purse) and the same in storage nonios:purse hn {p,t,w}
$scoreboard players operation #hp nx.purse = $(src)
scoreboard players operation #hw nx.purse = #hp nx.purse
scoreboard players operation #hw nx.purse /= #100 nx.purse
scoreboard players operation #hp nx.purse %= #100 nx.purse
scoreboard players operation #ht nx.purse = #hp nx.purse
scoreboard players operation #ht nx.purse /= #10 nx.purse
scoreboard players operation #hz nx.purse = #hp nx.purse
scoreboard players operation #hz nx.purse %= #10 nx.purse
execute store result storage nonios:purse hn.p int 1 run scoreboard players get #hp nx.purse
execute store result storage nonios:purse hn.t int 1 run scoreboard players get #ht nx.purse
execute store result storage nonios:purse hn.w int 1 run scoreboard players get #hw nx.purse
