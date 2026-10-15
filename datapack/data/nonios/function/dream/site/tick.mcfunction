# as a landed dreamer, at them, once a second: exploration sites in the 3x3 cells (#cell = 192 blocks) around them.
# Each cell holds at most one site at a fixed point (hash of the cell + #seed); it is decided (and built) the first
# time a dreamer comes within #reach blocks of that point, then flagged with a barrier at y 0 under it.
execute store result score #px nx.dream run data get entity @s Pos[0]
execute store result score #pz nx.dream run data get entity @s Pos[2]
scoreboard players operation #cx0 nx.dream = #px nx.dream
scoreboard players operation #cx0 nx.dream /= #cell nx.dream
scoreboard players operation #cz0 nx.dream = #pz nx.dream
scoreboard players operation #cz0 nx.dream /= #cell nx.dream
scoreboard players set #dx nx.dream -1
scoreboard players set #dz nx.dream -1
function nonios:dream/site/cell
scoreboard players set #dz nx.dream 0
function nonios:dream/site/cell
scoreboard players set #dz nx.dream 1
function nonios:dream/site/cell
scoreboard players set #dx nx.dream 0
scoreboard players set #dz nx.dream -1
function nonios:dream/site/cell
scoreboard players set #dz nx.dream 0
function nonios:dream/site/cell
scoreboard players set #dz nx.dream 1
function nonios:dream/site/cell
scoreboard players set #dx nx.dream 1
scoreboard players set #dz nx.dream -1
function nonios:dream/site/cell
scoreboard players set #dz nx.dream 0
function nonios:dream/site/cell
scoreboard players set #dz nx.dream 1
function nonios:dream/site/cell
