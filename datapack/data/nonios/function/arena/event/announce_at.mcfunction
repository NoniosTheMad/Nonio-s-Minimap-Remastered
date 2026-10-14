title @a times 10 70 20
$title @a subtitle [{text:"$(sub) at ",color:"$(color)"},{text:"$(where)",color:"yellow",bold:true}]
$title @a title {text:"$(name)",color:"$(color)",bold:true}
$execute as @a at @s run playsound $(sound) master @s ~ ~ ~ 1 1
$tellraw @a [{text:"★ ",color:"$(color)"},{text:"$(name)",color:"$(color)",bold:true},{text:"  $(sub) at ",color:"gray"},{text:"$(where)",color:"yellow"}]
