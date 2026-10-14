title @a times 10 70 20
$title @a subtitle {text:"$(sub)",color:"$(color)"}
$title @a title {text:"$(name)",color:"$(color)",bold:true}
$execute as @a at @s run playsound $(sound) master @s ~ ~ ~ 1 1
$tellraw @a [{text:"★ ",color:"$(color)"},{text:"$(name)",color:"$(color)",bold:true},{text:"  $(sub)",color:"gray"}]
