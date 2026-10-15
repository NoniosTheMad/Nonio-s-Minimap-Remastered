# {n, lab, tip}: one live button (fixed slot) -> /trigger demo.ec set n
$data modify storage demo:im acts append value {label:{text:"$(lab)"},tooltip:{text:"$(tip)"},width:74,action:{type:"minecraft:run_command",command:"trigger demo.ec set $(n)"}}
