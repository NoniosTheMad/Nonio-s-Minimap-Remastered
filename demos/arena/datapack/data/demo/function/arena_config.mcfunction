# Runs from #nonios:arena/config after the game defaults: the demo's own nodes, arena box and centre generator.
# This is how the real map plugs in its coordinates (or edit nonios:arena/config directly).
# Each node's bonus picks its rune (src/runes.json): haste = Sowilo, interest = Fehu, regrow = Jera.
data modify storage nonios:arena config.nodes set value [{id:"west",name:"West Node",x:-11,y:64,z:-3,bonus:"haste"},{id:"north",name:"North Node",x:0,y:64,z:-13,bonus:"interest"},{id:"east",name:"East Node",x:11,y:64,z:-3,bonus:"regrow"}]
data modify storage nonios:arena config.bounds set value {x:-19,y:60,z:-19,dx:38,dy:20,dz:38}
data modify storage nonios:arena config.center set value {x:0,y:64,z:-4}
# the emerald fountain, in the middle of the three nodes
data modify storage nonios:arena config.cgen set value {x:0,y:64,z:-3}
