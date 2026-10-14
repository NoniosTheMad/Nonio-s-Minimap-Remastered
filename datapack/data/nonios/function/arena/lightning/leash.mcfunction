# macro (config.bounds): a rabbit that hopped out of the Arena goes back to the centre
$execute as @e[type=rabbit,tag=nx.lrabbit] unless entity @s[x=$(x),y=$(y),z=$(z),dx=$(dx),dy=$(dy),dz=$(dz)] run function nonios:arena/lightning/home with storage nonios:arena config.center
