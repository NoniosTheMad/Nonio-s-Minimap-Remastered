# as + at a player: an enemy husk (other team, tag nx.captor, no AI) on the node nearest to them
data modify storage demo:arena d set value {t:"black",n:"Black",c:"dark_purple"}
execute if entity @s[team=black] run data modify storage demo:arena d set value {t:"white",n:"White",c:"white"}
execute as @e[type=marker,tag=nx.node,sort=nearest,limit=1] at @s run function demo:dummy_at with storage demo:arena d
