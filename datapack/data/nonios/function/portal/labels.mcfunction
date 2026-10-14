# pad holograms: locked = price, open = name only
execute store result storage nonios:portal l.cost int 1 run data get storage nonios:config dream_cost
data modify storage nonios:portal l.team set value "white"
function nonios:portal/label with storage nonios:portal l
data modify storage nonios:portal l.team set value "black"
function nonios:portal/label with storage nonios:portal l
