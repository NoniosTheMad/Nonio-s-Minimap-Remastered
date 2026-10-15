# macro {gy, rune, view}: per viewer, from the glyph centre facing them (a billboard: ^x = their right, ^y = up)
$execute positioned ~ ~$(gy) ~ as @a[distance=..$(view)] facing entity @s eyes run function nonios:arena/rune/gen/$(rune) with storage nonios:arena rx
$execute if score #tip nx.arena matches 1.. positioned ~ ~$(gy) ~ as @a[distance=..$(view)] facing entity @s eyes run function nonios:arena/rune/gen/$(rune)_tip with storage nonios:arena rx
