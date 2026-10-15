# as a player
execute unless score #cgen nx.arena matches 1 run return run tellraw @s {text:"  centre generator: none",color:"gray"}
tag @s add nx.cg_ask
execute as @e[type=marker,tag=nx.cgen,limit=1] run tellraw @a[tag=nx.cg_ask] [{text:"  centre generator: Lv ",color:"gray"},{score:{name:"@s",objective:"nx.gen_lvl"},color:"yellow"},{text:", ",color:"gray"},{score:{name:"#crolls",objective:"nx.arena"},color:"yellow"},{text:" rolls (banks ",color:"gray"},{score:{name:"#cbank",objective:"nx.arena"},color:"gold"},{text:"), pot ",color:"gray"},{score:{name:"@s",objective:"nx.gen_pot"},color:"gold"},{text:"/",color:"gray"},{score:{name:"@s",objective:"nx.gen_cap"},color:"gold"},{text:", next drop in ",color:"gray"},{score:{name:"@s",objective:"nx.gen_t"},color:"yellow"},{text:" ticks",color:"gray"}]
tag @s remove nx.cg_ask
