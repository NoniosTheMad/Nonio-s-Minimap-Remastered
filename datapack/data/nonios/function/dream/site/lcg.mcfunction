# #h = #h * 1103515245 + 12345 (int overflow wraps); #hv = its high bits, 0..32767
scoreboard players operation #h nx.dream *= #lcg_a nx.dream
scoreboard players operation #h nx.dream += #lcg_c nx.dream
scoreboard players operation #hv nx.dream = #h nx.dream
scoreboard players operation #hv nx.dream /= #65536 nx.dream
scoreboard players operation #hv nx.dream %= #32768 nx.dream
