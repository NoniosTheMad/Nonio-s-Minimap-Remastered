# Runs from #nonios:arena/config after the game defaults: the demo's own nodes and arena box.
# This is how the real map plugs in its coordinates (or edit nonios:arena/config directly).
data modify storage nonios:arena config.nodes set value [{id:"west",name:"West Node",x:-11,y:64,z:-3},{id:"north",name:"North Node",x:0,y:64,z:-13},{id:"east",name:"East Node",x:11,y:64,z:-3}]
data modify storage nonios:arena config.bounds set value {x:-19,y:60,z:-19,dx:38,dy:20,dz:38}
data modify storage nonios:arena config.center set value {x:0,y:64,z:-4}
