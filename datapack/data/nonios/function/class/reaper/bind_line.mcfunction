# as/at the Reaper: a violet chain of light from the lantern to the bound victim
execute store result storage nonios:class bl.x double 0.01 run data get entity @e[tag=nx.reaper_bindhit,limit=1] Pos[0] 100
execute store result storage nonios:class bl.y double 0.01 run data get entity @e[tag=nx.reaper_bindhit,limit=1] Pos[1] 100
execute store result storage nonios:class bl.z double 0.01 run data get entity @e[tag=nx.reaper_bindhit,limit=1] Pos[2] 100
function nonios:class/reaper/bind_line_at with storage nonios:class bl
