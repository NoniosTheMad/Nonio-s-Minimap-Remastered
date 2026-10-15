# as a landed dreamer (tag nx.in_dream), at them, every tick
function nonios:dream/wings/tick
function nonios:dream/pixie/tick
execute if score #t nx.dream matches 0 run function nonios:dream/void/tick
execute if score #t20 nx.dream matches 0 run function nonios:dream/site/tick
