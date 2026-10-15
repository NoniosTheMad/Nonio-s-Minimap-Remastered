# as + at the core marker; reports to the player tagged nx.ar_ask
data modify storage nonios:arena tmp.cs set value {b:"another block (blocked)"}
execute if block ~ ~ ~ #minecraft:air run data modify storage nonios:arena tmp.cs.b set value "air (regrowing)"
data modify storage nonios:arena tmp.cbl set from storage nonios:arena config.core_blocks
function nonios:arena/core/status_find
tellraw @a[tag=nx.ar_ask] [{text:"[arena] core ",color:"aqua"},{storage:"nonios:arena",nbt:"tmp.cs.b",color:"yellow"},{text:" | regrow timer ",color:"gray"},{score:{name:"@s",objective:"nx.ar_t"},color:"yellow"},{text:" | regrown ",color:"gray"},{score:{name:"#c_grown",objective:"nx.arena"},color:"yellow"},{text:" | weight sum ",color:"gray"},{score:{name:"#cwsum",objective:"nx.arena"},color:"yellow"}]
