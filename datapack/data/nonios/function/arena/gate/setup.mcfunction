# (Re)build the random-entry gates from storage nonios:arena config.gates / config.slots (arena/setup runs this).
# Gate = entry pad (marker nx.agate + nx.<team> at foot level, "ARENA" label). Slot = a landing point + its exit (marker nx.aslot at the exit).
kill @e[type=marker,tag=nx.agate]
kill @e[type=marker,tag=nx.aslot]
kill @e[type=text_display,tag=nx.agate_label]
scoreboard players set #gates nx.arena 0
scoreboard players set #slots nx.arena 0
data modify storage nonios:arena tmp.gl set from storage nonios:arena config.gates
function nonios:arena/gate/setup_gate
data modify storage nonios:arena tmp.sl set from storage nonios:arena config.slots
function nonios:arena/gate/setup_slot
function nonios:arena/gate/rotate
function nonios:arena/gate/state
