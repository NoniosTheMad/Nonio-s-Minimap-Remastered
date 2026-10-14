# #own nx.nxs = owner of the pressure node (1 white, 2 black, 0 none / no such node)
$execute as @e[type=marker,tag=nx.node] if data entity @s {data:{id:"$(node)"}} run scoreboard players operation #own nx.nxs = @s nx.ar_own
