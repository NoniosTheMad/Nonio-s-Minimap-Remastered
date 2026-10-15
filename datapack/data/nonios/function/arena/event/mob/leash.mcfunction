# macro (config.bounds): event mobs outside the Arena box go back to its centre
$execute as @e[tag=nx.ev_mob] unless entity @s[x=$(x),y=$(y),z=$(z),dx=$(dx),dy=$(dy),dz=$(dz)] run function nonios:arena/lightning/home with storage nonios:arena config.center
