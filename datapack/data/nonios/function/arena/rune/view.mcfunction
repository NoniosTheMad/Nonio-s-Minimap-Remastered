# as + at a node, storage rx ready: draw for every player within config.rune.view blocks of the glyph
data modify storage nonios:arena rv set value {}
data modify storage nonios:arena rv.gy set from entity @s data.gy
data modify storage nonios:arena rv.rune set from entity @s data.rune
data modify storage nonios:arena rv.view set from storage nonios:arena config.rune.view
function nonios:arena/rune/view_m with storage nonios:arena rv
