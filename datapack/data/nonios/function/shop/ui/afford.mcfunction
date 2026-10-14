# ui.c.col / tip: green "Click to buy" or red "Not enough coins" (#bal nx.tmp = the buyer's coins)
execute store result score #p nx.tmp run data get storage nonios:shop ui.c.price
data modify storage nonios:shop ui.c.col set value "green"
data modify storage nonios:shop ui.c.tip set value "Click to buy"
execute if score #p nx.tmp > #bal nx.tmp run data modify storage nonios:shop ui.c.col set value "red"
execute if score #p nx.tmp > #bal nx.tmp run data modify storage nonios:shop ui.c.tip set value "Not enough coins"
