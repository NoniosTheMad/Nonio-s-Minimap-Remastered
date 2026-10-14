# ui.c = a page entry {n,label,ncol,atlas,sprite,price,count,bulk,sl,unit,blurb}: quantity and price in the current
# mode (ui.c.qt " xN", ui.c.pt "Pc" or "free"); greyed out (dark gray, tooltip "Nc short") when the purse can't pay it
function nonios:shop/lots {p:"ui.c"}
execute store result score #pr nx.tmp run data get storage nonios:shop ui.c.price
scoreboard players operation #pr nx.tmp *= #lots nx.tmp
execute store result score #q nx.tmp run data get storage nonios:shop ui.c.count
scoreboard players operation #q nx.tmp *= #lots nx.tmp
execute store result storage nonios:shop ui.c.tot int 1 run scoreboard players get #pr nx.tmp
execute store result storage nonios:shop ui.c.q int 1 run scoreboard players get #q nx.tmp
data modify storage nonios:shop ui.c.qt set value ""
execute if score #q nx.tmp matches 2.. run function nonios:shop/ui/qt with storage nonios:shop ui.c
data modify storage nonios:shop ui.c.pt set value "free"
execute if score #pr nx.tmp matches 1.. run function nonios:shop/ui/pt with storage nonios:shop ui.c
execute unless data storage nonios:shop ui.c.ncol run data modify storage nonios:shop ui.c.ncol set value "white"
data modify storage nonios:shop ui.c.pcol set value "gold"
data modify storage nonios:shop ui.c.tip set value ""
data modify storage nonios:shop ui.c.act set value 1b
execute if score #pr nx.tmp > #bal nx.tmp run function nonios:shop/ui/grey
