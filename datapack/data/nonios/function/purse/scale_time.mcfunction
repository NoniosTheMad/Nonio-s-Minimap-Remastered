# #st nx.purse = 100 + w_grow * seconds since the match started / 60
execute store result score #st nx.purse run time query gametime
scoreboard players operation #st nx.purse -= #t0 nx.eco
scoreboard players operation #st nx.purse /= #20 nx.eco
scoreboard players operation #st nx.purse *= #w_grow nx.purse
scoreboard players operation #st nx.purse /= #60 nx.purse
execute if score #st nx.purse matches ..-1 run scoreboard players set #st nx.purse 0
scoreboard players add #st nx.purse 100
