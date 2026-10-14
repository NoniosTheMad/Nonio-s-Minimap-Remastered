scoreboard players operation #s demo.c = #channel_ticks nx.dream
scoreboard players operation #s demo.c /= #20 nx.dream
scoreboard players operation #g demo.c = #regrow_ticks nx.dream
scoreboard players operation #g demo.c /= #20 nx.dream
tellraw @s [{"text":"[demo] channel ","color":"yellow"},{"score":{"name":"#s","objective":"demo.c"},"color":"green"},{"text":" s, vein regrow "},{"score":{"name":"#g","objective":"demo.c"},"color":"green"},{"text":" s, veins/arrival "},{"score":{"name":"#veins","objective":"nx.dream"},"color":"green"},{"text":", arrival range +/-"},{"score":{"name":"#range","objective":"nx.dream"},"color":"green"}]
