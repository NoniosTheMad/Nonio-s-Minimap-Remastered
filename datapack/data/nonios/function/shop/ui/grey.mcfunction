data modify storage nonios:shop ui.c.ncol set value "dark_gray"
data modify storage nonios:shop ui.c.pcol set value "dark_gray"
scoreboard players operation #need nx.tmp = #pr nx.tmp
scoreboard players operation #need nx.tmp -= #bal nx.tmp
execute store result storage nonios:shop ui.c.need int 1 run scoreboard players get #need nx.tmp
data modify storage nonios:shop ui.c.act set value 0b
function nonios:shop/ui/grey_tip with storage nonios:shop ui.c
