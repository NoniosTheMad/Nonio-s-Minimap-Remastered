$data modify storage nonios:dream bar.a set string storage nonios:dream bar.full 0 $(n)
$data modify storage nonios:dream bar.b set string storage nonios:dream bar.full $(n)
title @s actionbar [{"text":"Waking up ","color":"green"},{"nbt":"bar.a","storage":"nonios:dream","color":"green","bold":true},{"nbt":"bar.b","storage":"nonios:dream","color":"dark_gray","bold":true},{"text":" ","color":"gray"},{"nbt":"bar.s","storage":"nonios:dream","color":"gray"},{"text":"s","color":"gray"}]
