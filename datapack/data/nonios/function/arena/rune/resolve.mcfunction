# macro (storage n): n.rd = config.runes.<rune> {g,name,n}; n.label = "<glyph> <Name>"
$data modify storage nonios:arena n.rd set from storage nonios:arena config.runes.$(rune)
function nonios:arena/rune/label with storage nonios:arena n.rd
