# {n}: one fixed withdraw button: live when the team bank (#bb nx.eco) holds at least n, greyed otherwise
$execute if score #bb nx.eco matches $(n).. run return run data modify storage nonios:bank ui.d.actions append value {label:{text:"$(n)",color:"yellow"},width:150,action:{type:"minecraft:run_command",command:"trigger nx.bankw set $(n)"}}
$data modify storage nonios:bank ui.d.actions append value {label:{text:"$(n)",color:"dark_gray"},tooltip:{text:"The bank holds less than $(n)"},width:150}
