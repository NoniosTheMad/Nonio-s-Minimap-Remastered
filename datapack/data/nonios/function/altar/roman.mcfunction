# {s,k}: storage nonios:altar v.<k> = score <s> nx.altar as a roman numeral (1-5, else the number)
$execute store result storage nonios:altar v.$(k) int 1 run scoreboard players get $(s) nx.altar
$execute if score $(s) nx.altar matches 1 run data modify storage nonios:altar v.$(k) set value "I"
$execute if score $(s) nx.altar matches 2 run data modify storage nonios:altar v.$(k) set value "II"
$execute if score $(s) nx.altar matches 3 run data modify storage nonios:altar v.$(k) set value "III"
$execute if score $(s) nx.altar matches 4 run data modify storage nonios:altar v.$(k) set value "IV"
$execute if score $(s) nx.altar matches 5 run data modify storage nonios:altar v.$(k) set value "V"
