# popup open: lifetime = 30 ticks + 10 per step in it (#psh hundredths), at most 80, from its opening
scoreboard players add @s nx.page 1
scoreboard players operation #pl nx.purse = @s nx.pgain
scoreboard players operation #pl nx.purse /= #psh nx.purse
scoreboard players operation #pl nx.purse *= #10 nx.purse
scoreboard players add #pl nx.purse 30
execute if score #pl nx.purse matches 81.. run scoreboard players set #pl nx.purse 80
scoreboard players operation #pl nx.purse -= @s nx.page
scoreboard players operation @s nx.ptime = #pl nx.purse
execute if score @s nx.ptime matches ..0 run function nonios:purse/gain_end
