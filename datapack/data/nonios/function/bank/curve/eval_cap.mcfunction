# #ct nx.eco = match seconds -> #capm nx.eco = the mode A cap curve there (1/1000 coin per second). Swaps the cap curve
# in for bank/curve/eval and back: nonios:bank curve, #cn and #ppm are left as they were.
data modify storage nonios:bank tmp set from storage nonios:bank curve
data modify storage nonios:bank curve set from storage nonios:bank capc
scoreboard players operation #cnB nx.eco = #cn nx.eco
scoreboard players operation #cn nx.eco = #cnA nx.eco
scoreboard players operation #ppmS nx.eco = #ppm nx.eco
function nonios:bank/curve/eval
scoreboard players operation #capm nx.eco = #ppm nx.eco
scoreboard players operation #ppm nx.eco = #ppmS nx.eco
scoreboard players operation #cn nx.eco = #cnB nx.eco
data modify storage nonios:bank curve set from storage nonios:bank tmp
