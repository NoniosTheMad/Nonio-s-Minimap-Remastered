# #sec nx.tmp -> #mm nx.tmp : #ss nx.tmp
scoreboard players operation #mm nx.tmp = #sec nx.tmp
scoreboard players operation #mm nx.tmp /= #60 nx.const
scoreboard players operation #ss nx.tmp = #sec nx.tmp
scoreboard players operation #ss nx.tmp %= #60 nx.const
