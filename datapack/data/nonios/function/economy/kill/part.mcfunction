# {key, obj, label}: storage nonios:eco ab.<key> = "  +N label" (N = @s obj)
$execute store result storage nonios:eco ab.n int 1 run scoreboard players get @s $(obj)
$data modify storage nonios:eco ab.lbl set value "$(label)"
$data modify storage nonios:eco ab.key set value "$(key)"
function nonios:economy/kill/part_set with storage nonios:eco ab
