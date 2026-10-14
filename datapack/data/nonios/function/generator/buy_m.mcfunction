# as + at the generator; buyer tagged nx.gen_buyer
execute if score @s nx.gen_lvl matches 3.. run return run tellraw @p[tag=nx.gen_buyer] {text:"Already at max level (3).",color:"yellow"}
execute if score @s nx.gen_lvl matches ..1 run scoreboard players operation #cost nx.gen = #cost2 nx.gen
execute if score @s nx.gen_lvl matches 2 run scoreboard players operation #cost nx.gen = #cost3 nx.gen
scoreboard players add @p[tag=nx.gen_buyer] nx.coins 0
execute if score @p[tag=nx.gen_buyer] nx.coins < #cost nx.gen run return run tellraw @p[tag=nx.gen_buyer] [{text:"Upgrade costs ",color:"red"},{score:{name:"#cost",objective:"nx.gen"},color:"gold"},{text:" coins. You have ",color:"red"},{score:{name:"@p[tag=nx.gen_buyer]",objective:"nx.coins"},color:"gold"},{text:".",color:"red"}]
scoreboard players operation @p[tag=nx.gen_buyer] nx.coins -= #cost nx.gen
function nonios:generator/upgrade
tellraw @p[tag=nx.gen_buyer] [{text:"Generator upgraded to Lv ",color:"green"},{score:{name:"@s",objective:"nx.gen_lvl"},color:"yellow"},{text:" (-",color:"green"},{score:{name:"#cost",objective:"nx.gen"},color:"gold"},{text:" coins)",color:"green"}]
