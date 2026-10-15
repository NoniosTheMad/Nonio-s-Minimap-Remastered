# (Re)take the protection snapshot from config.protect {x1,y1,z1,x2,y2,z2,by} (none = off). arena/setup runs this last,
# on the freshly built arena. The backup copy sits at y by..by+(y2-y1), same x/z. Holes (air) in the backup = blocks
# that stay changeable: the regrowing core.
scoreboard players set #prot nx.arena 0
execute unless data storage nonios:arena config.protect.x1 run return 0
data modify storage nonios:arena prot set from storage nonios:arena config.protect
execute store result score #px1 nx.arena run data get storage nonios:arena prot.x1
execute store result score #py1 nx.arena run data get storage nonios:arena prot.y1
execute store result score #pz1 nx.arena run data get storage nonios:arena prot.z1
execute store result score #pdx nx.arena run data get storage nonios:arena prot.x2
execute store result score #pdy nx.arena run data get storage nonios:arena prot.y2
execute store result score #pdz nx.arena run data get storage nonios:arena prot.z2
scoreboard players operation #pdx nx.arena -= #px1 nx.arena
scoreboard players operation #pdy nx.arena -= #py1 nx.arena
scoreboard players operation #pdz nx.arena -= #pz1 nx.arena
execute store result storage nonios:arena prot.dx int 1 run scoreboard players get #pdx nx.arena
execute store result storage nonios:arena prot.dy int 1 run scoreboard players get #pdy nx.arena
execute store result storage nonios:arena prot.dz int 1 run scoreboard players get #pdz nx.arena
# backup top, and the y offset arena -> backup
execute store result score #poff nx.arena run data get storage nonios:arena prot.by
scoreboard players operation #pby2 nx.arena = #poff nx.arena
scoreboard players operation #pby2 nx.arena += #pdy nx.arena
execute store result storage nonios:arena prot.by2 int 1 run scoreboard players get #pby2 nx.arena
scoreboard players operation #poff nx.arena -= #py1 nx.arena
# players who could have mined a protected block: the box grown by 8 blocks (their coins for it are cancelled)
scoreboard players remove #px1 nx.arena 8
scoreboard players remove #py1 nx.arena 8
scoreboard players remove #pz1 nx.arena 8
scoreboard players add #pdx nx.arena 16
scoreboard players add #pdy nx.arena 16
scoreboard players add #pdz nx.arena 16
execute store result storage nonios:arena prot.ex int 1 run scoreboard players get #px1 nx.arena
execute store result storage nonios:arena prot.ey int 1 run scoreboard players get #py1 nx.arena
execute store result storage nonios:arena prot.ez int 1 run scoreboard players get #pz1 nx.arena
execute store result storage nonios:arena prot.edx int 1 run scoreboard players get #pdx nx.arena
execute store result storage nonios:arena prot.edy int 1 run scoreboard players get #pdy nx.arena
execute store result storage nonios:arena prot.edz int 1 run scoreboard players get #pdz nx.arena
function nonios:arena/protect/save with storage nonios:arena prot
# holes: core
execute as @e[type=marker,tag=nx.acore] at @s run function nonios:arena/protect/hole_here
scoreboard players set #prot nx.arena 1
