# as + at a node marker, macro {team, tname, col, own, st}: the node now belongs to $(team)
$scoreboard players set @s nx.ar_own $(own)
$scoreboard players set #st nx.arena $(st)
scoreboard players operation @s nx.ar_t = @s nx.ar_iv
$tellraw @a [{text:"⚑ ",color:"$(col)"},{text:"$(tname)",color:"$(col)",bold:true},{text:" claimed ",color:"gray"},{entity:"@s",nbt:"data.label",color:"yellow"}]
$execute as @a[team=$(team)] at @s run playsound minecraft:ui.toast.challenge_complete master @s ~ ~ ~ 0.8 1.2
$execute as @a[team=!$(team)] at @s run playsound minecraft:block.bell.resonate master @s ~ ~ ~ 0.8 0.7
$function nonios:arena/rune/flare {team:"$(team)"}
$data modify storage nonios:arena cap set value {team:"$(team)"}
data modify storage nonios:arena cap.node set from entity @s data.id
data modify storage nonios:arena cap.name set from entity @s data.label
function #nonios:arena/on_capture
