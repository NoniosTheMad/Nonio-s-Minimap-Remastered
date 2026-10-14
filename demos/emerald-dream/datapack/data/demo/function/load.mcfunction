scoreboard objectives add demo.ed trigger
scoreboard objectives add demo.c dummy
scoreboard objectives setdisplay sidebar nx.coins
scoreboard objectives modify nx.coins displayname {"text":"Coins","color":"gold"}
# coin stub until the purse branch lands: mined dream ores -> nx.coins (values from feat/coin-purse; emerald block is new)
scoreboard objectives add demo.m.em minecraft.mined:minecraft.emerald_ore
scoreboard objectives add demo.m.dem minecraft.mined:minecraft.deepslate_emerald_ore
scoreboard objectives add demo.m.dia minecraft.mined:minecraft.diamond_ore
scoreboard objectives add demo.m.gold minecraft.mined:minecraft.gold_ore
scoreboard objectives add demo.m.lap minecraft.mined:minecraft.lapis_ore
scoreboard objectives add demo.m.emb minecraft.mined:minecraft.emerald_block
execute unless data storage demo:state {built:1b} run schedule function demo:build 2t
